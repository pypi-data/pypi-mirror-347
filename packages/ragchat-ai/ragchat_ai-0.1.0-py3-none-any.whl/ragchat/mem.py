import os
import re
import asyncio
import aiofiles
import uuid
from typing import Any, Dict, List, Optional, Tuple, AsyncIterator, Union, Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
# local imports
from ragchat.definitions import (
    Flow,
    ChunkResult,
    MessageClassification,
    Relation,
    BaseNode,
    Node,
    NodeType,
    get_base_target,
    FileStatus,
    FileState,
    Language,
    BaseMetadata,
    ChatMetadata,
    FileMetadata,
    ChatFilters,
    Filters,
    )
from ragchat.log import get_logger, configure_logging
from ragchat.embedding import Embedder
from ragchat.neo4j import MemoryGraph
from ragchat.llm import LLM, Message
from ragchat.utils import get_unique
from ragchat.parser import chunk_text, messages_to_user_text
from ragchat.progress import BatchProgress
from ragchat.prompts import RETRIEVAL_CHAT, RETRIEVAL_RAG


logger = get_logger(__name__)
configure_logging()

class MemorySettings(BaseSettings):
    chunk_char_size: int = 2000
    language: Language = Language.ENGLISH
    local_hosts: Optional[List[str]] = ["localhost", "host.docker.internal"]
    
    model_config = SettingsConfigDict(case_sensitive=False)

    @field_validator("local_hosts", mode="before")
    @classmethod
    def validate_hosts(cls, v):
        if isinstance(v, str):
            return [m.strip() for m in v.split(',')]
        return v

logger.debug("testing")
logger.info("testing")
logger.warning("testing")
logger.error("testing")
logger.critical("testing")

class Memory:
    """
    Manages memory operations including upserting, searching, and recalling information
    using LLMs, embeddings, and a graph database.
    """
    def __init__(self, settings: Optional[MemorySettings] = None):
        """
        Initializes the Memory instance with settings and core components.

        Args:
            settings (Optional[MemorySettings], optional): Configuration settings.
                                                           Defaults to MemorySettings().
        """
        self.settings = settings or MemorySettings()
        self.llm = LLM()
        self.embedder = Embedder()
        self.graph = MemoryGraph()

        # Dictionary to track ongoing file processing tasks for cancellation
        self._processing_tasks: Dict[str, asyncio.Task] = {}

    async def initialize(self) -> None:
        """
        Initializes the underlying graph database, LLM, and embedder components.
        """
        await asyncio.gather(
            self.graph.initialize(),
            self.llm.initialize(),
            self.embedder.initialize(),
        )

    async def upsert(
        self,
        messages: List[Message],
        metadata: ChatMetadata | FileMetadata,
        context: Optional[str] = None,
        language: Optional[Language] = None,
        threshold: Optional[float] = 0.90,
        rr_threshold: Optional[float] = 0.95,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        emb_kwargs: Optional[Dict[str, Any]] = None,
    ) -> List[Relation]:
        """
        Extracts relations from messages, embeds them, and upserts into the graph.

        Args:
            messages (List[Message]): The messages to process.
            metadata (ChatMetadata | FileMetadata): Metadata associated with the messages.
            context (Optional[str], optional): Additional context for the LLM. Defaults to None.
            language (Optional[Language], optional): Language for processing. Defaults to settings.language.
            threshold (Optional[float], optional): Similarity threshold for upserting nodes. Defaults to 0.90.
            rr_threshold (Optional[float], optional): Similarity threshold for upserting relations. Defaults to 0.95.
            llm_kwargs (Optional[Dict[str, Any]], optional): Arguments for the LLM. Defaults to None.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder. Defaults to None.

        Returns:
            List[Relation]: A list of relations successfully upserted into the graph.
        """
        flow = metadata._flow
        language = language or self.settings.language
        llm_kwargs = llm_kwargs or {}
        emb_kwargs = emb_kwargs or {}

        try:
            text = messages_to_user_text(messages)

            rels = await self.llm.extract_relations(
                text=text,
                metadata=metadata,
                context=context,
                flow=flow,
                language=language,
                **llm_kwargs
            )
            await self.embedder.embed_relations(rels, **emb_kwargs)
            graph_result: List[Relation] = await self.graph.upsert_relations(rels, threshold, rr_threshold)
        except Exception as e:
            logger.exception(f"Error adding memory: {e}")
            raise # Re-raise the exception after logging
        return graph_result

    async def cancel_file_upsert(self, task_id: str) -> bool:
        """
        Cancels a running file upsert task by its ID.

        Args:
            task_id (str): The ID of the task to cancel.

        Returns:
            bool: True if cancellation was requested, False if task not found or finished.
        """
        task = self._processing_tasks.get(task_id)
        if task and not task.done():
            task.cancel()
            logger.info(f"Cancellation requested for task ID: {task_id}")
            return True
        logger.warning(f"Task ID not found or already finished: {task_id}")
        return False

    async def file_upsert(
        self,
        metadata: FileMetadata,
        context: Optional[str] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        emb_kwargs: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterator[FileState]:
        """
        Processes a file, extracts relations from chunks, embeds them, and upserts into the graph.
        Yields FileState objects representing the current processing state.

        Args:
            metadata (FileMetadata): Metadata associated with the file.
            context (Optional[str], optional): Additional context for the LLM. Defaults to None.
            flow (Optional[Flow], optional): Processing flow (e.g., FILE). Defaults to settings.flow.
            language (Optional[Language], optional): Language for processing. Defaults to settings.language.
            llm_kwargs (Optional[Dict[str, Any]], optional): Arguments for the LLM. Defaults to None.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder. Defaults to None.

        Yields:
            FileState: The current state of processing for the file.
        """
        # Get base name for logging/task ID
        file_path = metadata.path
        file_name = os.path.basename(file_path)

        # Generate a unique task ID for this file processing early
        task_id = f"file_upsert_{file_name}_{uuid.uuid4()}"
        current_task = asyncio.current_task()
        # Track the current task for potential cancellation
        if current_task: self._processing_tasks[task_id] = current_task
        logger.info(f"Starting file_upsert for {file_path} with task_id {task_id}")

        # Initialize the FileState object to track progress
        file_state = FileState(file_path=file_path, task_id=task_id, status=FileStatus.PENDING)

        # Yield the initial PENDING state to signal start
        yield file_state
        logger.debug(f"File_upsert yielded initial PENDING state for {file_path}")

        try:
            if not metadata.folder_id:
                raise ValueError(f"Missing metadata.folder_id")

            if not metadata.file_id:
                metadata.file_id = file_name
                logger.warning(f"Upsert metadata missing source_id, using file name as source_id for file {file_path}")

            # Use provided or default settings for flow, language, kwargs
            language = language or self.settings.language
            llm_kwargs = llm_kwargs or {}
            emb_kwargs = emb_kwargs or {}

            file_text = ""
            try:
                # Read file asynchronously
                async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
                    file_text = await f.read()
            except FileNotFoundError:
                error_msg = f"File not found: {file_path}"
                logger.error(error_msg)
                yield FileState.create_error_state(file_path, error_msg, task_id)
                return
            except Exception as e:
                error_msg = f"Error reading file {file_path}: {e}"
                logger.exception(error_msg)
                yield FileState.create_error_state(file_path, error_msg, task_id)
                return

            try:
                # Chunk the file text
                chunks = chunk_text(file_text, chunk_char_size=self.settings.chunk_char_size)
            except Exception as e:
                # Handle chunking errors
                error_msg = f"Error chunking text for file {file_path}: {e}"
                logger.exception(error_msg)
                # Update and yield error state, then exit
                yield FileState.create_error_state(file_path, error_msg, task_id)
                return

            # Handle empty file case (no chunks)
            if not chunks:
                logger.warning(f"File {file_path} has no content to process.")
                # Update state for empty file: 0 chunks, COMPLETED status
                file_state.total_chunks = 0
                file_state.status = FileStatus.COMPLETED
                # Yield completed state for empty file and exit
                yield file_state
                return

            # Use file_name in context for readability if no context provided
            context = context or f"Source: {file_name}"
            total_chunks = len(chunks)

            # Initialize lists for previous topics/entities (used by relation extraction)
            prev_topics = []
            prev_entities = []

            # Iterate through each chunk for processing
            for i, chunk_content in enumerate(chunks):
                # Check if the task has been cancelled before processing the chunk
                if current_task and current_task.cancelled():
                    logger.info(f"File processing for {file_path} cancelled before chunk {i+1}.")
                    # Update state for cancellation and exit
                    file_state.status = FileStatus.CANCELLED
                    file_state.error = "Processing cancelled."
                    yield file_state
                    return

                file_state.total_chunks = total_chunks
                file_state.status = FileStatus.PROCESSING
                yield file_state
                logger.debug(f"File_upsert yielded state with total_chunks for {file_path} ({total_chunks} chunks)")

                # Initialize ChunkResult for the current chunk to track its outcome
                chunk_result = ChunkResult(chunk_index=i)

                try:
                    # --- Process a single chunk ---
                    # Add chunk index to the metadata
                    m = metadata.model_dump() | {"ichunk": i, "chunks": total_chunks}
                    metadata = type(metadata)(**m)
                    # Extract relations using LLM
                    rels = await self.llm.extract_relations(
                        text=chunk_content,
                        metadata=metadata,
                        context=context,
                        prev_topics=prev_topics,
                        prev_entities=prev_entities,
                        flow=flow or Flow.FILE,
                        language=language,
                        **llm_kwargs
                    )
                    await self.embedder.embed_relations(rels, **emb_kwargs)
                    # Upsert relations into the graph database
                    upserted: List[Relation] = await self.graph.upsert_relations(rels, 0.9, 0.95)

                    # Get IDs of successfully upserted chunks
                    ids = get_unique([r.chunk.node_id for r in upserted])
                    chunk_result.ids = ids

                    # Update the file state with the successful chunk result
                    file_state.update_with_chunk_result(chunk_result)
                    # Yield the updated state with the new chunk result
                    yield file_state
                    logger.debug(f"File_upsert yielded state after chunk {i+1}/{total_chunks} for {file_path}")
                    # --- End Process a single chunk ---

                except asyncio.CancelledError:
                    # Handle cancellation specifically during chunk processing
                    logger.info(f"File processing for {file_path} cancelled during chunk {i+1}.")
                    # Update state for cancellation
                    file_state.status = FileStatus.CANCELLED
                    file_state.error = "Processing cancelled."
                    yield file_state # Yield the CANCELLED state
                    raise # Re-raise CancelledError to be caught by the caller (batch processor) or outer except

                except Exception as e:
                    # Handle errors during chunk processing
                    logger.exception(f"Error processing chunk {i+1}/{total_chunks} from {file_path}: {e}")
                    # Add error to the chunk result
                    chunk_result.error = str(e)
                    # Update the file state with the chunk result containing the error
                    file_state.update_with_chunk_result(chunk_result)
                    # Yield the state with the chunk error result (processing continues for other chunks)
                    yield file_state

            # If the loop finishes normally, the status should be COMPLETED
            logger.info(f"File_upsert finished chunk processing for {file_path}. Final status: {file_state.status}")
            # Yield the final state explicitly to ensure the consumer sees the COMPLETED status,
            # unless it's already in a terminal state (like ERROR from an outer exception).
            if not file_state.is_terminal:
                 # This case should ideally not be reached if update_with_chunk_result works correctly
                 # and no outer exceptions occurred. But as a safeguard:
                 file_state.status = FileStatus.COMPLETED
                 yield file_state
            elif file_state.status == FileStatus.COMPLETED:
                 # Explicitly yield the final COMPLETED state if it was set by the last chunk
                 yield file_state


        except asyncio.CancelledError:
            # Catch cancellation that happens outside the chunk loop
            logger.info(f"File processing task for {file_path} was cancelled (caught in outer try).")
            # Ensure the state is marked as cancelled if it wasn't already
            if not file_state.is_terminal:
                file_state.status = FileStatus.CANCELLED
                file_state.error = "Processing cancelled."
                yield file_state # Yield the CANCELLED state
            raise # Re-raise CancelledError

        except Exception as e:
            # Catch any unhandled exceptions during the entire process
            logger.exception(f"Unhandled error processing file {file_path}: {e}")
            # Ensure the state is marked as error if it wasn't already
            if not file_state.is_terminal:
                file_state.status = FileStatus.ERROR
                file_state.error = str(e)
                yield file_state # Yield the ERROR state

        finally:
            # Clean up the task entry specific to this call regardless of outcome
            if task_id in self._processing_tasks:
                del self._processing_tasks[task_id]
            logger.debug(f"File_upsert cleanup for {file_path}, task_id {task_id}")

    async def file_upsert_batch(
        self,
        metadatas: List[FileMetadata],
        context: Optional[str] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        emb_kwargs: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterator[FileState]:
        """
        Upserts memories from multiple files concurrently, yielding FileState objects
        representing the processing state of each file as updates become available.

        Args:
            metadatas (List[FileMetadata]): A list of metadata objects for the files to process.
            context (Optional[str], optional): Additional context for the LLM. Defaults to None.
            flow (Optional[Flow], optional): Processing flow (e.g., FILE). Defaults to settings.flow.
            language (Optional[Language], optional): Language for processing. Defaults to settings.language.
            llm_kwargs (Optional[Dict[str, Any]], optional): Arguments for the LLM. Defaults to None.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder. Defaults to None.

        Yields:
            FileState: The current state of processing for a specific file in the batch.
        """
        total_files = len(metadatas)
        logger.info(f"Starting batch for {total_files} files (batch_size={self.llm.settings.batch_size})")

        # --- Input Validation ---
        if any(not f.file_id for f in metadatas):
            logger.warning("Upsert operation missing source_id for some files, using file name as source_id")
            for f in metadatas:
                f.file_id = os.path.basename(f.path)
        
        file_ids = [f.file_id for f in metadatas]
        if len(file_ids) != len(set(file_ids)):
            logger.warning("'source_id' values are not unique.")

        if total_files == 0:
            logger.warning("No files to process in batch.")
            return
        # --- End Input Validation ---

        results_queue: asyncio.Queue[Union[FileState, object]] = asyncio.Queue()
        sentinel = object()
        async def run_single_file_producer(sem: asyncio.Semaphore, metadata: FileMetadata, context: str, q: asyncio.Queue, **kwargs_for_upsert):
            """Runs a single file upsert and puts results in queue."""
            file_path = metadata.path
            task_id_for_error: Optional[str] = f"file_upsert_{os.path.basename(file_path)}_init_error_{uuid.uuid4()}"
            first_result_yielded = False

            await sem.acquire()
            try:
                async for state in self.file_upsert(
                    metadata=metadata,
                    context=context,
                    **kwargs_for_upsert
                ):
                    if not first_result_yielded and state.task_id:
                        task_id_for_error = state.task_id
                        first_result_yielded = True
                    await q.put(state)
                logger.debug(f"Producer for {file_path} finished iterating file_upsert.")

            except asyncio.CancelledError:
                logger.warning(f"Cancellation caught in run_single_file_producer wrapper for {file_path}")
                cancelled_state = FileState.create_cancelled_state(file_path, task_id=task_id_for_error)
                await q.put(cancelled_state)
                raise

            except Exception as e:
                logger.exception(f"Exception caught in run_single_file_producer wrapper for {file_path}")
                error_state = FileState.create_error_state(file_path, f"Internal error during processing: {e}", task_id=task_id_for_error)
                await q.put(error_state)
                raise

            finally:
                sem.release()
                await q.put(sentinel)
                logger.debug(f"Producer for {file_path} put sentinel.")


        producer_tasks: List[asyncio.Task] = []

        common_kwargs = {
            "flow": flow,
            "language": language,
            "llm_kwargs": llm_kwargs,
            "emb_kwargs": emb_kwargs,
        }

        try:
            for metadata in metadatas:
                task = asyncio.create_task(
                    run_single_file_producer(
                        sem=self.llm.semaphore,
                        metadata=metadata,
                        context=context,
                        q=results_queue,
                        **common_kwargs
                    )
                )
                producer_tasks.append(task)
                logger.debug(f"Created producer task for {metadata.path}")

        except Exception as e:
            logger.exception("Error during batch task creation.")
            for task in producer_tasks:
                if not task.done(): task.cancel()
            await asyncio.gather(*producer_tasks, return_exceptions=True)
            raise


        completed_producers = 0
        try:
            while completed_producers < total_files:
                result = await results_queue.get()

                if result is sentinel:
                    completed_producers += 1
                    logger.debug(f"Sentinel received. Completed producers: {completed_producers}/{total_files}")
                elif isinstance(result, FileState):
                    yield result
                else:
                    logger.error(f"Received unexpected item from queue: {type(result)}")

                results_queue.task_done()

            logger.info("All producers finished putting sentinels. Batch queue processing complete.")

        except asyncio.CancelledError:
            logger.info("Batch processing generator (consumer) cancelled. Cancelling producers.")
            for task in producer_tasks:
                if not task.done(): task.cancel()
            await asyncio.gather(*producer_tasks, return_exceptions=True)
            logger.info("Producers cancelled.")
            raise
        except Exception as e:
            logger.exception("An unexpected error occurred in batch processing consumer.")
            for task in producer_tasks:
                if not task.done(): task.cancel()
            await asyncio.gather(*producer_tasks, return_exceptions=True)
            raise
        finally:
            if producer_tasks:
                logger.debug("Awaiting all producer tasks in batch finally block.")
                await asyncio.gather(*producer_tasks, return_exceptions=True)
            logger.info("Finished file_upsert_batch generator.")

    async def stream_file_upsert_batch(
        self,
        metadatas: List[FileMetadata],
        context: Optional[str] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        emb_kwargs: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterator[str]:
        """
        Streams batch file upsert progress using OpenAI-like chat completion chunks.
        Provides overall batch progress updates and individual file status changes.

        Args:
            metadatas (List[FileMetadata]): A list of metadata objects for the files to process.
            context (Optional[str], optional): Additional context for the LLM. Defaults to None.
            flow (Optional[Flow], optional): Processing flow (e.g., FILE). Defaults to settings.flow.
            language (Optional[Language], optional): Language for processing. Defaults to settings.language.
            llm_kwargs (Optional[Dict[str, Any]], optional): Arguments for the LLM. Defaults to None.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder. Defaults to None.

        Yields:
            str: A JSON string representing a progress update, formatted like an OpenAI chat completion chunk.
        """

        total_files = len(metadatas)
        progress = BatchProgress(total_files=total_files)
        logger.info(f"Starting streamed batch file upsert for {total_files} files.")


        # Yield initial 0% progress
        update = await progress.maybe_get_progress_update(with_files=True)
        if update:
            yield update

        if total_files == 0:
            return

        try:
            async for file_state in self.file_upsert_batch(
                metadatas=metadatas,
                context=context,
                flow=flow,
                language=language,
                llm_kwargs=llm_kwargs,
                emb_kwargs=emb_kwargs,
            ):
                await progress.handle_file_state(file_state)
                update = await progress.maybe_get_progress_update()
                if update:
                    yield update

            # Ensure final 100% progress is yielded if not already
            update = await progress.maybe_get_progress_update()
            if update:
                yield update

            # yield final update with file status details
            summary = await progress.get_status_summary()
            yield progress.format_progress_chunk(summary, with_files=True)


        except asyncio.CancelledError:
            logger.warning("Batch processing cancelled.")
            non_terminal_files = await progress.get_non_terminal_file_paths()
            for file_path in non_terminal_files:
                await progress.update_file_status(file_path, 'cancelled')
            update = await progress.maybe_get_progress_update()
            if update:
                yield update

        except Exception as e:
            logger.exception("An error occurred during batch processing.")
            non_terminal_files = await progress.get_non_terminal_file_paths()
            error_msg = str(e)
            for file_path in non_terminal_files:
                await progress.update_file_status(file_path, 'error', error_msg)
            update = await progress.maybe_get_progress_update()
            if update:
                yield update

        finally:
            logger.info("Streamed batch file upsert generator finished.")

    async def search_chunks(
        self,
        query: str,
        filters: Filters,
        context: Optional[str] = None,
        threshold: float = 0.70,
        retry_threshold: Optional[float] = None,
        limit: int = 32,
        char_limit: int = 12000,
        explain: bool = False,
        language: Optional[Language] = None,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        emb_kwargs: Optional[Dict[str, Any]] = None,
    ) -> List[Node]:
        """
        Searches for relevant chunk nodes in the graph database based on a query and filters.

        Args:
            query (str): The search query string.
            filters (Filters): Filter criteria to apply to the search.
            context (Optional[str], optional): Additional context for the search. Defaults to None.
            threshold (float, optional): The similarity threshold for initial search. Defaults to 0.70.
            retry_threshold (Optional[float], optional): A lower threshold to use if the initial search yields no results. Defaults to None.
            limit (int, optional): The maximum number of results to return. Defaults to 32.
            char_limit (int, optional): The maximum total character length of the returned chunk content. Defaults to 12000.
            explain (bool, optional): If True, includes explanation details in the results (if supported by the graph backend). Defaults to False.
            language (Optional[Language], optional): Language for processing. Defaults to settings.language.
            llm_kwargs (Optional[Dict[str, Any]], optional): Arguments for the LLM (not directly used in search, but passed to underlying components if needed). Defaults to None.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder (used to embed the query). Defaults to None.

        Returns:
            List[Node]: A list of relevant chunk nodes found.
        """
        if not query:
            return []
        if not filters:
            raise ValueError("Missing filters.")
        flow = filters._flow
        mtype = get_base_target(BaseMetadata, flow)
        language = language or self.settings.language
        llm_kwargs = llm_kwargs or {}
        emb_kwargs = emb_kwargs or {}
        
        relations = await self.llm.extract_query_relations(query, mtype(**{k: "query" for k in mtype.required_fields()}), context, language, **llm_kwargs)
        await self.embedder.embed_relations(relations, **emb_kwargs)
        relevant_chunks = await self.graph.search_chunks_from_relations(relations, filters, threshold, limit, char_limit, explain)
        if not relevant_chunks and retry_threshold is not None:
            logger.debug(f"No relevant chunks found. Retrying with a lower threshold ({retry_threshold})...")
            relevant_chunks = await self.graph.search_chunks_from_relations(relations, filters, retry_threshold, limit, char_limit, explain)
        
        output_class = get_base_target(BaseNode, flow)
        relevant_chunks = [output_class.from_base(c) for c in relevant_chunks]
        return relevant_chunks

    async def update_nodes(
        self,
        nodes: List[Node],
        return_embeddings: bool = False,
        emb_kwargs: Optional[Dict[str, Any]] = None,
    ) -> List[Node]:
        """
        Updates multiple nodes by their IDs in the graph database.

        Existing properties are preserved when new values are null. Embeddings are
        re-calculated if the node content changes.

        Args:
            nodes (List[Node]): A list of Node objects to update. Must include node_id.
            return_embeddings (bool, optional): If True, return the updated embeddings. Defaults to False.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder. Defaults to None.

        Returns:
            List[Node]: The updated Node objects as retrieved from the database.
        """
        emb_kwargs = emb_kwargs or {}
        if not nodes:
            return []
        flow = nodes[0]._flow
        nodes: List[BaseNode] = [n.to_base(BaseNode(node_type=n.node_type, flow=n.flow)) for n in nodes]
        await self.embedder.embed_nodes(nodes, **emb_kwargs)
        await self.graph.update_nodes_by_ids(nodes, return_embeddings)
        output_class: Node = get_base_target(BaseNode, flow)
        output_nodes = [output_class.from_base(c) for c in nodes]
        
        return output_nodes

    async def recall(
        self,
        messages: List[Message],
        filters: Filters,
        context: Optional[str] = None,
        threshold: Optional[float] = 0.7,
        retry_threshold: Optional[float] = None,
        fallback: Optional[Literal["first", "last"]] = None,
        limit: Optional[int] = 32,
        char_limit: int = 12000,
        explain: Optional[bool] = False,
        language: Optional[Language] = None,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        emb_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Message], List[Node]]:
        """
        Retrieves relevant memories (chunks) based on the user's query within the messages
        and adds them to the messages list, typically modifying the system prompt or user message.

        Args:
            messages (List[Message]): The list of messages, including the user's query.
            filters (Filters): Filter criteria to apply when searching for memories.
            context (Optional[str], optional): Additional context for the LLM during query relation extraction. Defaults to None.
            threshold (Optional[float], optional): The similarity threshold for initial search. Defaults to 0.7.
            retry_threshold (Optional[float], optional): A lower threshold to use if the initial search yields no results. Defaults to None.
            fallback (Optional[Literal["first", "last"]], optional): If no results are found via search, fall back to retrieving the 'first' or 'last' few nodes based on creation/update time. Defaults to None.
            limit (Optional[int], optional): The maximum number of relevant chunks to retrieve via search. Defaults to 32.
            char_limit (int, optional): The maximum total character length of the returned chunk content from search. Defaults to 12000.
            explain (Optional[bool], optional): If True, includes explanation details in search results (if supported). Defaults to False.
            language (Optional[Language], optional): Language for processing. Defaults to settings.language.
            llm_kwargs (Optional[Dict[str, Any]], optional): Arguments for the LLM. Defaults to None.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder. Defaults to None.

        Returns:
            Tuple[List[Message], List[Node]]: A tuple containing the updated list of messages
                                              (with memories added) and the list of relevant
                                              Node objects that were retrieved.
        """
        if not messages:
            return [], []
        if not filters:
            raise ValueError("Missing filters.")
        if fallback not in ["first", "last", None]:
            raise ValueError("Invalid fallback value.")
        flow = filters._flow
        language = language or self.settings.language
        llm_kwargs = llm_kwargs or {}

        self._remove_previous_memories(messages, flow)
        
        # Add RAG prompt if not already present
        if messages and messages[0].role != "system":
            if flow == Flow.FILE:
                prompt = RETRIEVAL_RAG.to_str(flow, language)
            elif flow == flow.CHAT:
                prompt = RETRIEVAL_CHAT.to_str(flow, language)
            else:
                 # Handle other flows if necessary, or raise error
                 prompt = "" # Or a default prompt
                 logger.warning(f"No specific RAG prompt for flow: {flow}")

            if prompt:
                 messages.insert(0, Message(role="system", content=prompt))
        
        query: str = messages_to_user_text(messages)
        chunks = await self.search_chunks(
            query=query,
            filters=filters,
            context=context,
            threshold=threshold,
            retry_threshold=retry_threshold,
            limit=limit,
            char_limit=char_limit,
            explain=explain,
            language=language,
            llm_kwargs=llm_kwargs,
            emb_kwargs=emb_kwargs,
        )

        if not chunks and fallback:
            logger.info(f"Nothing found from similarity search, falling back to: {fallback}, from filters: {filters}")
            chunks = await self.graph.get_nodes(
                filters=filters,
                order_by="created_at" if fallback == "first" else "updated_at",
                order_direction="asc" if fallback == "first" else "desc",
                limit=3
            )

        output_class = get_base_target(BaseNode, flow)
        chunks = [output_class.from_base(c) for c in chunks]
        self._add_new_memories(messages, chunks)
        
        return messages, chunks

    async def chat(
        self,
        messages: List[Message],
        metadata: ChatMetadata,
        filters: ChatFilters,
        context: Optional[str] = None,
        threshold: Optional[float] = 0.70,
        retry_threshold: Optional[float] = 0.60,
        rr_threshold: Optional[float] = 0.95,
        limit: Optional[int] = 32,
        char_limit: int = 12000,
        explain: Optional[bool] = False,
        language: Optional[Language] = None,
        llm_kwargs: Optional[Dict[str, Any]] = None,
        emb_kwargs: Optional[Dict[str, Any]] = None,
        sequential_upsert: bool = False,
    ) -> List[Message]:
        """
        Performs a chat interaction by recalling relevant memories based on the message history
        and filters, adding them to the messages, and optionally upserting the latest message
        as a new memory if classified as a statement.

        Args:
            messages (List[Message]): The list of messages in the conversation history.
            metadata (ChatMetadata): Metadata associated with the chat session.
            filters (ChatFilters): Filter criteria to apply when searching for memories. Must include user_id.
            context (Optional[str], optional): Additional context for the LLM during recall and upsert. Defaults to None.
            threshold (Optional[float], optional): The similarity threshold for initial search during recall. Defaults to 0.70.
            retry_threshold (Optional[float], optional): A lower threshold for search retry during recall. Defaults to 0.60.
            rr_threshold (Optional[float], optional): Similarity threshold for upserting relations. Defaults to 0.95.
            limit (Optional[int], optional): The maximum number of relevant chunks to retrieve during recall. Defaults to 32.
            char_limit (int, optional): The maximum total character length of recalled chunks. Defaults to 12000.
            explain (Optional[bool], optional): If True, includes explanation details in recall search results. Defaults to False.
            language (Optional[Language], optional): Language for processing. Defaults to settings.language.
            llm_kwargs (Optional[Dict[str, Any]], optional): Arguments for the LLM. Defaults to None.
            emb_kwargs (Optional[Dict[str, Any]], optional): Arguments for the embedder. Defaults to None.
            sequential_upsert (bool, optional): If True, the upsert operation (if triggered) will be awaited
                                                before returning. If False, it will be scheduled as a background task.
                                                Defaults to False.

        Returns:
            List[Message]: The updated list of messages with recalled memories added.
        """
        if not messages:
            return []
        if not filters:
            raise ValueError("Missing filters.")
        if not filters.user_id:
            raise ValueError(f"Missing filters.user_id")

        language = language or self.settings.language
        llm_kwargs = llm_kwargs or {}
        emb_kwargs = emb_kwargs or {}

        text = messages_to_user_text(messages)
        await self.recall(
            messages=messages,
            filters=filters,
            context=context,
            threshold=threshold,
            retry_threshold=retry_threshold,
            limit=limit,
            char_limit=char_limit,
            explain=explain,
            language=language,
            llm_kwargs=llm_kwargs,
            emb_kwargs=emb_kwargs
        )

        async def classify_and_upsert(messages, metadata, context, language, llm_kwargs):
            # Use the 'text' variable defined outside this inner function
            msg_type = await self.llm.classify_message(text, context, Flow.CHAT, language, **llm_kwargs)
            if msg_type != MessageClassification.STATEMENT:
                return

            await self.upsert(
                messages=messages,
                metadata=metadata,
                context=context,
                language=language,
                threshold=threshold,
                rr_threshold=rr_threshold,
                llm_kwargs=llm_kwargs,
                emb_kwargs=emb_kwargs,
            )

        # Conditional execution based on the new parameter
        if sequential_upsert:
            # Await the upsert process directly
            await classify_and_upsert(messages, metadata, context, language, llm_kwargs)
        else:
            # Schedule the upsert process asynchronously (original behavior)
            asyncio.create_task(classify_and_upsert(messages, metadata, context, language, llm_kwargs))

        return messages

    async def get_updated_at(
        self,
        filters: Filters,
        return_fields: set[str] = None,
        order_by: Optional[str] = 'updated_at',
        order_direction: Optional[str] = 'desc',
        limit: Optional[int] = 100,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves the latest 'updated_at' timestamp and optionally other fields
        for nodes matching the filters, grouped by the specified return_fields.

        Args:
            filters (Filters): Filter criteria to apply to the query.
            return_fields (set[str], optional): Fields to group by and return along with the latest updated_at. Defaults to None.
            order_by (Optional[str], optional): Property to order results by. Defaults to 'updated_at'.
            order_direction (Optional[str], optional): Direction of ordering, "asc" or "desc". Defaults to 'desc'.
            limit (Optional[int], optional): Maximum number of results to return. Defaults to 100.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing the requested
                                  return_fields and the latest 'updated_at' for that group.
        """
        if not filters:
            raise ValueError("Missing filters.")

        results = await self.graph.get_updated_at(
            filters=filters,
            return_fields=return_fields,
            order_by=order_by,
            order_direction=order_direction,
            limit=limit,
        )

        return results
    
    async def get_nodes_by_ids(
        self,
        node_ids: List[str],
        node_type: NodeType = NodeType.CHUNK,
        return_fields: set[str] = None,
    ) -> List[Node]:
        """
        Retrieves multiple nodes by their unique IDs from the graph database.

        Args:
            node_ids (List[str]): A list of node IDs to retrieve.
            node_type (NodeType, optional): The type of node to retrieve. Defaults to NodeType.CHUNK.
            return_fields (set[str], optional): Specific fields to return for each node. Defaults to None (return all).

        Returns:
            List[Node]: A list of the retrieved Node objects. Returns an empty list if no nodes are found or node_ids is empty.
        """
        if not node_ids:
            return []

        # Delegate the call to the underlying graph instance (neo4j.py)
        base_nodes = await self.graph.get_nodes_by_ids(
            node_ids=node_ids,
            node_type=node_type,
            return_fields=return_fields,
        )

        # Convert BaseNode list to Node list
        nodes: List[Node] = []
        for base_node in base_nodes:
            # Get the target Node class based on the flow
            output_class: Node = get_base_target(BaseNode, base_node.flow)
            # Convert the BaseNode to the target Node class
            nodes.append(output_class.from_base(base_node))

        return nodes

    async def delete_nodes_by_ids(
        self,
        node_ids: List[str],
        node_type: NodeType = NodeType.CHUNK,
        return_fields: set[str] = None,
        cleanup: bool = True,
    ) -> List[Node]:
        """
        Deletes multiple nodes by their unique IDs from the graph database.

        Args:
            node_ids (List[str]): A list of node IDs to delete.
            node_type (NodeType, optional): The type of node to delete. Defaults to NodeType.CHUNK.
            return_fields (set[str], optional): Specific fields of the deleted nodes to return. Defaults to None (return all).
            cleanup (bool, optional): If True, performs cleanup operations for orphaned nodes/relations after deletion. Defaults to True.

        Returns:
            List[Node]: A list of the deleted Node objects. Returns an empty list if no nodes are found or node_ids is empty.
        """
        if not node_ids:
            return []

        # Call the underlying graph function (retry is handled there)
        deleted_base_nodes: List[BaseNode] = await self.graph.delete_nodes_by_ids(
            node_ids=node_ids,
            node_type=node_type,
            return_fields=return_fields,
            cleanup=cleanup,
        )

        # Convert BaseNode list to Node list
        deleted_nodes: List[Node] = []
        for base_node in deleted_base_nodes:
            # Get the target Node class based on the flow
            output_class: Node = get_base_target(BaseNode, base_node.flow)
            # Convert the BaseNode to the target Node class
            deleted_nodes.append(output_class.from_base(base_node))

        return deleted_nodes

    async def get_nodes(
        self,
        filters: Filters,
        node_type: NodeType = NodeType.CHUNK,
        return_fields: set[str] = None,
        order_by: str = 'updated_at',
        order_direction: str = 'desc',
        limit: int = 100,
    ) -> List[Node]:
        """
        Retrieves nodes from the graph database based on filters, with optional ordering and limiting.

        Args:
            filters (Filters): Filter criteria to apply to the query (required).
            node_type (NodeType, optional): The type of node to retrieve. Defaults to NodeType.CHUNK.
            return_fields (set[str], optional): Specific fields to return for each node. Defaults to None (return all).
            order_by (str, optional): Property to order results by. Defaults to 'updated_at'.
            order_direction (str, optional): Direction of ordering, "asc" or "desc". Defaults to "desc".
            limit (int, optional): Maximum number of nodes to return. Defaults to 100.

        Returns:
            List[Node]: A list of the retrieved Node objects. Returns an empty list if no nodes are found or filters are empty.
        """
        if not filters:
            raise ValueError("Missing filters.")

        base_nodes = await self.graph.get_nodes(
            filters=filters,
            node_type=node_type,
            return_fields=return_fields,
            order_by=order_by,
            order_direction=order_direction,
            limit=limit,
        )

        nodes: List[Node] = []
        for base_node in base_nodes:
            output_class: Node = get_base_target(BaseNode, base_node.flow)
            nodes.append(output_class.from_base(base_node))

        return nodes

    async def delete_nodes(
        self,
        filters: Filters,
        node_type: NodeType = NodeType.CHUNK,
        return_fields: set[str] = None,
        cleanup: bool = True,
    ) -> List[Node]:
        """
        Deletes nodes from the graph database based on filters.

        Args:
            filters (Filters): Filter criteria to apply to the query (required).
            node_type (NodeType, optional): The type of node to delete. Defaults to NodeType.CHUNK.
            return_fields (set[str], optional): Specific fields of the deleted nodes to return. Defaults to None (return all).
            cleanup (bool, optional): If True, performs cleanup operations for orphaned nodes/relations after deletion. Defaults to True.

        Returns:
            List[Node]: A list of the deleted Node objects. Returns an empty list if no nodes are found or filters are empty.
        """
        if not filters:
            raise ValueError(f"Missing filters.")

        # Call the underlying graph function (retry is handled there)
        deleted_base_nodes: List[BaseNode] = await self.graph.delete_nodes(
            filters=filters,
            node_type=node_type,
            return_fields=return_fields,
            cleanup=cleanup,
        )

        # Convert BaseNode list to Node list
        deleted_nodes: List[Node] = []
        for base_node in deleted_base_nodes:
            # Get the target Node class based on the flow
            output_class: Node = get_base_target(BaseNode, base_node.flow)
            # Convert the BaseNode to the target Node class
            deleted_nodes.append(output_class.from_base(base_node))

        return deleted_nodes

    def _remove_previous_memories(
        self, 
        messages: List[Message],
        flow: Optional[Flow] = None,
    ):
        """
        Internal helper to remove previously added memory sections from message content
        to avoid duplication during recall.

        Args:
            messages (List[Message]): The list of messages.
            flow (Optional[Flow], optional): The processing flow to determine the format. Defaults to None.
        """
        if flow == Flow.CHAT:
            msg = next((msg for msg in messages if msg.role == "system"), None)
            if not msg:
                return
            # Remove the [MEMORIES]...[/MEMORIES] block and restore the original [PROMPT]
            pattern = r"\[PROMPT\](.*?)\[/PROMPT\]\n\[MEMORIES\].*?\[/MEMORIES\]"
            match = re.search(pattern, msg.content, re.DOTALL)
            if match:
                msg.content = match.group(1).strip() # Restore just the prompt content
        elif flow == Flow.FILE:
            msg = next((msg for msg in reversed(messages) if msg.role == "user"), None)
            if not msg:
                return
            # Remove the [INPUT]...[/INPUT] block and restore the original <query>
            pattern = r"\[INPUT\].*?<query>(.*?)</query>.*?\[/INPUT\]"
            match = re.search(pattern, msg.content, re.DOTALL)
            if match:
                msg.content = match.group(1).strip() # Restore just the query content
        else:
            logger.warning(f"Unsupported flow for _remove_previous_memories: {flow}")

    def _add_new_memories(
        self,
        messages: List[Message],
        relevant_memories: List[Node],
    ):
        """
        Internal helper to add relevant memories (chunks) to the message content,
        formatting them according to the specified flow.

        Args:
            messages (List[Message]): The list of messages to modify.
            relevant_memories (List[Node]): The list of relevant Node objects (chunks) to add.
        """
        if not relevant_memories:
            return
        
        # Determine flow from the first memory node
        flow = relevant_memories[0]._flow

        if flow == Flow.CHAT:
            # Find the system message to append memories
            msg = next((msg for msg in messages if msg.role == "system"), None)
            if not msg:
                logger.warning("No system message found to add chat memories.")
                return
            
            # Format memories for chat
            memories_text = "\n\n-----\n\n".join(str(chunk) for chunk in relevant_memories)
            
            # Wrap existing content and add memories
            # Ensure existing content is within [PROMPT] tags if not already
            if not msg.content.strip().startswith("[PROMPT]"):
                 msg.content = f"[PROMPT]\n{msg.content}\n[/PROMPT]"

            msg.content = f"{msg.content}\n[MEMORIES]\n{memories_text}\n[/MEMORIES]"

        elif flow == Flow.FILE:
            # Find the last user message to append memories
            msg = next((msg for msg in reversed(messages) if msg.role == "user"), None)
            if not msg:
                logger.warning("No user message found to add file memories.")
                return
            
            # Format memories for file RAG
            memories_text = "\n\n".join(f'<source id="{i+1}">\n{chunk.content}\n</source>' for i, chunk in enumerate(relevant_memories))
            
            # Wrap existing content and add memories
            # Ensure existing content is within <query> tags if not already
            if not msg.content.strip().startswith("<query>"):
                 msg.content = f"<query>\n{msg.content}\n</query>"

            msg.content = f"[INPUT]\n\n{msg.content}\n\n{memories_text}\n\n[/INPUT]\n[OUTPUT]"

        else:
            logger.warning(f"Unsupported flow for _add_new_memories: {flow}")
            return

        logger.debug(f"message with memories:\n{msg}")
    
    async def close(self):
        """
        Closes the connections to underlying components, such as the graph database.
        """
        await self.graph.close()