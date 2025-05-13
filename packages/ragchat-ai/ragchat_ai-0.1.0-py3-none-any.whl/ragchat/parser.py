import re
from rapidfuzz import process, fuzz
from ragchat.log import get_logger
from typing import List, Optional, Any, Dict, Iterable, Union, Tuple
from pydantic_settings import BaseSettings, SettingsConfigDict
from ragchat.definitions import NodeType, BaseNode, BaseNode, Relation, Metadata, Message
from ragchat.utils import get_unique


logger = get_logger(__name__)

class ParserSettings(BaseSettings):
    score_cutoff: int = 80
    chunk_char_size: int = 2000
    max_chars_topic: int = 99
    max_chars_fact: int = 256
    max_chars_entity: int = 99

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="PARSER_")


settings = ParserSettings()

def _split_name_descriptor(s: str) -> Tuple[str, Optional[str]]:
    """Splits a string into a name and an optional descriptor in parentheses."""
    # match name and first parenthetical expression
    matches = re.match(r'([^(]+)\s*\((.*?)\).*$', s)
    if matches:
        name = matches.group(1).strip()
        descriptor = matches.group(2).strip()

        # Handle edge case where name might be numeric and descriptor might be the actual name
        if name[:1].isdigit() or (name.startswith('-') and name[1:2].isdigit()):
            _ = name
            name = descriptor
            descriptor = _

        return name, descriptor

    # If there are no parentheses or any other invalid format,
    # treat the entire string as the name with no descriptor
    return s, None

def str_to_node(item: str, node_type: NodeType, metadata: Metadata) -> BaseNode:
    """Factory function to create a BaseNode from a string and metadata."""
    item = item.strip()
    # Use the static method from BaseNode for parsing
    name, descriptor = _split_name_descriptor(item)
    # Reserved names check (common)
    reserved_names = ["topic", "topics", "entity", "entities", "fact", "facts", "chunk", "chunks"] # en
    reserved_names += ["tema", "temas", "entidad", "entidades", "hecho", "hechos", "parte", "partes"] # es
    reserved_names += ["sujet", "sujets", "entité", "entités", "fait", "faits", "partie", "parties"] # fr
    reserved_names += ["Thema", "Themen", "Entität", "Entitäten", "Fakt", "Fakten", "Teil", "Teile"] # de

    if name.lower() in reserved_names:
        raise ValueError(f"The name cannot be '{name}'. It is a reserved word.")

    # Entity format check (specific to ENTITY node_type, but done during parsing)
    content = None
    if node_type == NodeType.ENTITY:
        if descriptor is None:
            raise ValueError(
                f"Invalid entity format: '{item}' "
                "Each entity should be listed separately with a single name and a single type: `name (type)`"
            )
        content = f"{name} ({descriptor})"

    common_args = {
        'node_type': node_type,
        'flow': metadata._flow,
        'content': content or item,
        'descriptor': descriptor,
    }

    node = metadata.to_base(BaseNode(**common_args))

    return node

def header_items_to_markdown(header: str, items: List[Any], header_level: str = '##', bullet_char: str = '-') -> str:
    """
    Convert a list of items into markdown format with the given header.
    """
    markdown = f"{header_level} {header}\n"
    markdown += "\n".join([f"{bullet_char} {item}" for item in items])
    return markdown

def markdown_to_heading_items(
    markdown: str,
    item_type: Optional[NodeType] = None,
    heading_type: Optional[NodeType] = None,
    match_headings: Optional[List[str]] = None,
    headings_pool: Optional[List[str]] = None,
    match_items: Optional[List[str]] = None,
    items_pool: Optional[List[str]] = None,
    mutually_exclusive: bool = False,
    exclude_nones: bool = True,
    score_cutoff: int = settings.score_cutoff
) -> Dict[str, List[str]]:
    """
    Parse markdown text to extract list items organized by headings,
    with optional fuzzy validation against pools or exact (fuzzy) matching sets.

    Expected format:
    ```
    ## Heading
    - Item
    - Item
    ## Heading
    - Item
    - Item
    ```

    Args:
        markdown: The markdown text to parse.
        item_type: Optional NodeType to apply character limits to items.
        heading_type: Optional NodeType to apply character limits to headings.
        match_headings: If provided, checks if parsed headings fuzzily match this exact set.
        headings_pool: If provided, checks if all parsed headings have a fuzzy match in this pool.
        match_items: If provided, checks if parsed items fuzzily match this exact set.
        items_pool: If provided, checks if all parsed items have a fuzzy match in this pool.
        mutually_exclusive: If True, checks if items are unique across all headings.
        exclude_nones: If True, removes items that are 'none' (case-insensitive) and empty headings.
        score_cutoff: The minimum similarity ratio (0-100) for fuzzy matching.

    Returns:
        A dictionary mapping headings to lists of unique items.
        Returns empty dict if no headings are found.

    Raises:
        ValueError: If any validation fails or character limits are exceeded.
    """
    # Parse markdown list items with all bullet types (-, *, +)
    lines = markdown.split('\n')
    list_item_pattern = re.compile(r'^\s*[-*+]\s+(.*?)$')
    heading_pattern = re.compile(r'^(#{1,6})\s+(.*?)$')

    max_chars = {
        NodeType.TOPIC: settings.max_chars_topic,
        NodeType.FACT: settings.max_chars_fact,
        NodeType.ENTITY: settings.max_chars_entity,
    }

    result: Dict[str, List[str]] = {}
    current_heading: Optional[str] = None

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
             continue

        # Check if line is a heading
        heading_match = heading_pattern.match(line)
        if heading_match:
            current_heading = ' '.join(heading_match.group(2).strip().split())

            if heading_type and max_chars.get(heading_type) is not None and max_chars[heading_type] < len(current_heading):
                logger.warning(f"Line exceeding {max_chars[heading_type]} characters: {line[:max_chars[heading_type]]}...")
                raise ValueError(f"Be concise!")

            if current_heading not in result:
                result[current_heading] = []
            continue

        # Check if line is a list item *under the current heading*
        if current_heading and current_heading.lower() != 'none':
            match = list_item_pattern.match(line)
            if match:
                # Use stripped item, handle potential multiple spaces
                item = ' '.join(match.group(1).strip().split())

                if item_type and max_chars.get(item_type) is not None and max_chars[item_type] < len(item):
                    logger.warning(f"Item exceeding {max_chars[item_type]} characters: {item[:max_chars[item_type]]}...")
                    raise ValueError(f"Be concise!")

                # Add only if non-empty and not already present for this heading
                if item and item not in result[current_heading]:
                    result[current_heading].append(item)


    # --- Validation Section ---
    parsed_headings: List[str] = list(result.keys())
    parsed_items: List[str] = get_unique(result.values())

    # Helper for fuzzy check within a pool
    def check_pool(items_to_check: List[str], pool: List[str], item_type: str):
        if not pool: # If pool is empty, any item found is invalid
            if items_to_check:
                raise ValueError(f"Found {item_type}s {items_to_check} but {item_type} pool is empty.")
            return # Pool and items are both empty, valid state

        invalid_items = set()
        for item in items_to_check:
            match = process.extractOne(item, pool, scorer=fuzz.ratio, score_cutoff=score_cutoff)
            if match is None:
                invalid_items.add(item)
        if invalid_items:
            logger.debug(
                f"Found {item_type}s not in the allowed pool: "
                f"{list(invalid_items)}. Pool: {pool}"
            )
            raise ValueError(f"Select only from the allowed {item_type}s: {pool}.")

    # Helper for fuzzy set comparison (two-way check)
    def check_match(parsed: List[str], expected: List[str], item_type: str):
        # Check 1: Every parsed item must have a match in expected
        unmatched_parsed = []
        if expected: # Only check if expected list is not empty
            for item in parsed:
                match = process.extractOne(item, expected, scorer=fuzz.ratio, score_cutoff=score_cutoff)
                if match is None:
                    unmatched_parsed.append(item)
        elif parsed: # Expected is empty, but parsed is not
             unmatched_parsed = parsed

        if unmatched_parsed:
            logger.debug(
                f"Found unexpected {item_type}s: "
                f"Found {unmatched_parsed}. Expected: {expected}"
            )
            raise ValueError(f"Adhere strictly to {item_type}s: {expected}")

        # Check 2: Every expected item must have a match in parsed
        unmatched_expected = []
        if parsed: # Only check if parsed list is not empty
            for item in expected:
                match = process.extractOne(item, parsed, scorer=fuzz.ratio, score_cutoff=score_cutoff)
                if match is None:
                    unmatched_expected.append(item)
        elif expected: # Parsed is empty, but expected is not
            unmatched_expected = expected

        if unmatched_expected:
            logger.debug(
                f"Missing {item_type}s: "
                f"Found: {parsed}. Missing {unmatched_expected}"
            )
            raise ValueError(f"Adhere strictly to {item_type}s: {expected}")

    # Apply Validators
    if headings_pool is not None:
        check_pool(parsed_headings, headings_pool, "heading")

    if items_pool is not None:
        check_pool(parsed_items, items_pool, "item")

    if match_headings is not None:
        check_match(parsed_headings, match_headings, "heading")

    if match_items is not None:
        check_match(parsed_items, match_items, "item")

    if mutually_exclusive:
        # This check remains exact - fuzzy doesn't make sense here
        all_items = [item for items in result.values() for item in items]
        if len(set(all_items)) != len(all_items):
            # Find duplicates for a more informative error message
            counts = {}
            duplicates = set()
            for item in all_items:
                counts[item] = counts.get(item, 0) + 1
                if counts[item] > 1:
                    duplicates.add(item)
            logger.debug(f"Items are not mutually exclusive across headings. Duplicates found: {list(duplicates)}")
            raise ValueError("Items cannot repeat across headings.")

    # --- Cleanup Section ---
    if exclude_nones:
        cleaned_result = {}
        for k, v in result.items():
            # Filter out 'none' (case-insensitive) and potential empty strings after stripping
            filtered_items = [item for item in v if item and item.lower() != 'none']
            if filtered_items: # Only keep heading if it has non-none items
                cleaned_result[k] = filtered_items
        result = cleaned_result

    return result

def markdown_to_nodes(
    markdown: str,
    metadata: Metadata,
    node_type: NodeType = None,
    heading_type: Optional[NodeType] = None,
    match_headings: Iterable[str] = None,
    headings_pool: Iterable[str] = None,
    match_items: Iterable[str] = None,
    items_pool: Iterable[str] = None,
    mutually_exclusive = False,
    exclude_nones = True,
    score_cutoff: int = settings.score_cutoff
) -> Dict[str, List[BaseNode]]:
    """
    Parse markdown text into a dictionary mapping headings to lists of BaseNode objects.

    Uses `markdown_to_heading_items` for parsing and validation, then converts
    the extracted items into BaseNode objects using `str_to_node`.

    Args:
        markdown: The markdown text to parse.
        metadata: Metadata to associate with the created nodes.
        node_type: The NodeType to assign to the created item nodes.
        heading_type: Optional NodeType to apply character limits to headings.
        match_headings: If provided, checks if parsed headings fuzzily match this exact set.
        headings_pool: If provided, checks if all parsed headings have a fuzzy match in this pool.
        match_items: If provided, checks if parsed items fuzzily match this exact set.
        items_pool: If provided, checks if all parsed items have a fuzzy match in this pool.
        mutually_exclusive: If True, checks if items are unique across all headings.
        exclude_nones: If True, removes items that are 'none' (case-insensitive) and empty headings.
        score_cutoff: The minimum similarity ratio (0-100) for fuzzy matching.

    Returns:
        A dictionary mapping headings (strings) to lists of BaseNode objects.
        Returns empty dict if no headings are found or after filtering.

    Raises:
        ValueError: If any validation fails during parsing or node creation.
    """
    heading_items = markdown_to_heading_items(
        markdown,
        node_type,
        heading_type,
        match_headings,
        headings_pool,
        match_items,
        items_pool,
        mutually_exclusive,
        exclude_nones,
        score_cutoff,
        )

    # Convert items (strings) to BaseNode objects
    nodes_dict: Dict[str, List[BaseNode]] = {}
    for heading, items in heading_items.items():
        nodes_dict[heading] = [str_to_node(item, node_type, metadata) for item in items]

    return nodes_dict

def markdown_to_relations(
    markdown: str,
    metadata: Metadata,
    text: str,
    score_cutoff: int = settings.score_cutoff
) -> List[Relation]:
    """
    Parse hierarchical markdown into a list of Relation objects.

    Expected format:
    ```
    # Topics
    - Topic
    - Topic

    ## Fact
    - Entity (descriptor)
    - Entity (descriptor)
    ## Fact
    - Entity (descriptor)
    ```

    Args:
        markdown: The markdown text to parse.
        metadata: Metadata to associate with the created nodes and relations.
        text: Original text chunk from which the markdown was generated. Used to create the Chunk node.
        score_cutoff: The minimum similarity ratio (0-100) for fuzzy matching during internal parsing.

    Returns:
        A list of Relation objects. Each relation links a Fact node to the Chunk node,
        associated Topic nodes, and associated Entity nodes.

    Raises:
        ValueError: If parsing fails, required sections are missing, or validation fails.
    """
    # Remove code block markers if present
    try:
        # Split into topics section and fact/entities sections
        t, f = re.split(r'(?=##)', markdown, maxsplit=1)
    except:
        raise ValueError("There must be at least one fact with format `## [fact]` and corresponding entities below it.")

    # Parse the markdown to get all headings and items
    # Topics are under #, items are topics
    topics_dict = markdown_to_nodes(
        markdown=t,
        metadata=metadata,
        node_type=NodeType.TOPIC,
        exclude_nones=True,
        score_cutoff=score_cutoff,
    )

    # Facts are ## headings, items are entities
    fact_entities_dict = markdown_to_nodes(
        markdown=f,
        metadata=metadata,
        node_type=NodeType.ENTITY, # Items are Entities
        heading_type=NodeType.FACT, # Headings are Facts
        exclude_nones=True,
        score_cutoff=score_cutoff,
    )

    # Validate that we have at least one main topic
    all_topics: List[BaseNode] = get_unique(topics_dict.values())
    if not all_topics:
        logger.warning(f"No topics found in markdown:\n{markdown}\n\nTopics section parsed:\n{t}")
        raise ValueError("Topics should be listed under '# Topics'")

    # Validate that we have at least one fact
    if not fact_entities_dict:
        logger.warning(f"No fact_entities found in markdown:\n{markdown}\n\nFacts section parsed:\n{f}")
        raise ValueError("There must be at least one fact with format `## [fact]` and corresponding entities below it.")

    # Create the Chunk node
    chunk = str_to_node(text, NodeType.CHUNK, metadata)

    # Create Relations
    relations: List[Relation] = []
    for fact_str, entity_nodes in fact_entities_dict.items():
        fact_node = str_to_node(fact_str, NodeType.FACT, metadata)

        # Find which topics are associated with this fact.
        # This assumes the structure implies all facts relate to all topics listed.
        # If a more complex topic-fact mapping is needed, this logic would change.
        # For now, all facts are related to all parsed topics.
        related_topics = all_topics

        relations.append(
            Relation(
                fact=fact_node,
                chunk=chunk,
                topics=related_topics,
                entities=entity_nodes
            )
        )

    return relations

def _find_split(window: str, delimiters: list[str], min_window_size: int) -> int:
    """Find an appropriate split point in a text window based on delimiters."""
    window_size = len(window)
    # Try each delimiter in order of priority
    for delimiter in delimiters:
        idx = window.rfind(delimiter)
        if min_window_size < idx:
            window_size = idx
            break
    # If no suitable split point is found, use the original chunk size
    return window_size

def chunk_text(text: str, chunk_char_size=None) -> List[str]:
    """Split text into chunks, respecting code blocks and paragraphs."""
    chunks = []
    start = 0
    text_length = len(text)
    chunk_char_size = chunk_char_size or settings.chunk_char_size
    while start < text_length:
        end = start + chunk_char_size
        if text_length < end:
            chunks.append(text[start:])
            break

        current_window = text[start:end]
        delimiters = ['\n# ', '\n## ', '\n### ', '\n\n\n\n', '\n\n\n', '\n\n', '\n', '. ', ' ']
        end = start + _find_split(current_window, delimiters, chunk_char_size*0.5)

        chunk = text[start:end]
        if chunk:
            if 0 < len(chunks) and (len(chunks[-1]) + len(chunk)) < chunk_char_size:
                chunks[-1] += chunk
            else:
                chunks.append(chunk)
        start = end

    return chunks

def get_most_common_item(items: Iterable[str], similarity_threshold: float = 90) -> Optional[str]:
    """
    Find the most frequently occurring string in the provided iterable
    using fuzzy string matching with rapidfuzz

    Args:
        items: An iterable of strings to analyze
        similarity_threshold: Threshold percentage for considering strings as similar (default: 90)

    Returns:
        The most common string or None if the input is empty
    """
    if not items:
        return None

    # Convert to list if it's not already
    items_list: List[str] = list(items)

    if not items_list:
        return None

    # Group similar solutions
    groups: List[str] = []
    group_counts: List[int] = []

    for item in items_list:
        # Check if this item is similar to any existing group
        best_match: Optional[str] = None
        best_score: float = 0
        best_idx: int = -1

        for idx, group in enumerate(groups):
            # Compare with the representative of each group
            score: float = fuzz.ratio(item.lower(), group.lower())
            if score > similarity_threshold and score > best_score:
                best_score = score
                best_match = group
                best_idx = idx

        if best_match:
            # Add to existing group
            group_counts[best_idx] += 1
        else:
            # Create new group
            groups.append(item)
            group_counts.append(1)

    # Find the group with the highest count
    if not groups:
        return None

    max_idx: int = group_counts.index(max(group_counts))
    return groups[max_idx]

def get_top_k_common_items(items: Iterable[str], k: int = 3, similarity_threshold: float = 90) -> List[str]:
    """
    Find the top k most frequently occurring strings in the provided iterable
    using fuzzy string matching with rapidfuzz

    Args:
        items: An iterable of strings to analyze
        k: Number of top items to return (default: 3)
        similarity_threshold: Threshold percentage for considering strings as similar (default: 90)

    Returns:
        A list containing the top k most common strings, sorted by frequency in descending order.
        Returns an empty list if the input is empty.
    """
    if not items:
        return []

    # Convert to list if it's not already
    items_list: List[str] = list(items)

    if not items_list:
        return []

    # Group similar items
    groups: List[str] = []
    group_counts: List[int] = []

    for item in items_list:
        # Check if this item is similar to any existing group
        best_match: Optional[str] = None
        best_score: float = 0
        best_idx: int = -1

        for idx, group in enumerate(groups):
            # Compare with the representative of each group
            score: float = fuzz.ratio(item.lower(), group.lower())
            if score > similarity_threshold and score > best_score:
                best_score = score
                best_match = group
                best_idx = idx

        if best_match:
            # Add to existing group
            group_counts[best_idx] += 1
        else:
            # Create new group
            groups.append(item)
            group_counts.append(1)

    # Create list of (group, count) tuples and sort by count
    result_tuples = sorted(zip(groups, group_counts), key=lambda x: x[1], reverse=True)

    # Extract just the strings, maintaining the sorted order
    result_strings = [group for group, _ in result_tuples]

    # Return top k results (or all if fewer than k)
    return result_strings[:min(k, len(result_strings))]

def dicts_to_relations(chunk: str, topic_facts: Dict[str, List[str]], fact_entities: Dict[str, List[BaseNode | BaseNode]], metadata: Metadata) -> List[Relation]:
    """
    Converts dictionaries representing topic-fact and fact-entity relationships into a list of Relation objects.

    Matches facts from the topic-fact dictionary to facts (keys) in the fact-entities dictionary
    using exact match first, then fuzzy fallback. Creates Relation objects linking the chunk,
    fact, associated topics, and associated entities.

    Args:
        chunk: The original text chunk string.
        topic_facts: A dictionary mapping topic strings to lists of fact strings.
        fact_entities: A dictionary mapping fact strings to lists of BaseNode entity objects.
        metadata: Metadata to associate with the created nodes and relations.

    Returns:
        A list of Relation objects.

    Raises:
        ValueError: If a fact from topic_facts cannot be matched (exactly or fuzzily)
                    to a fact key in fact_entities.
    """
    if not topic_facts or not fact_entities:
        return []

    relations: List[Relation] = []
    chunk_node = str_to_node(chunk, NodeType.CHUNK, metadata)

    # Create a mapping from fact string to a list of topic strings
    fact_to_topic_strings: Dict[str, List[str]] = {}
    for topic_str, fact_strs in topic_facts.items():
        for fact_str in fact_strs:
            if fact_str not in fact_to_topic_strings:
                fact_to_topic_strings[fact_str] = []
            fact_to_topic_strings[fact_str].append(topic_str)

    # Iterate through the facts found in the topic-fact mapping
    for fact_str, topic_strs in fact_to_topic_strings.items():
        fact_node = str_to_node(fact_str, NodeType.FACT, metadata)
        topic_nodes = [str_to_node(s, NodeType.TOPIC, metadata) for s in topic_strs]
        entity_nodes: Optional[List[BaseNode]] = None

        # 1. Try exact match for the fact string in fact_entities keys
        if fact_str in fact_entities:
            entity_nodes = fact_entities[fact_str]
        else:
            # 2. Fallback to fuzzy match if exact match failed
            best_match = process.extractOne(
                fact_str,
                fact_entities.keys(),
                scorer=fuzz.ratio,
                score_cutoff=settings.score_cutoff
            )
            if best_match:
                entity_nodes = fact_entities[best_match[0]]

        if entity_nodes is None:
            # This fact from topic_facts didn't match any fact in fact_entities
            raise ValueError(f"Fact '{fact_str}' found in topics but not matched in fact-entities.")

        # Create relation
        relations.append(Relation(chunk=chunk_node, fact=fact_node, topics=topic_nodes, entities=entity_nodes))

    return relations

def dicts_to_messages(messages: List[Dict[str, Any] | Message]) -> List[Message]:
    """
    Converts a list containing dictionaries and/or Message objects into a list of Message objects.

    Args:
        messages: A list where each element is either a dictionary representing a message
                  or an existing Message object.

    Returns:
        A list of Message objects.

    Raises:
        ValueError: If an element in the input list is neither a dict nor a Message object.
    """
    if not messages:
        return []

    new_messages = []
    for msg in messages:
        if isinstance(msg, Message):
            new_messages.append(msg)
        elif isinstance(msg, dict):
            new_messages.append(Message(**msg))
        else:
            raise ValueError(f"Cannot convert message of type {type(msg)} to Message")
    return new_messages

def messages_to_dicts(messages: List[Message | Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts a list containing Message objects and/or dictionaries into a list of dictionaries.

    Args:
        messages: A list where each element is either a Message object or an existing dictionary.

    Returns:
        A list of dictionaries, where each dictionary represents a message.

    Raises:
        ValueError: If an element in the input list is neither a Message object nor a dict.
    """
    if not messages:
        return []

    new_dicts = []
    for msg in messages:
        if isinstance(msg, dict):
            new_dicts.append(msg)
        elif isinstance(msg, Message):
            new_dicts.append(msg.model_dump(mode='json', exclude_none=True))
        else:
            raise ValueError(f"Cannot convert message of type {type(msg)} to dict")
    return new_dicts

def messages_to_user_text(
    messages: List[Message],
    limit: int = 3,
) -> str:
    """Create a string from the last three user messages."""
    s = "\n\n".join(
        [f"{m.role}: {m.content}" for m in messages if m.role == "user"][-limit:]
    )

    return s
