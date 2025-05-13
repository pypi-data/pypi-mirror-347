import asyncio
import httpx
from typing import List, Optional, Any, Dict
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from cachetools import LRUCache
from ragchat.definitions import BaseNode, Relation, UrlKey
from ragchat.log import get_logger
from ragchat.utils import select_model, timeit

logger = get_logger(__name__)

class EmbeddingSettings(BaseSettings):
    base_url: Optional[str] = None
    local_hosts: Optional[List[str]] = ["localhost", "host.docker.internal"]
    port: Optional[int] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    models: Optional[List[str]] = None
    dims: int = 1536
    cache_size: int = 5461

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="EMBEDDING_")

    @field_validator("models", mode="before")
    @classmethod
    def validate_models(cls, v):
        if isinstance(v, str):
            return [m.strip() for m in v.split(',')]
        return v

    def request_dict(self):
        return self.model_dump(mode='json', include={"base_url", "api_key", "model", "dims"}, exclude_none=True)

    async def initialize(self):
        """Select the best available model and API endpoint based on settings."""
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

class Embedder:
    def __init__(self, settings: Optional[EmbeddingSettings] = None):
        self.settings = settings or EmbeddingSettings()
        self.cache = LRUCache(maxsize=self.settings.cache_size)

    async def initialize(self):
        await self.settings.initialize()

    @staticmethod
    async def from_openai(
        texts: List[str],
        api_key: str,
        base_url: str,
        model: str,
        dims: Optional[int] = None,
    ) -> List[List[float]]:
        """
        Get embeddings from an OpenAI-compatible API for a list of texts.
        """
        url = f"{base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "input": texts,
            "model": model,
        }
        if dims:
            payload["dimensions"] = dims

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return [item["embedding"] for item in response.json()["data"]]

    async def embed(self, texts: List[str], use_cache=True, **kwargs) -> List[List[float]]:
        """Get the embeddings for the given list of texts using the configured API, with text deduplication and caching."""
        # Preprocess texts and prepare cache keys
        clean_texts = [t.replace("\n", " ") for t in texts]
        params = {**self.settings.request_dict(), **kwargs}
        model = params["model"]
        dims = params.get("dims")

        # Deduplicate texts while preserving original order information
        unique_texts = []
        text_to_unique_idx = {}
        
        for text in clean_texts:
            if text not in text_to_unique_idx:
                text_to_unique_idx[text] = len(unique_texts)
                unique_texts.append(text)
        
        # Prepare cache keys for each unique text
        unique_cache_keys = [(t, model, dims) for t in unique_texts]

        # Check cache and collect texts to fetch
        unique_embeddings = [None] * len(unique_texts)
        uncached_indices = []
        uncached_texts = []
        
        for idx, (text, cache_key) in enumerate(zip(unique_texts, unique_cache_keys)):
            if use_cache and cache_key in self.cache:
                unique_embeddings[idx] = self.cache[cache_key]
            else:
                uncached_indices.append(idx)
                uncached_texts.append(text)

        # Fetch embeddings for uncached unique texts
        if uncached_texts:
            uncached_embeddings = await self.from_openai(
                texts=uncached_texts,
                api_key=params["api_key"],
                base_url=params["base_url"],
                model=model,
                dims=dims,
            )
            # Store in cache and fill in the results
            for i, emb in enumerate(uncached_embeddings):
                unique_idx = uncached_indices[i]
                if use_cache:
                    self.cache[unique_cache_keys[unique_idx]] = emb
                unique_embeddings[unique_idx] = emb

        # Map the unique embeddings back to the original order
        embeddings = [unique_embeddings[text_to_unique_idx[text]] for text in clean_texts]
        return embeddings

    async def embed_nodes(self, nodes: List[BaseNode], use_cache: bool = True, **kwargs) -> None:
        """Embed a list of nodes by embedding their string representations."""
        embs = await self.embed([str(n) for n in nodes], use_cache, **kwargs)
        for i, n in enumerate(nodes):
            n.embedding = embs[i]

    @timeit
    async def embed_relations(self, relations: List[Relation], use_cache: bool = True, **kwargs) -> None:
        """Embed the nodes contained within a list of relations."""
        all_nodes = []
        for r in relations:
            all_nodes.extend(r.to_list())
        await self.embed_nodes(all_nodes, use_cache, **kwargs)