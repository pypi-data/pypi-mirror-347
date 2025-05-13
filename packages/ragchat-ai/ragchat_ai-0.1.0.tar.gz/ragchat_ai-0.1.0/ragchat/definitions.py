import re
import hashlib
import traceback
from typing import Literal, ClassVar, List, Optional, Any, Annotated, Dict, Set, Tuple, NamedTuple, Type, TypeVar
from typing_extensions import Self
from dataclasses import dataclass, fields
from litellm import Message
from pydantic import BaseModel, create_model, model_validator, ConfigDict, Field, field_validator, ValidationError, TypeAdapter, PrivateAttr
from pydantic_core import PydanticUndefined
from enum import Enum
from logging import getLogger
logger = getLogger(__name__)



####################################
# --- Flows & General ---
####################################

class classproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        if cls is None:
            cls = type(instance)
        return self.func(cls)

class Flow(Enum):
    FILE = "file"
    CHAT = "chat"
    def __str__(self):
        return self.value

class MessageClassification(Enum):
    """Enum representing the possible types of messages."""
    STATEMENT = "statement"
    QUESTION = "question"
    MIXED = "mixed"
    NONE = "none"
    def __str__(self):
        return self.value

T = TypeVar("T", bound=BaseModel)

class _mappedFields(BaseModel):
    @model_validator(mode='after')
    def at_least_one(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be set.")
        return self

    def to_base(self, base: T, exclude_none: bool = True) -> T:
        """
        Maps fields from this model instance to a provided base model instance.

        Mapping rules:
        - Fields defined in this model map to base model fields with the same name.
        - Fields in this model's model_extra map to entries in base.custom with the same key.
        - If a standard field from this model doesn't match a standard base field and base has no 'custom' attribute,
        it is ignored and a warning is logged.
        - If an extra field from this model is present and base has no 'custom' attribute,
        it is ignored and a warning is logged.
        - None values are excluded if exclude_none is True.
        """
        if base is None:
            raise TypeError("The 'base' parameter cannot be None.")

        base_keys: Set[str] = set(base.model_fields.keys())
        target_base_name: str = base.__class__.__name__

        # --- Handle base.custom initialization/validation upfront ---
        base_custom_dict: Optional[Dict[str, Any]] = None
        if hasattr(base, 'custom'):
            base_custom_value = getattr(base, 'custom')
            if isinstance(base_custom_value, dict):
                base_custom_dict = base_custom_value
            else:
                # It exists but isn't a dict (or is None). Initialize it.
                if base_custom_value is not None:
                    logger.warning(
                        f"base.custom ({type(base_custom_value)}) is not a dictionary on {target_base_name}, "
                        f"overwriting with empty dict for mapping."
                    )
                setattr(base, 'custom', {})
                # Get the reference to the newly created dictionary
                base_custom_dict = getattr(base, 'custom')
        # If base does not have 'custom', base_custom_dict remains None.
        # -------------------------------------------------------------

        # 1. Map standard fields from self to base
        for model_key in self.model_fields.keys():
            value = getattr(self, model_key)

            if exclude_none and value is None:
                continue

            if model_key in base_keys:
                # Rule: Map to base field with the same name
                setattr(base, model_key, value)
            elif base_custom_dict is not None:
                # Rule: If no standard field match, map to base.custom (if available)
                base_custom_dict[model_key] = value
            else:
                # Log warning if field cannot be mapped anywhere
                logger.warning(
                    f"Standard field '{model_key}' from {self.__class__.__name__} cannot be mapped to {target_base_name}. "
                    f"No matching standard field found and {target_base_name} does not have a 'custom' attribute."
                )

        # 2. Map extra fields from self.model_extra to base.custom
        if self.model_extra: # Check if model_extra is not None or empty
            for extra_key, extra_value in self.model_extra.items():
                if exclude_none and extra_value is None:
                    continue

                if base_custom_dict is not None:
                    # Rule: Map extra fields ONLY to base.custom (if available)
                    base_custom_dict[extra_key] = extra_value
                else:
                    # Log warning if extra field cannot be mapped
                    logger.warning(
                        f"Extra field '{extra_key}' from {self.__class__.__name__} cannot be mapped to {target_base_name}. "
                        f"{target_base_name} does not have a 'custom' attribute."
                    )

        if type(base) == BaseNode:
            base._update_hash()
        
        return base

    @classmethod
    def from_base(cls: Type[T], base: BaseModel, exclude_none: bool = True) -> T:
        """
        Maps fields from a base model instance to this model class.

        Mapping rules:
        - Base model fields map to fields in this model with the same name.
        - Entries in base.custom map to fields in this model with the same key,
        overwriting standard base fields if names collide.
        - Base model fields and base.custom entries that don't match a defined field
        in this model are mapped into this model's model_extra if allowed.
        - None values are excluded if exclude_none is True.
        """
        # 1. Get data from standard base fields (excluding 'custom' itself).
        #    model_dump handles exclude and exclude_none filtering efficiently.
        source_data = base.model_dump(exclude={'custom'}, exclude_none=exclude_none)

        # 2. Get data from base.custom, if it exists and is a dictionary.
        base_custom_dict: Dict[str, Any] = {}
        if hasattr(base, 'custom'):
            if isinstance(base.custom, dict):
                base_custom_dict = base.custom
            elif base.custom is not None:
                # Log warning only if custom exists and is not None/dict
                # Use stack level 2 to point to the caller of from_base
                logger.debug("Stack trace:\n" + "".join(traceback.format_stack()))
                logger.warning(f"base.custom ({type(base.custom)}) is not a dictionary, ignoring custom fields during mapping from base.", stacklevel=2)

        # 3. Add data from base.custom to source_data, allowing it to overwrite
        #    standard fields if keys collide (as per original logic's potential).
        if base_custom_dict:
            # Filter None from custom dict if needed before updating source_data
            filtered_custom_data = {
                k: v for k, v in base_custom_dict.items()
                if not (exclude_none and v is None)
            }
            source_data.update(filtered_custom_data) # .update() handles overwriting

        # 4. Create the instance. Pydantic's constructor automatically maps
        #    keys matching model_fields and puts the rest into model_extra
        #    if 'extra' is 'allow'. This replaces the manual init_data/extra_data logic.
        instance = cls(**source_data)

        return instance

    @classmethod
    def required_fields(cls) -> set[str]:
        return {
            field_name
            for field_name, field_info in cls.model_fields.items()
            if field_info.default is PydanticUndefined and field_info.default_factory is None
        }

####################################
# --- Metadata and Filters ---
####################################

Id = str | int

PRIMITIVE_TYPES: Tuple[type, ...] = (str, int, float, bool)

Primitive = str | int | float | bool

ALLOWED_KEY_REGEX = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

class BaseMetadata(_mappedFields):
    """
    Base class for metadata models.
    """
    model_config = ConfigDict(extra="allow")

    @model_validator(mode='after')
    def validate_extra_fields(self):
        if not self.model_extra:
            return self

        allowed_value_types = PRIMITIVE_TYPES

        for key, value in self.model_extra.items():
            if not isinstance(key, str):
                 raise ValueError(f"Custom field key must be a string, got {type(key).__name__} for key '{key}'.")

            if not ALLOWED_KEY_REGEX.fullmatch(key):
                 raise ValueError(
                     f"Custom field key '{key}' contains invalid characters or format. "
                     f"Keys must match regex '{ALLOWED_KEY_REGEX.pattern}'."
                 )

            # Existing Value Validation
            if not isinstance(value, allowed_value_types):
                raise ValueError(
                    f"Custom field '{key}' has an invalid value type. "
                    f"Expected one of {[t.__name__ for t in allowed_value_types]}, but got {type(value).__name__}."
                )

        return self
    
class ChatMetadata(BaseMetadata):
    """Metadata specific to `chat` flow."""
    _flow: Flow = PrivateAttr(Flow.CHAT)

    user_id: Id = Field(description="`Indexed` A user ID is an isolated search space.")
    chat_id: Optional[Id] = Field(None, description="`Indexed` Metadata for filtering.")
    
class FileMetadata(BaseMetadata):
    """Metadata specific to `file` flow."""
    _flow: Flow = PrivateAttr(Flow.FILE)

    path: str = Field(description="Needed to process the file.")
    folder_id: Id = Field(description="`Indexed` A folder ID is an isolated search space.")
    user_id: Optional[Id] = Field(None, description="`Indexed` Metadata for filtering.")
    file_id: Optional[Id] = Field(None, description="`Indexed` Metadata for filtering.")
    title: Optional[str] = Field(None, description="Metadata for filtering.")

Metadata = ChatMetadata | FileMetadata

class Operator(Enum):
    EQ = "="
    LT = "<"
    GT = ">"
    IN = "in"
    def __str__(self):
        return self.value

class Condition(BaseModel):
    """Represents an operator-value filter condition."""
    operator: Operator
    value: Primitive | List[Primitive]

    @model_validator(mode='after')
    def validate_operator_value_compatibility(self):
        """Validate operator/value compatibility within the Condition."""
        if self.operator == Operator.IN:
            if not isinstance(self.value, list):
                raise ValueError(
                    f"Operator '{self.operator.name}' requires a list value, "
                    f"but got {type(self.value).__name__}."
                )
        elif self.operator in (Operator.EQ, Operator.LT, Operator.GT):
            if isinstance(self.value, list):
                 raise ValueError(
                     f"Operator '{self.operator.name}' requires a single value, "
                     f"but got a list."
                 )
        return self


Filter = Primitive | List[Primitive] | List[Condition]
filter_adapter = TypeAdapter(Filter)

class BaseFilters(_mappedFields):
    """Base filter validator."""

    model_config = ConfigDict(extra="allow")

    @model_validator(mode='after')
    def validate_extra_fields(self):
        """Validates extra fields (keys and values) to ensure they conform to safety and Filter type."""
        if not self.model_extra:
            return self

        for key, value in self.model_extra.items():
            # validate keys
            if not isinstance(key, str):
                 raise ValueError(f"Filter key must be a string, got {type(key).__name__} for key '{key}'.")

            if not ALLOWED_KEY_REGEX.fullmatch(key):
                 raise ValueError(
                     f"Filter key '{key}' contains invalid characters or format. "
                     f"Keys must match regex '{ALLOWED_KEY_REGEX.pattern}'."
                 )

            # validate values
            try:
                filter_adapter.validate_python(value)
            except (ValidationError, ValueError) as e:
                raise ValueError(
                    f"Filter key '{key}' has an invalid value. "
                    f"Expected a valid Filter type, but got {value}. "
                    f"Validation error: {e}"
                ) from e

        return self

    def std_conditions(self) -> Dict[str, List[Condition]]:
        """
        Maps filters to standard dict object format:
        - Key: Standard field names (from mapping or extra field keys)
        - Value: List[Condition] object(s)
        """
        # Helper function to convert a Filter value into a List[Condition]
        def _to_list_of_conditions(value: Filter) -> List[Condition]:
            if isinstance(value, list):
                # Check if it's already a list of Conditions
                if value and isinstance(value[0], Condition):
                    return value
                else:
                    # Assume it's a list of values for an IN operator
                    return [Condition(operator=Operator.IN, value=value)]
            else:
                # Assume it's a single value for an EQ operator
                return [Condition(operator=Operator.EQ, value=value)]

        standardized_filters: Dict[str, List[Condition]] = {}

        # Process defined fields that were set and are in the indexed keys
        defined_fields_to_process = self.model_fields_set & BaseNode.indexed_keys(self._flow)
        defined_filters = {
            field_name: _to_list_of_conditions(getattr(self, field_name))
            for field_name in defined_fields_to_process
        }
        standardized_filters.update(defined_filters)

        # Process extra fields
        if self.model_extra:
            extra_filters = {
                key: _to_list_of_conditions(value)
                for key, value in self.model_extra.items()
            }
            standardized_filters.update(extra_filters)

        return standardized_filters

    def std_dict(self) -> Dict[str, Any]:
        """
        Maps filters to standard dict format:
        - Key: Standard field names (from mapping or extra field keys)
        - Value: Primitive | List[Primitive]
        """
        conditions = self.std_conditions()
        conditions = {k: condition.value for k, v in conditions.items() for condition in v}

        return conditions

class ChatFilters(BaseFilters):
    """Metadata filter specific to `chat` flow."""
    _flow: Flow = PrivateAttr(Flow.CHAT)

    user_id: Optional[Filter] = Field(None, description="`Indexed` A user ID is an isolated search space.")
    chat_id: Optional[Filter] = Field(None, description="`Indexed` Metadata for filtering.")

class FileFilters(BaseFilters):
    """Metadata filter specific to `file` flow."""
    _flow: Flow = PrivateAttr(Flow.FILE)

    folder_id: Optional[Filter] = Field(None, description="`Indexed` A folder is an isolated search space. Not required only for read operations.")
    user_id: Optional[Filter] = Field(None, description="`Indexed` Metadata filter.")
    file_id: Optional[Filter] = Field(None, description="`Indexed` Metadata filter.")
    title: Optional[Filter] = Field(None, description="Metadata filter.")
    path: Optional[Filter] = Field(None, description="Metadata filter.")

Filters = ChatFilters | FileFilters

####################################
# --- Nodes and Relations ---
####################################

class NodeType(Enum):
    """Enum representing the possible types of nodes."""
    FACT = "fact"
    CHUNK = "chunk"
    TOPIC = "topic"
    ENTITY = "entity"
    def __str__(self):
        return self.value

class BaseNode(BaseModel):
    """Internal structure with all node properties."""
    node_type: NodeType
    flow: Flow
    content: str
    embedding: Optional[List[float]] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    similarity: Optional[float] = None
    # indexed fields
    node_id: Optional[Id] = None
    user_id: Optional[Id] = None
    chat_id: Optional[Id] = None
    folder_id: Optional[Id] = None
    file_id: Optional[Id] = None
    # chunk node fields
    custom: Optional[Dict[str, Primitive]] = None

    # Non-db fields
    _descriptor: Optional[str] = PrivateAttr(None)
    _hash: str = PrivateAttr(None)

    max_name_chars: ClassVar[int] = 32

    @staticmethod
    def node_keys(node_type: NodeType) -> Set[str]:
        """Keys that represent data fields of the node, excluding private/class vars."""
        keys = set(BaseNode.model_fields.keys())
        if node_type != NodeType.CHUNK:
            keys -= {"custom"}

        return keys

    @staticmethod
    def indexed_keys(flow: Optional[Flow] = None) -> Set[str]:
        """Keys that are used for indexing."""
        k = {
            Flow.CHAT: {"user_id", "chat_id"},
            Flow.FILE: {"folder_id", "user_id", "file_id"},
        }

        if flow is None:
            return set.union(*k.values())
        else:
            return k[flow]

    @staticmethod
    def search_space(flow: Optional[Flow] = None) -> Set[str]:
        """Keys that are used for indexing."""
        k = {
            Flow.CHAT: {"user_id"},
            Flow.FILE: {"folder_id"},
        }

        if flow is None:
            return set.union(*k.values())
        else:
            return k[flow]

    def __init__(self, **data):
        super().__init__(**data)
        self._update_hash()

    def _update_hash(self) -> str:
        """Compute a hash based on the node's content and ids."""
        self._hash = hashlib.md5(f"{self.node_type}:{self.flow}:{self.content}".encode()).hexdigest()

    def __eq__(self, other):
        if not isinstance(other, BaseNode):
            return False
        return self._hash == other._hash

    @field_validator('content')
    @classmethod
    def strip_content(cls, v):
        if v is None:
            return None
        return v.strip()

    def __str__(self) -> str:
        return self.content or ""

    @field_validator('created_at', 'updated_at')
    @classmethod
    def to_millis(cls, value: Optional[int]) -> Optional[int]:
        """Validates if the timestamp is likely in seconds and converts it to milliseconds."""
        if value is None:
            return None

        if not isinstance(value, (int, float)):
             raise ValueError("Timestamp must be an integer or float")

        value = int(value)

        if value <= 1e8 or 1e16 <= value:
            raise ValueError("Invalid timestamp value")

        if 1e14 < value:
            return int(value/1000)
        elif 1e11 < value:
            return value
        elif 1e8 < value:
            return value * 1000

class ChatNode(BaseNode, _mappedFields):
    """Represents a basic unit of memory for a `chat` flow."""
    _flow: Flow = PrivateAttr(Flow.CHAT)

    user_id: Id = Field(description="`Indexed` A user ID is an isolated search space.")
    chat_id: Optional[Id] = Field(None, description="`Indexed` Metadata for filtering.")

class FileNode(BaseNode, _mappedFields):
    """Represents a basic unit of memory for a `file` flow."""
    _flow: Flow = PrivateAttr(Flow.FILE)

    path: Optional[str] = Field(None, description="Needed to process the file.")
    folder_id: Optional[Id] = Field(None, description="`Indexed` A folder ID is an isolated search space.")
    user_id: Optional[Id] = Field(None, description="`Indexed` Metadata for filtering.")
    file_id: Optional[Id] = Field(None, description="`Indexed` Metadata for filtering.")
    title: Optional[str] = Field(None, description="Metadata for filtering.")
    ichunk: Optional[int] = Field(None, description="Number of chunk in the file, base 0.")
    chunks: Optional[int] = Field(None, description="Total number of chunks in the file.")

Node = ChatNode | FileNode

class Relation(BaseModel):
    """Represents the basic memory unit."""
    fact: BaseNode = Field(description="The facts associated with the relation")
    chunk: BaseNode = Field(description="The chunk of the relation")
    topics: List[BaseNode] = Field(description="The topics of the relation")
    entities: List[BaseNode] = Field(description="The entities involved in the relation")

    def to_list(self) -> List[BaseNode]:
        """Convert the relation to a list of nodes.
        
        Returns a list in the order:
            [fact, chunk, topics..., entities...]
        """
        return [self.fact, self.chunk] + self.topics + self.entities
        
    def to_dicts(self, include: Set = None, exclude: Set = None, exclude_none=False) -> List[Dict[str, Any]]:
        """Convert the relation to a list of node dictionaries.
        
        Returns a list of dictionaries in the same order as to_list():
            [fact, chunk, topics..., entities...]
        """
        nodes = self.to_list()
        return [node.model_dump(mode='json', include=include, exclude=exclude, exclude_none=exclude_none) 
                for node in nodes]

    def to_id_nodes(self, include: Set = None, exclude: Set = None, exclude_none=False) -> Dict[str, Any]:
        """Convert the relation to a dictionary.
        
        Keys:
            n0: fact
            n1: chunk
            n*: topics and entities (n3, n4, ...)
        """
        node_dicts = self.to_dicts(include, exclude, exclude_none)
        
        return {f"n{i}": d for i, d in enumerate(node_dicts)}


####################################
# --- File operations ---
####################################

class FileStatus(Enum):
    """Enum for possible file processing states."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    ERROR = 'error'
    CANCELLED = 'cancelled'
    def __str__(self):
        return self.value

class ChunkResult(BaseModel):
    """Represents the result of processing a single chunk."""
    chunk_index: int = Field(..., description="Index of the chunk within the file.")
    ids: Optional[List[str]] = Field(None, description="List of IDs generated for the upserted items in this chunk.")
    error: Optional[str] = Field(None, description="Error message if processing this chunk failed.")

class FileState(BaseModel):
    """Represents the processing state and cumulative result of a single file."""
    file_path: str = Field(..., description="Path to the file being processed.") # Added from FileUpsertResult
    task_id: Optional[str] = Field(None, description="ID of the task processing this file.")
    total_chunks: Optional[int] = Field(None, description="Total number of chunks expected for this file.")
    chunk_results: List[ChunkResult] = Field([], description="List of results for each processed chunk.") # Added from FileUpsertResult, now cumulative
    status: FileStatus = Field(FileStatus.PENDING, description="Current status of the file processing.")
    error: Optional[str] = Field(None, description="Error message if status is ERROR or CANCELLED.") # Kept from both

    # is_terminal is kept as a property
    @property
    def is_terminal(self) -> bool:
        """Returns True if the file is in a final state (completed, error, cancelled)."""
        return self.status in {FileStatus.COMPLETED, FileStatus.ERROR, FileStatus.CANCELLED}

    # Helper method to create an error state (similar to FileUpsertResult.error)
    @classmethod
    def create_error_state(cls, file_path: str, error_msg: str, task_id: Optional[str] = None) -> 'FileState':
        """Helper to create a FileState instance representing an error."""
        return cls(
            file_path=file_path,
            task_id=task_id,
            status=FileStatus.ERROR,
            error=error_msg,
            # total_chunks and chunk_results would likely be unknown or empty on a file-level error
            total_chunks=None,
            chunk_results=[]
        )

    # Helper method to update state with a new chunk result
    def update_with_chunk_result(self, chunk_result: ChunkResult) -> None:
        """Updates the state by adding a new chunk result and potentially updating status."""
        self.chunk_results.append(chunk_result)
        # Transition from PENDING to PROCESSING on the first chunk result
        if self.status == FileStatus.PENDING:
            self.status = FileStatus.PROCESSING
        # Transition to COMPLETED if total_chunks is known and all chunks are processed
        if self.total_chunks is not None and len(self.chunk_results) == self.total_chunks:
            # Note: Individual chunk errors don't change the file status from COMPLETED. File-level error is established by create_error_state()
            self.status = FileStatus.COMPLETED

class BatchStatusSummary(BaseModel):
    """Summary of the current batch processing status."""
    total_files: int
    files_done: int
    processing_files: int
    percentage: float
    elapsed_time: float
    remaining_time: Optional[float] = None
    file_states: Dict[str, FileState] = {}


####################################
# --- APIs and models ---
####################################

class UrlKeyModel(NamedTuple):
    url: str
    key: str
    model: str

class UrlKey(NamedTuple):
    url: str
    key: str


####################################
# --- Prompts ---
####################################

class Language(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"

    def __str__(self):
        return self.value

    @classmethod
    def _missing_(cls, value):
        """Handle variations like 'en-US'."""
        if isinstance(value, str):
            base_lang = value.split('-')[0].lower()
            for member in cls:
                if member.value == base_lang:
                    return member
        return super()._missing_(value)

class Translations(BaseModel):
    en: str
    es: str
    fr: str
    de: str

class Example(BaseModel):
    flow: Flow = Field(..., description="Type of example")
    example_input: Translations = Field(..., description="Example input translations")
    example_output: Translations = Field(..., description="Example output translations")

class Prompt(BaseModel):
    prompt_type: Literal["system", "user"] = Field(..., description="Type of prompt")
    prompt: Translations = Field(..., description="Prompt translations")
    examples: List[Example] = Field(..., description="Examples of inputs and outputs")

    def to_str(self, flow: Optional[Flow] = None, language: Language = Language.ENGLISH) -> str:
        r = getattr(self.prompt, language.value)
        examples = [
            f"[EXAMPLE_INPUT]\n{getattr(e.example_input, language.value)}\n[/EXAMPLE_INPUT]\n[EXAMPLE_OUTPUT]\n{getattr(e.example_output, language.value)}"
            for e in self.examples if not flow or e.flow == flow
        ]
        if not examples:
            return r

        r += "\n\n--- This is an example ---\n\n"
        r += "\n\n--- This is another example ---\n\n".join(examples)
        r += "\n\n--- This was an example ---\n\n"
        return r

####################################
# --- Helper functions ---
####################################

OUTPUT_CLASS_MAP: Dict[Type, Dict[Flow, Type]] = {
    BaseMetadata: {
        Flow.CHAT: ChatMetadata,
        Flow.FILE: FileMetadata,
    },
    BaseFilters: {
        Flow.CHAT: ChatFilters,
        Flow.FILE: FileFilters,
    },
    BaseNode: {
        Flow.CHAT: ChatNode,
        Flow.FILE: FileNode,
    },
}

def get_base_target(output_base: Type, flow: Optional[Flow]) -> Type:
    """Match the output class flow type to the input base class and flow."""
    flow_map = OUTPUT_CLASS_MAP.get(output_base)
    if flow_map and flow in flow_map:
        return flow_map[flow]

    return output_base

