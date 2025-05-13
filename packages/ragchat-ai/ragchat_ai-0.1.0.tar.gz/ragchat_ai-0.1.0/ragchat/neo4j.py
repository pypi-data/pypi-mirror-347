import asyncio
import aiofiles
from neo4j import (
    AsyncGraphDatabase,
    exceptions as neo4jExceptions,
    SummaryCounters,
)
from typing import Any, Optional, List, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from ragchat.log import get_logger, abbrev
from ragchat.utils import retry, timeit
from ragchat.definitions import get_base_target, NodeType, BaseNode, Relation, Flow, Filters, BaseFilters

logger = get_logger(__name__)

class Neo4jSettings(BaseSettings):
    url: Optional[str] = None
    local_hosts: Optional[List[str]] = ["localhost", "host.docker.internal"]
    bolt_port: int = 7687
    user: str = None
    password: str = None
    pool_size: int = 100
    timeout: int = 30
    acq_timeout: int = 60
    retry_time: int = 30
    retries: int = 3

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="NEO4J_")

    async def initialize(self):
        """
        Attempts to connect to Neo4j using the provided URL or default local hosts.
        Sets the `url` attribute to the first successful connection URL.
        Raises ConnectionError if no connection can be established.
        """
        urls_to_check = set()
        if self.url:
            urls_to_check.add(self.url)

        for host in self.local_hosts:
            urls_to_check.add(f"bolt://{host}:{self.bolt_port}")

        connection_attempts = [self._attempt_connection(url) for url in urls_to_check]
        results = await asyncio.gather(*connection_attempts, return_exceptions=True)
        self.url = next((result for result in results if result), None)
        if not self.url:
            raise ConnectionError(f"Could not connect to Neo4j using any of the default hosts or the provided URL: {self.url}")

        logger.info(f"Connection established using {self.url.split('@')[-1]}")

    async def _attempt_connection(self, url):
        """Attempts to connect to Neo4j at the given URL and returns the URL if successful."""
        try:
            driver = AsyncGraphDatabase.driver(url, auth=(self.user, self.password))
            async with driver:
                await driver.verify_connectivity()
            await driver.close()
            return url
        except Exception:
            return None

class MemoryGraph:
    def __init__(self, settings: Optional[Neo4jSettings] = None):
        self.settings = settings or Neo4jSettings()

        self.rerank_clauses = {
            "chunk": 0.0,
            "topic": 0.0,
            "fact": 0.0,
            "entity": "1 - apoc.text.jaroWinklerDistance(raw, n.content)",
        }
        self.rerank_weights = {
            "chunk": 0.0,
            "topic": 0.00,
            "fact": 0.00,
            "entity": 0.5,
        }

        self.retry_on = [ # only retry on these errors
            neo4jExceptions.TransientError,
            neo4jExceptions.ServiceUnavailable,
            neo4jExceptions.DatabaseError,
        ]

    async def initialize(self):
        """Initializes the Neo4j database with necessary constraints and indexes."""
        await self.settings.initialize()
        self.graph = AsyncGraphDatabase.driver(
            self.settings.url,
            auth=(self.settings.user, self.settings.password),
            max_connection_pool_size=self.settings.pool_size,
            connection_timeout=self.settings.timeout,
            connection_acquisition_timeout=self.settings.acq_timeout,
            max_transaction_retry_time=self.settings.retry_time,
        )

        queries  = [
            f"create index idx_{flow}_{k} if not exists for (n:{flow}) on (n.{k});"
            for flow in Flow
            for k in BaseNode.indexed_keys(flow)
        ]

        queries += [
            f"create index idx_chunk_node_id if not exists for (n:chunk) on (n.node_id);"
        ]

        async with self.graph.session() as session:
            tasks = [session.run(q) for q in queries]
            await asyncio.gather(*tasks)
            logger.info("Neo4j initialized successfully.")

    def _get_filter_clause(
        self,
        filters: BaseFilters,
        node_letter: str = 'n',
    ) -> str:
        """
        Build a Neo4j filter clause string based on provided filters.
        """
        with_custom = f"with *, apoc.convert.fromJsonMap({node_letter}.custom) as custom"
        filter_clauses = [
            f"coalesce({node_letter}.{k}, custom.{k}) {condition.operator} $filters.{k}"
            for k, v in filters.std_conditions().items()
            for condition in v if k in BaseNode.indexed_keys()
        ]

        if not filter_clauses:
            raise ValueError(f"Missing filter.")

        filter_clause_str = """
            and """.join(filter_clauses)
        filter_clause_str = f"""
            {with_custom}
            where {filter_clause_str}
        """ if filter_clauses else ""

        return filter_clause_str

    def _get_cleanup_clause(
        self,
        node_type: NodeType,
        node_letter: str = 'n',
    ) -> str:
        """
        Generate a Cypher clause to clean up orphaned nodes after deletion.

        The cleanup clause identifies and deletes:
        1. First-degree adjacent nodes that were connected only to the nodes being deleted and are different node_type from the nodes being deleted.
        2. Second-degree adjacent nodes connected only to nodes being deleted (original and first degree), thus about to become dangling nodes.

        Args:
            element_type: The node_type of element being deleted (e.g., NodeType.CHUNK)
            node_letter: The variable name used for the nodes being deleted in the preceding MATCH clause.

        Returns:
            str: Cypher clause for cleanup operations.

        NOTE: This clause assumes it's inserted *after* a MATCH clause identifying the nodes
              to delete (bound to `node_letter`) and *before* the final DETACH DELETE
              of those original nodes.
        """
        label = node_type.value # Get the string label from NodeType
        n = node_letter # alias for node_letter for readability
        r = f"""
            // Collect the original nodes identified for deletion
            with collect({n}) as x_nodes                                    // nodes being deleted
            with x_nodes as {n}_nodes, x_nodes                              // keep a pointer to the original nodes

            // 1. From first-degree adjacent nodes
            optional match (x)
            where not x:{label}                                             // Is not the node_type being deleted
            and exists((x)--(:{label}))                                     // Has connection to the node_type being deleted
            and all(y in [(x)--(z:{label}) | z] where y in x_nodes)         // Their only {label} connections are to nodes being deleted
            with {n}_nodes, x_nodes, x where x is not null                  // filter out nulls
            with {n}_nodes, x_nodes, collect(distinct x) as _nodes
            with {n}_nodes, x_nodes + _nodes as x_nodes                     // combine nodes being deleted

            // 2. From first/second-degree adjacent nodes
            optional match (x)
            where not x:{label}                                             // Is not the node_type being deleted
            and not any(y in [(x)--(z) | z] where not y in x_nodes)         // Connected only to nodes being deleted
            with {n}_nodes, x_nodes, x where x is not null                  // filter out nulls
            with {n}_nodes, x_nodes, collect(distinct x) as _nodes
            with {n}_nodes, x_nodes + _nodes as x_nodes                     // combine nodes being deleted

            // 3. delete cleanup nodes and unwind original nodes
            with {n}_nodes, x_nodes
            foreach (x in apoc.coll.subtract(x_nodes, {n}_nodes) | detach delete x)

            // 4. Unwind original nodes
            with {n}_nodes unwind {n}_nodes as {n}
        """

        return r

    def _get_projection(
            self,
            return_fields: set[str],
            node_type: NodeType = NodeType.CHUNK,
            as_map_str: bool = True,
            node_letter: str = "n",
            include: Optional[set[str]] = {"node_type", "flow"},
            exclude: Optional[set[str]] = {"embedding", "similarity"},
        ) -> dict | str:
        """
        Generates a Cypher projection string or dictionary for returning node properties.

        Args:
            return_fields: Set of fields to include in the projection. If None, uses default indexed keys for the node type.
            node_type: The type of node being projected (used for default keys).
            as_map_str: If True, returns a Cypher map string (e.g., "n{field1, field2}"). If False, returns a dictionary.
            node_letter: The variable name used for the node in the Cypher query.
            include: Set of fields to always include, even if not in return_fields (unless explicitly excluded).
            exclude: Set of fields to always exclude.

        Returns:
            dict | str: The Cypher projection as a dictionary or string.
        """
        return_fields = return_fields or (BaseNode.node_keys(node_type))
        return_fields = set(return_fields) - (exclude or set()) | (include or set())

        r = {field: f"{node_letter}.{field}" for field in return_fields}
        r |= {k: v for k, v in {
            "custom":       f"case when {node_letter}.custom is not null then apoc.convert.fromJsonMap({node_letter}.custom) else null end",
            "similarity":   f"similarity",
        }.items() if k in return_fields}

        if as_map_str:
            r = [f"{k}: {v}" for k, v in r.items()]
            r = node_letter + "{" + ", ".join(r) + "}"

        return r

    @retry()
    async def upsert_relations(
        self,
        relations: List[Relation],
        threshold: float,
        rr_threshold: float,
    ) -> List[Relation]:
        """
        Adds or updates relations and their associated nodes in the graph.

        Merges nodes if they already exist based on indexed keys or vector similarity
        (for new nodes without IDs). Sets properties and creates/merges relationships.

        Args:
            relations: A list of Relation objects to upsert.
            threshold: Vector similarity threshold for finding existing nodes.
            rr_threshold: Reranked similarity threshold for finding existing nodes.

        Returns:
            List[Relation]: The list of relations with updated node_ids for newly created nodes.
        """

        if not relations:
            return []

        if any(not (rel.chunk.model_fields_set & rel.chunk.indexed_keys(rel.chunk.flow)) for rel in relations):
            raise ValueError(f"Missing indexed field.")

        n_results = 0
        node_ids = {}
        async with self.graph.session() as session:
            for r in relations:
                # --- find existing nodes and their ids ---
                new_nodes = [n for n in r.to_list() if not n.node_id]
                # upsert ops use metadata as filters
                filters_target = get_base_target(BaseFilters, r.chunk.flow)
                filters = filters_target(**{k: getattr(r.chunk, k) for k in BaseNode.search_space() if getattr(r.chunk, k) is not None})
                if new_nodes:
                    # get ids if they already exist
                    for n in new_nodes:
                        n.node_id = node_ids.get(n._hash)

                    # re-filter, only nodes that don't have a node_id
                    new_nodes = [n for n in new_nodes if not n.node_id]

                if new_nodes:
                    # very similar nodes will be merged
                    return_fields = {"node_id", "content"}
                    tasks = [self.vector_search_nodes(n.node_type, filters, n.content, n.embedding, threshold, rr_threshold=rr_threshold, limit=1, return_fields=return_fields) for n in new_nodes]
                    existing_nodes = await asyncio.gather(*tasks)

                    # assign ids
                    for i, n in enumerate(new_nodes):
                        if not existing_nodes[i]:
                            continue
                        if existing_nodes[i][0].node_type == NodeType.CHUNK and existing_nodes[i][0] != n:
                            continue # chunks have to be exact match
                        n.node_id = existing_nodes[i][0].node_id
                        node_ids[n._hash] = n.node_id

                    # re-filter, only nodes that don't have a node_id
                    new_nodes = [n for n in new_nodes if not n.node_id]

                logger.debug(f"upserting relation: {abbrev(r)}")
                parameters = r.to_id_nodes()
                parameters.update({"filters": filters.std_dict()})

                # --- build cypher ---
                nodes = [r.fact, r.chunk] + r.topics + r.entities
                match_create_clauses = []
                # match or create clauses
                for i, n in enumerate(nodes):
                    with_clause = f"with {', '.join([f'n{j}' for j in range(i)])}\n" if i > 0 else ""
                    if n.node_id:
                        match_create_clauses.append(f"{with_clause}match (n{i}:{n.node_type}:{n.flow}) where n{i}.node_id = $n{i}.node_id")
                    else:
                        match_create_clauses.append(f"{with_clause}create (n{i}:{n.node_type}:{n.flow})")

                # set properties clauses
                set_clauses = []
                for i, n in enumerate(nodes):
                    weird_fields = {
                        "node_id": f"n{i}.node_id = coalesce(n{i}.node_id, randomUUID())",
                        "created_at": f"n{i}.created_at = coalesce(n{i}.created_at, timestamp())",
                        "updated_at": f"n{i}.updated_at = timestamp()",
                        "custom": f"n{i}.custom = case when coalesce($n{i}.custom, n{i}.custom) is not null then apoc.convert.toJson(coalesce($n{i}.custom, n{i}.custom)) else null end",
                    }

                    s  = [f"n{i}.{k} = coalesce($n{i}.{k}, n{i}.{k})" for k in BaseNode.node_keys(n.node_type) if k not in weird_fields]
                    s += [v for v in weird_fields.values()]
                    set_str = ",\n".join(s)

                    set_clauses.append(f"""
                    set
                        {set_str}
                    """)

                # relation clauses
                # chunk-[fact]->fact
                # topic-[fact]->fact
                # entity-[fact]->fact
                relation_clauses = []
                for i, n in enumerate(nodes):
                    if i != 0:
                        relation_clauses.append(f"merge (n{i})-[:{NodeType.FACT}]->(n0)")

                # return clauses
                return_clauses = [f"n{i}.node_id" for i in range(len(nodes))]

                # Combine all parts
                cypher = "\n".join(match_create_clauses)
                cypher += "\n" + "\n".join(set_clauses)
                cypher += "\n" + "\n".join(relation_clauses)
                cypher += "\nreturn " + ", ".join(return_clauses)

                # Execute the Cypher query
                try:
                    result = await session.run(cypher, parameters=parameters)
                    data = await result.data()
                    if data:
                        for i, n in enumerate(nodes):
                            n.node_id = data[0][f"n{i}.node_id"]
                            node_ids[n._hash] = n.node_id

                    n_results += 1

                except Exception as e:
                    if not any(isinstance(e, e_type) for e_type in self.retry_on):
                        logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
                    raise

        logger.info(f"Upserted {n_results}/{len(relations)} relations" + (f": {abbrev(relations)}" if logger.level <= 10 else ""))
        return relations

    @retry()
    async def get_nodes_by_ids(
        self,
        node_ids: List[str],
        node_type: NodeType = NodeType.CHUNK,
        return_fields: set[str] = None,
    ) -> List[BaseNode]:
        """
        Retrieve multiple nodes by their IDs.

        Args:
            node_ids: List of node IDs to retrieve
            element_type: Type of element to retrieve (default: CHUNK)
            return_fields: Fields to return for each node.

        Returns:
            List[Node]: The retrieved nodes (empty list if none found)
        """
        if not node_ids:
            return []
        filters = BaseFilters(node_ids=node_ids)

        cypher = f"""
            match (n:{node_type})
            {self._get_filter_clause(filters, 'n')}

            return {self._get_projection(return_fields)}
        """

        try:
            parameters = {"filters": filters.std_dict()}

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)
                records = await result.data()

            if not records:
                logger.debug(f"No {node_type} nodes found with IDs {node_ids}")
                return []

            nodes = []
            for record in records:
                nodes.append(BaseNode(**record['n']))

            return nodes

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    @retry()
    async def get_nodes(
        self,
        filters: Filters,
        node_type: NodeType = NodeType.CHUNK,
        return_fields: Optional[set[str]] = None,
        order_by: str = 'updated_at',
        order_direction: str = 'desc',
        limit: int = 100,
    ) -> List[BaseNode]:
        """
        Retrieve all nodes of a specific node_type with filtering and ordering.

        Args:
            filters: Filters to apply to the query.
            node_type: Type of element to retrieve (default: CHUNK)
            limit: Maximum number of nodes to return (default: None, returns all)
            order_by: Property to order results by (default: None)
            order_direction: Direction of ordering, "asc" or "desc" (default: "asc")
            return_fields: Fields to return for each node.

        Returns:
            List[Node]: The retrieved nodes (empty list if none found)
        """
        if not order_by in ['created_at','updated_at']:
            raise ValueError(f"order_by must be a valid field, order_by: {order_by}")
        if not order_direction in ['asc', 'desc']:
            raise ValueError(f"order_direction must be a valid direction, order_direction: {order_direction}")
        if not filters:
            raise ValueError(f"Missing filters.")

        # Add ordering if specified
        order_clause = ""
        if order_by:
            order_clause = f"order by n.{order_by} {order_direction}"

        # Add limit if specified
        limit_clause = ""
        if limit is not None:
            limit_clause = f"limit {limit}"

        cypher = f"""
            match (n:{filters._flow}:{node_type})
            {self._get_filter_clause(filters, 'n')}
            {order_clause}
            {limit_clause}
            return {self._get_projection(return_fields, node_type=node_type)}
        """

        try:
            parameters = {"filters": filters.std_dict()}

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)
                records = await result.data()

            if not records:
                logger.debug(f"No {node_type} nodes found with the specified criteria")
                return []

            nodes = []
            for record in records:
                nodes.append(BaseNode(**record['n']))

            return nodes

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    @retry()
    async def get_updated_at(
        self,
        filters: Filters,
        return_fields: set[str] = None,
        order_by: Optional[str] = 'updated_at',
        order_direction: Optional[str] = 'desc',
        limit: Optional[int] = 100,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the latest 'updated_at' timestamp for nodes matching filters, grouped by return fields.

        Args:
            filters: Filters to apply to the query.
            return_fields: Fields to group by and return along with the max updated_at. Defaults to indexed keys.
            limit: Maximum number of results to return (default: 100)
            order_by: Property to order results by ('created_at' or 'updated_at', default: 'updated_at')
            order_direction: Direction of ordering, "asc" or "desc" (default: "desc")
        """
        if not filters:
            raise ValueError(f"Missing filters.")
        if order_by and not order_by in ['created_at','updated_at']:
            raise ValueError(f"order_by must be a valid field, order_by: {order_by}")
        if order_direction and not order_direction in ['asc', 'desc']:
            raise ValueError(f"order_direction must be a valid direction, order_direction: {order_direction}")

        order_clause = ""
        if order_by:
            order_clause = f"order by n.{order_by} {order_direction}"

        limit_clause = ""
        if limit is not None:
            limit_clause = f"limit {limit}"

        return_fields = return_fields or BaseNode.indexed_keys()
        projection =", ".join([f"{v} as {k}" for k, v in self._get_projection(return_fields, as_map_str=False, include=None).items()])

        cypher = f"""
            match (n:{filters._flow}:chunk)
            {self._get_filter_clause(filters, 'n')}
            return {projection}, max(n.updated_at) as updated_at
            {order_clause}
            {limit_clause}
        """

        try:
            parameters = {"filters": filters.std_dict()}

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)
                records = await result.data()

            if not records:
                logger.debug(f"No chunk nodes found with the specified criteria")
                return []

            return records

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    @retry()
    async def update_nodes_by_ids(
        self,
        nodes: List[BaseNode],
        return_fields: set[str] = None,
    ) -> List[BaseNode]:
        """
        Update multiple nodes by their IDs, preserving existing properties when new values are null.

        Args:
            nodes: List[Node objects with updated properties
            return_fields: Fields to return for the updated nodes.

        Returns:
            List[Node]: The updated nodes (empty list if none found)
        """
        if not nodes:
            return []

        node_data = []
        for node in nodes:
            properties = node.model_dump(mode="json", exclude={"node_id", "node_type", "flow"})
            node_data.append({
                "node_id": node.node_id,
                "node_type": node.node_type,
                "flow": node.flow,
                "properties": {k: v for k, v in properties.items()}
            })

        cypher = f"""
            unwind $node_data as data
            match (n:data.flow:data.node_type)
            where n.node_id = data.node_id

            set n = apoc.map.merge(n, data.properties, {{
                // For each property in the update, use coalesce to keep existing value if new is null
                // k, v -> case when v is null then n[k] else v end
                k, v -> coalesce(v, n[k])
            }})

            return {self._get_projection(return_fields)}
        """

        try:
            parameters = {"node_data": node_data}

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)
                records = await result.data()

            if not records:
                logger.debug(f"No nodes found with the provided IDs")
                return []

            updated_nodes = []
            for record in records:
                updated_nodes.append(BaseNode(**record['n']))

            return updated_nodes

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    @retry()
    async def delete_nodes_by_ids(
        self,
        node_ids: List[str],
        node_type: NodeType = NodeType.CHUNK,
        return_fields: set[str] = None,
        cleanup: bool = True,
    ) -> List[BaseNode]:
        """
        Delete multiple nodes by their IDs.

        Args:
            node_ids: List of node IDs to delete
            element_type: Type of element to delete (default: CHUNK)
            return_fields: Fields to return for the deleted nodes.
            cleanup: Whether to perform cleanup operations on orphaned nodes.

        Returns:
            List[BaseNode]: The deleted nodes (empty list if none found).
        """
        if not node_ids:
            return []
        filters = BaseFilters(node_ids=node_ids)
        projection = self._get_projection(return_fields, as_map_str=True)[1:]

        cypher = f"""
            match (n:{node_type})
            {self._get_filter_clause(filters, 'n')}
            {self._get_cleanup_clause(node_type, 'n') if cleanup else ""}
            with n, {projection} as r
            detach delete n
            return r
        """

        try:
            parameters = {"filters": filters.std_dict()}

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)
                records = await result.data()

            if not records:
                logger.debug(f"No {node_type} nodes found with the specified criteria")
                return []

            nodes = [BaseNode(**r['r']) for r in records]

            return nodes

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    @retry()
    async def delete_nodes(
        self,
        filters: Filters,
        node_type: NodeType = NodeType.CHUNK,
        return_fields: set[str] = None,
        cleanup: bool = True,
    ) -> List[BaseNode]:
        """
        Delete nodes based on filters.

        Args:
            element_type: Type of element to delete (default: chunk)
            filters: Filters to apply to the query (required)
            return_fields: Fields to return for the deleted nodes.
            cleanup: Whether to run cleanup operations for orphaned nodes (default: True)

        Returns:
            List[BaseNode]: The deleted nodes (empty list if none found).
        """
        if not filters:
            raise ValueError(f"Missing filters.")

        projection = self._get_projection(return_fields, as_map_str=True)[1:]

        cypher = f"""
            match (n:{filters._flow}:{node_type})
            {self._get_filter_clause(filters, 'n')}
            {self._get_cleanup_clause(node_type, 'n') if cleanup else ""}
            with n, {projection} as r
            detach delete n
            return r
        """

        try:
            parameters = {"filters": filters.std_dict()}

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)
                records = await result.data()

            if not records:
                logger.debug(f"No {node_type} nodes found with the specified criteria")
                return []

            nodes = [BaseNode(**r['r']) for r in records]

            return nodes


        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    @retry()
    async def vector_search_nodes(
        self,
        node_type: NodeType,
        filters: Filters,
        raw_string: str,
        embeddings: List[float],
        threshold: float,
        order_by: str = "similarity",
        limit: int = 100,
        rr_threshold: Optional[float] = None,
        return_fields: set[str] = None,
    ) -> List[BaseNode]:
        """
        Find the best matching nodes based on embedding similarity and optional reranking.

        Args:
            node_type: The type of node to search for.
            filters: Filters to apply to the search.
            raw_string: The original string used to generate the embeddings (used for reranking).
            embeddings: The embedding vector to search with.
            threshold: The minimum base similarity score required.
            order_by: Property to order results by ('similarity', 'created_at', or 'updated_at').
            limit: Maximum number of nodes to return.
            rr_threshold: The minimum reranked similarity score required (defaults to threshold).
            return_fields: Fields to return for each node.

        Returns:
            List[BaseNode]: A list of matching nodes, ordered by the specified property.
        """
        if not raw_string:
            return []
        if not filters:
            raise ValueError(f"Missing filters.")
        if not order_by in ['similarity','created_at','updated_at']:
            raise ValueError(f"order_by must be a valid field, order_by: {order_by}")
        if not rr_threshold:
            rr_threshold = threshold

        filter_clause = self._get_filter_clause(filters, 'n') or "where true"
        order_by = f"n.{order_by}" if order_by != "similarity" else "similarity"
        cypher = f"""
        match (n:{filters._flow}:{node_type})
        {filter_clause}
        and n.embedding is not null

        with n, $raw_string as raw,
        vector.similarity.cosine(n.embedding, $embedding) as base_similarity
        where base_similarity >= $threshold

        with n,
        (1.0 - {self.rerank_weights[node_type.value]}) * base_similarity + {self.rerank_weights[node_type.value]} * ({self.rerank_clauses[node_type.value]}) as similarity
        where similarity >= $rr_threshold
        order by {order_by} desc
        limit $limit

        return {self._get_projection(return_fields, node_type=node_type, include={"flow", "node_type", "similarity"})}
        order by {order_by} asc
        """

        try:
            parameters = {
                "raw_string": raw_string,
                "embedding": embeddings,
                "filters": filters.std_dict(),
                "threshold": threshold,
                "rr_threshold": rr_threshold,
                "limit": limit
            }

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)
                records = await result.data()

            nodes = [BaseNode(**r['n']) for r in records]

            return nodes

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    @retry()
    @timeit
    async def search_chunks_from_relations(
        self,
        relations: List[Relation],
        filters: Filters,
        threshold: float,
        limit: int = 32,
        char_limit: int = 12000, # ~ 3k tokens (ollama default max 4k)
        explain: bool = False,
        return_fields: set[str] = None,
    ) -> List[BaseNode]:
        """
        Searches for relevant chunk nodes connected to the nodes within the provided relations.

        Uses vector similarity search on the related nodes (Fact, Topic, Entity) and
        then finds the connected Chunk nodes. Results are weighted and reranked based
        on similarity and node type connections.

        Args:
            relations: A list of Relation objects containing the input nodes (Fact, Topic, Entity) to search from.
            filters: Filters to apply to the search (applied to both input nodes and resulting chunks).
            threshold: The minimum similarity score required for related nodes.
            limit: Maximum number of chunk nodes to return.
            char_limit: Maximum total character count for the returned chunks.
            explain: If True, includes explanation details in the returned nodes.
            return_fields: Fields to return for each chunk node.

        Returns:
            List[BaseNode]: A list of relevant chunk nodes, limited by count and character limit,
                            and sorted by custom index ('ichunk') and creation time.
        """
        if not relations:
            return []
        if not filters:
            raise ValueError(f"Missing filters.")

        match_clauses = {
            f"{NodeType.TOPIC}":    f"(c:{NodeType.CHUNK})-->(:{NodeType.FACT})<--(n)",
            f"{NodeType.FACT}":     f"(c:{NodeType.CHUNK})-->(n)",
            f"{NodeType.ENTITY}":   f"(c:{NodeType.CHUNK})-->(:{NodeType.FACT})<--(n)",
        }

        call_clauses = [
            f"""
            with input_node
            where input_node.node_type = '{k}'
            match (n:{filters._flow}:{k})
            {self._get_filter_clause(filters, 'n')}
            and n.embedding is not null

            with input_node, input_node.content as raw, n, vector.similarity.cosine(input_node.embedding, n.embedding) as base_similarity
            where $threshold <= base_similarity

            match {match_clauses[k]}
            {self._get_filter_clause(filters, 'n')}

            with input_node, n, c,
                (1.0 - {self.rerank_weights[k]}) * base_similarity + {self.rerank_weights[k]} * ({self.rerank_clauses[k]}) as similarity

            return c, similarity
            {', "("+tostring(round(similarity * 1000.0) / 1000.0)+"="+input_node.content+"<=>"+n.content+")" as explain order by similarity desc' if explain else ''}
            """
            for k in match_clauses.keys()
        ]
        include = {"node_type", "flow", "similarity"}
        if explain:
            include |= {"types", "explain"}
        projection = self._get_projection(return_fields, node_letter='c', include=include)

        cypher = f"""
            unwind $input_nodes as input_node
            call (input_node) {{
                {"union".join(call_clauses)}
            }}

            // get max similarity per input-chunk
            with input_node, c, max(similarity) as similarity
            {', collect(explain)[0] as explain order by input_node.node_type' if explain else ', false as explain'}
            where $threshold <= similarity

            // count chunks
            with collect({{i: input_node, c: c, s: similarity, e: explain}}) as _map, count(distinct c) as total_chunks
            unwind _map as map
            with total_chunks, map.i as input_node, collect(map) as _map, count(distinct map.c) as input_chunks
            with input_node, _map, 1.0 + log(toFloat(total_chunks+1)/toFloat(input_chunks+1)) as weight
            {', total_chunks, input_chunks' if explain else ''}
            unwind _map as map

            with input_node, map.c as c, map.s as similarity, weight
            {', "(log("+total_chunks+"/"+input_chunks+")="+tostring(round(weight * 1000.0) / 1000.0)+")"+" * "+map.e as explain' if explain else ''}

            // get weighted avg similarity per node_type
            with c, input_node.node_type as node_type, avg(similarity) as similarity, avg(weight) as weight
            {', collect(explain) as explain'if explain else ''}
            with c, node_type, similarity^(1.0/weight) as similarity
            {', {node_type: node_type+"("+tostring(round(similarity*1000.0) / 1000.0)+"^(1/"+tostring(round(weight * 1000.0) / 1000.0)+")="+tostring(round(similarity^(1.0/weight)*1000.0)/1000.0)+")", explain: explain} as explain' if explain else ''}

            // get weighted avg similarity per chunk
            with c, collect(node_type) as types, avg(similarity) as similarity
            {', collect(explain) as explain' if explain else ''}
            where size(types) = {len(match_clauses)}
            order by similarity desc
            limit $limit

            return {projection}
            {' order by c.similarity desc' if explain else ''}
        """

        try:
            id_chunks = {}

            async def _get_id_chunks(r: Relation) -> Dict[str, Any]:
                nonlocal id_chunks
                input_nodes = r.to_list()
                if any(not n.embedding for n in input_nodes):
                    raise ValueError(f"Missing embedding for nodes.")

                parameters = {
                    "input_nodes": [n.model_dump(mode='json') for n in input_nodes],
                    "filters": filters.std_dict(),
                    "threshold": threshold,
                    "limit": limit,
                }

                async with self.graph.session() as session:
                    result = await session.run(cypher, parameters=parameters)
                    records = await result.data()

                if explain:
                    r = [{'c': {k: v for k, v in r['c'].items() if k != 'raw'}} for r in records]
                    logger.debug(f"records: {r}")

                return {r['c']['node_id']: r['c'] for r in records}

            tasks = [_get_id_chunks(r) for r in relations]
            id_chunks = {}
            for d in await asyncio.gather(*tasks):
                id_chunks.update(d)

            if not id_chunks:
                logger.debug(f"Nothing found. Filters {filters}")
                return []

            chunks = [BaseNode(**c) for c in id_chunks.values()]
            chunks.sort(key=lambda x: x.similarity)
            chunks = self._limit_chunks(chunks, limit, char_limit)
            chunks.sort(key=lambda x: (x.custom.get("ichunk", 0), x.created_at))

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nFilters {filters}")
            raise

        return chunks

    @retry()
    async def export(
        self,
        file_name: str,
        filters: Filters,
        order_by: str = 'updated_at',
        order_direction: str = 'asc',
        return_fields: set[str] = None,
    ) -> None:
        """
        Dumps all nodes matching filters to a file, streaming the results to avoid loading everything into memory.

        Args:
            file_name: The name of the file to write to.
            filters: Filters to apply to the query.
            order_by: Property to order results by (default: 'updated_at').
            order_direction: Direction of ordering, "asc" or "desc" (default: "asc").
            return_fields: Fields to return for each node.
        """
        if not filters:
            raise ValueError(f"Missing filters.")
        if not order_by in ['created_at','updated_at']:
            raise ValueError(f"order_by must be a valid field, order_by: {order_by}")
        if not order_direction in ['asc', 'desc']:
            raise ValueError(f"order_direction must be a valid direction, order_direction: {order_direction}")

        # Add ordering if specified
        order_clause = ""
        if order_by:
            order_clause = f"order by n.{order_by} {order_direction}"

        cypher = f"""
            match (n:{filters._flow})
            {self._get_filter_clause(filters, 'n')}
            {order_clause}
            return {self._get_projection(return_fields)}
        """

        try:
            parameters = {"filters": filters.std_dict()}

            async with self.graph.session() as session:
                result = await session.run(cypher, parameters=parameters)

                async with aiofiles.open(file_name, 'w') as f:
                    async for record in result:
                        node = BaseNode(**record['n'])
                        await f.write(node.model_dump_json() + '\n')  # Write each node as a JSON string on a new line

            logger.info(f"Successfully exported nodes to {file_name}")

        except Exception as e:
            if not any(isinstance(e, e_type) for e_type in self.retry_on):
                logger.exception(f"Query:\n{cypher},\nParameters: {abbrev(parameters)}")
            raise

    async def close(self):
        """Closes the Neo4j graph driver connection."""
        await self.graph.close()

    def _limit_chunks(self, chunks: list[BaseNode], limit: int, char_limit: int) -> list[BaseNode]:
        """
        Limits the number of chunks and the total character count of their content.

        Args:
            chunks: The list of chunk nodes to limit.
            limit: The maximum number of chunks to return.
            char_limit: The maximum total character count allowed across all returned chunks.

        Returns:
            list[BaseNode]: The limited list of chunk nodes.
        """
        chunks = chunks[:limit]
        chars = 0
        limited_chunks = []
        for c in chunks:
            chars += len(c.content)
            if char_limit < chars:
                break
            limited_chunks.append(c)

        return limited_chunks

