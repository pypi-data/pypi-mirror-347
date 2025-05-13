from time import time
import json
import copy
import asyncio
from litellm import acompletion
from litellm.types.utils import ChatCompletionMessageToolCall
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Any, Optional, Union, Callable, AsyncGenerator
from functools import partial
from ragchat.log import get_logger
from ragchat.utils import retry, flatten, get_unique, select_model, timeit
from ragchat.definitions import (
    Flow,
    Message,
    MessageClassification,
    NodeType,
    Relation,
    BaseNode,
    UrlKey,
    Language,
    Metadata,
    )
from ragchat.parser import (
    markdown_to_heading_items,
    markdown_to_relations,
    header_items_to_markdown,
    markdown_to_nodes,
    dicts_to_relations,
    get_top_k_common_items,
    )
from ragchat.prompts import (
    MSG_CLASSIFICATION,
    TOPICS,
    TOPIC_FACTS,
    FACT_ENTITIES,
    ENTITY_DEFINITIONS,
    QUERY_NODES,
    )

logger = get_logger(__name__)

class LlmSettings(BaseSettings):
    base_url: Optional[str] = None
    local_hosts: Optional[List[str]] = ["localhost", "host.docker.internal"]
    port: Optional[int] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    models: Optional[List[str]] = None
    retries: int = 3
    batch_size: int = 8
    temperature: float = 0.1
    custom_msg_classification_prompt: Optional[str] = Field(None, description="Replaces MESSAGE_CLASSIFICATION prompt")
    custom_topics_prompt: Optional[str] = Field(None, description="Replaces TOPICS_PROMPT")
    custom_topic_facts_prompt: Optional[str] = Field(None, description="Replaces TOPIC_FACTS_PROMPT")
    custom_fact_entities_prompt: Optional[str] = Field(None, description="Replaces FACT_ENTITIES_PROMPT")
    custom_entity_definitions_prompt: Optional[str] = Field(None, description=f"Replaces ENTITY_DEFINITIONS_PROMPT")
    custom_query_nodes_prompt: Optional[str] = Field(None, description="Replaces QUERY_NODES_PROMPT")
    
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="LLM_")

    @field_validator("models", mode="before")
    @classmethod
    def validate_models(cls, v):
        if isinstance(v, str):
            return [m.strip() for m in v.split(',')]
        return v
    
    def request_dict(self):
        return self.model_dump(mode='json', include={"base_url", "api_key", "model", "temperature"}, exclude_none=True)
    
    async def initialize(self):
        """Ensure `model` is available in `base_url`."""
        apis = set()
        if self.base_url and self.api_key:
            apis.add(UrlKey(url=self.base_url, key=self.api_key))
        port = f":{self.port}" if self.port else ""
        for host in self.local_hosts:
            apis.add(UrlKey(url=f"http://{host}{port}/v1", key="NA"))
        
        selected_model = await select_model([self.model] if self.model else self.models, apis)
        self.base_url = selected_model.url
        self.api_key = selected_model.key
        self.model = selected_model.model
        logger.info(f"Using model {selected_model.model} from URL {selected_model.url}")

class LLM:
    def __init__(self, settings: Optional[LlmSettings] = None):
        self.settings = settings or LlmSettings()
        self.semaphore: asyncio.Semaphore

    async def initialize(self):
        await self.settings.initialize()
        self.semaphore = asyncio.Semaphore(self.settings.batch_size)
    
    @retry(msg_arg="retry_message")
    @timeit
    async def generate_response(self,
        messages: List[Message],
        retry_message: Optional[str] = None,
        parser: Optional[Callable[[str], Any]] = None,
        **kwargs
        ) -> str | List[ChatCompletionMessageToolCall] | Any:
        """
        Generate a response based on the given messages using Litellm asynchronously.

        Args:
            messages (List[Message]): List of message objects with role and content.
            retry_message (Optional[str]): Message to include in system prompt when retrying.
            parser (Optional[Callable[[str], Any]]): Optional function to parse the response content (e.g., parse_entities_markdown).
        
        Kwargs:
            model (str): Model to use for completion.
            base_url (str): Base URL for the model API.
            api_key (str): API key for authentication.
            temperature (float): Sampling temperature.
            max_tokens (int): Maximum number of tokens to generate.
            tools (List[Dict]): List of tools the model may call.
            tool_choice (str | Dict): Controls which (if any) tool is called by the model.
            strict (bool): Whether to enforce strict validation.

        Returns:
            str | List[ChatCompletionMessageToolCall] | Any: Either a string response, a parsed object using the parser function, or the full message object when tools are used.
        """

        # Handle retry_message if provided
        if retry_message and messages:
            messages = copy.deepcopy(messages)
            has_system_message = False
            for msg in messages:
                if msg.role == 'system':
                    msg.content += f"\n\n{retry_message}"
                    has_system_message = True
                    break
            if not has_system_message:                
                messages.insert(0, Message(role='system', content=retry_message))
                
        params = {**self.settings.request_dict(), **kwargs, "stream": False}
        strict = params.pop("strict", True)

        # filter params
        remove = {"flow", "language"}
        params = {k: v for k, v in params.items() if k not in remove}

        response = await acompletion(messages=messages, **params)
        message = response.choices[0].message
                
        system_msgs = [m for m in messages if m.role == "system"]
        logger.debug(f"llm sysetm msg: {system_msgs[0] if system_msgs else 'NA'}\nllm user msg: {messages[-1]}\nllm response: {message}")
        
        # Parse tool_calls if tools are being used
        if message.tool_calls:
            for tool_call in message.tool_calls:
                if hasattr(tool_call, 'function') and hasattr(tool_call.function, 'arguments'):
                    try:
                        tool_call.function.arguments = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError as e:
                        if strict:
                            raise ValueError(f"Failed to parse tool arguments as JSON: {e}")
            return message.tool_calls
        
        # Handle content parsing if no tools
        if parser and message.content:
            try:
                return parser(message.content)
            except Exception as e:
                if strict:
                    raise

        return message.content

    @retry(msg_arg="retry_message")
    async def extract_relations(
        self,
        text: str,
        metadata: Metadata,
        context: Optional[str] = None,
        prev_topics: Optional[List[str]] = None,
        prev_entities: Optional[List[str]] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        retry_message: Optional[str] = None,
        **kwargs
    ) -> List[Relation]:
        """Extracts all the topics, facts and entities mentioned in the text."""
        there_is_data = 32 < len(text)

        draft_topics: List[str] = await self._extract_topics(
            text=text,
            metadata=metadata,
            context=context,
            prev_topics=prev_topics,
            flow=flow,
            language=language,
            retry_message=retry_message,
            **kwargs
        )
        if not draft_topics and there_is_data:
            raise ValueError(f"Pay attention to the instructions.")

        topic_facts: Dict[str, List[str]] = await self._extract_topic_facts(
            text=text,
            draft_topics=draft_topics,
            context=context,
            flow=flow,
            language=language,
            retry_message=retry_message,
            **kwargs
        )
        if not topic_facts and there_is_data:
            raise ValueError(f"Pay attention to the instructions.")
        
        draft_facts = get_unique(topic_facts.values())
        fact_entities: Dict[str, List[BaseNode]] = await self._extract_fact_entities(
            draft_facts=draft_facts,
            metadata=metadata,
            context=context,
            prev_entities=prev_entities,
            flow=flow,
            language=language,
            retry_message=retry_message,
            **kwargs
        )
        if not fact_entities and there_is_data:
            raise ValueError(f"Pay attention to the instructions.")
        
        fact_entities = await self._extract_entity_definitions(
            text=text,
            metadata=metadata,
            fact_entities=fact_entities,
            flow=flow,
            language=language,
            retry_message=retry_message,
            **kwargs
        )
        relations: List[Relation] = dicts_to_relations(
            chunk=text,
            topic_facts=topic_facts,
            fact_entities=fact_entities,
            metadata=metadata,
        )
        if not relations and there_is_data:
            logger.warning(f"Failed to extract memories from text: {text}")
        
        return relations
        
    async def classify_message(
        self,
        text: str,
        context: Optional[str] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        **kwargs
    ) -> MessageClassification:
        """Classifies the type of the input message."""        
        if not text:
            return MessageClassification.NONE
        
        input = context + "\n\n" if context else ""
        input += text
        messages = [
            Message(role="system", content=self.settings.custom_msg_classification_prompt or MSG_CLASSIFICATION.to_str(flow, language)),
            Message(role="user", content=f"[INPUT]\n{input}\n\n[/INPUT]\n[OUTPUT]\n"),
        ]

        try:
            llm_response: str = await self.generate_response(
                messages=messages,
                **kwargs
            )
            logger.debug(f"llm response:\n{(llm_response)}")

        except Exception as e:
            logger.exception(e)
            return MessageClassification.NONE
        
        return MessageClassification(llm_response.strip())

    async def _extract_topics(
        self,
        text: str,
        metadata: Metadata,
        context: Optional[str] = None,
        prev_topics: Optional[List[str]] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        retry_message: Optional[str] = None,
        **kwargs
    ) -> List[str]:
        """Extracts topics mentioned in the text."""
        
        if not text:
            return {}
        
        if prev_topics is None:
            prev_topics = []

        input = context + "\n\n" if context else ""
        input += text
        if prev_topics:
            text += "\n\n" + header_items_to_markdown("Optional topics, create different ones if these are not suitable:", prev_topics, "", "-")
        
        messages = [
            Message(role="system", content=self.settings.custom_topics_prompt or TOPICS.to_str(flow, language)),
            Message(role="user", content=f"[INPUT]\n{input}\n\n[/INPUT]\n[OUTPUT]\n"),
        ]

        try:
            llm_response: Dict[str, List[BaseNode]] = await self.generate_response(
                messages=messages,
                parser=partial(markdown_to_nodes, metadata=metadata, node_type=NodeType.TOPIC),
                strict=True,
                retry_message=retry_message,
                max_tokens=256,
                **kwargs
            )
            logger.debug(f"llm response:\n{(llm_response)}")
            topics: List[str] = [t.content for t in get_unique(llm_response.values())]
            prev_topics[:] = topics

        except Exception as e:
            logger.exception(e)
            return {}
        
        return topics

    async def _extract_topic_facts(
        self,
        text: str,
        draft_topics: List[str],
        context: Optional[str] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        retry_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, List[str]]:
        """Extracts facts related to the given topics from the text."""
        
        if not text or not draft_topics:
            return {}

        input = context + "\n\n" if context else ""
        input += "\n\n" + header_items_to_markdown("Topics", draft_topics, "#", "##")
        input += "\n\n" + text
        messages = [
            Message(role="system", content=self.settings.custom_topic_facts_prompt or TOPIC_FACTS.to_str(flow, language)),
            Message(role="user", content=f"[INPUT]\n{input}\n\n[/INPUT]\n[OUTPUT]\n"),
        ]

        try:
            llm_response: Dict[str, List[str]] = await self.generate_response(
                messages=messages,
                parser=partial(markdown_to_heading_items, headings_pool=draft_topics),
                strict=True,
                retry_message=retry_message,
                max_tokens=4096,
                **kwargs
            )
            logger.debug(f"llm response:\n{(llm_response)}")

        except Exception as e:
            logger.exception(e)
            return {}
        
        return llm_response

    async def _extract_fact_entities(
        self,
        draft_facts: List[str],
        metadata: Metadata,
        context: Optional[str] = None,
        prev_entities: Optional[List[str]] = None,
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        retry_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, List[BaseNode]]:
        """Extracts all the entities mentioned in the facts."""
        
        if not draft_facts:
            return []
        
        if prev_entities is None:
            prev_entities = []
        
        input = context + "\n\n" if context else ""
        input += header_items_to_markdown("Facts", draft_facts, "#", "##")
        input += "\n**Do NOT use entities from the examples.**"
        
        if prev_entities:
            input += "\n" + header_items_to_markdown("Optional entities - select from these or create different entities:", prev_entities, '')

        messages = [
            Message(role="system", content=self.settings.custom_fact_entities_prompt or FACT_ENTITIES.to_str(flow, language)),
            Message(role="user", content=f"[INPUT]\n{input}\n\n[/INPUT]\n[OUTPUT]\n"),
        ]

        try:
            llm_response: Dict[str, List[BaseNode]] = await self.generate_response(
                messages=messages,
                parser=partial(markdown_to_nodes, metadata=metadata, node_type=NodeType.ENTITY, heading_type=NodeType.FACT, match_headings=draft_facts),
                strict=True,
                retry_message=retry_message,
                max_tokens=4096,
                **kwargs
            )
            logger.debug(f"llm response:\n{(llm_response)}")
            prev_entities[:] = get_top_k_common_items([n.content for n in flatten(llm_response.values())], 5)

        except Exception as e:
            logger.exception(e)
            return []
                
        return llm_response

    async def _extract_entity_definitions(
        self,
        text: str,
        metadata: Metadata,
        fact_entities: Dict[str, List[BaseNode]],
        flow: Optional[Flow] = None,
        language: Optional[Language] = None,
        retry_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, List[BaseNode]]:
        """Extracts definitions for entities found in facts from the text."""
        
        if not text or not fact_entities:
            return {}
        
        unique_entities = [str(e) for e in get_unique(fact_entities.values())]
        input = header_items_to_markdown("Allowed headings", unique_entities, "#", "##")
        input += "\n**Do NOT use entities from the examples.** The headings refer to entities in the following text:\n"
        input += text
        messages = [
            Message(role="system", content=self.settings.custom_entity_definitions_prompt or ENTITY_DEFINITIONS.to_str(flow, language)),
            Message(role="user", content=f"[INPUT]\n{input}\n[/INPUT]\n[OUTPUT]\n"),
        ]

        try:
            entity_definitions: Dict[str, List[BaseNode]] = await self.generate_response(
                messages=messages,
                parser=partial(markdown_to_nodes, metadata=metadata, node_type=NodeType.ENTITY, heading_type=NodeType.ENTITY, headings_pool=unique_entities),
                strict=True,
                retry_message=retry_message,
                max_tokens=2048,
                **kwargs
            )
            logger.debug(f"llm response:\n{(entity_definitions)}")
            
            if not entity_definitions:
                return fact_entities
            
            unique_definitions = [str(e) for e in get_unique(entity_definitions.values())]
            # might need two passes if a defined entity was itself used as definition
            loops = 1 + int(any(e in unique_definitions for e in unique_entities))
            for i in range(loops):
                for fact, original_entities in fact_entities.items():
                    updated_entities = []
                    for entity in original_entities:
                        new_entities = entity_definitions.get(str(entity))
                        if new_entities:
                            updated_entities.extend(new_entities)
                        else:
                            updated_entities.append(entity)
                    fact_entities[fact] = get_unique(updated_entities)

        except Exception as e:
            logger.exception(e)
            return fact_entities
        
        return fact_entities
    
    @timeit
    async def extract_query_relations(
        self,
        text: str,
        metadata: Metadata,
        context: Optional[str] = None,
        language: Optional[Language] = None,
        **kwargs
    ) -> List[Relation]:
        """Extracts all the topics, facts and entities mentioned in the query."""

        if not text:
            return []
        flow = metadata._flow
        input = context + "\n\n" if context else ""
        input += text
        messages = [
            Message(role="system", content=self.settings.custom_query_nodes_prompt or QUERY_NODES.to_str(flow, language)),
            Message(role="user", content=f"[INPUT]\n{input}\n[/INPUT]\n[OUTPUT]\n"),
        ]
                
        try:
            relations: List[Relation] = await self.generate_response(
                messages=messages,
                parser=partial(markdown_to_relations, text=text, metadata=metadata),
                strict=True,
                max_tokens=512,
                **kwargs
            )
            logger.debug(f"llm response:\n{relations}")

        except Exception as e:
            logger.exception(e)
            return []

        return relations
    