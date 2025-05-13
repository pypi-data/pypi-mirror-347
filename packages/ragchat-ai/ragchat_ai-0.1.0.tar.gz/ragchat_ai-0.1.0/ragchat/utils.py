import functools
import asyncio
import httpx
import copy
import itertools
import tiktoken
from time import time
from cachetools import TTLCache
from typing import List, Any, Tuple, Dict, TypeVar, Iterable
from ragchat.log import get_logger
from ragchat.definitions import UrlKey, UrlKeyModel

logger = get_logger(__name__)
URL_MODELS_CACHE = TTLCache(maxsize=128, ttl=900)

T = TypeVar('T')

def flatten(items: List[Any]) -> List[Any]:
    """Flatten a list of items.

    Converts a list that may contain nested lists into a single flat list.

    Args:
        items: A list that may contain nested lists

    Returns:
        A flattened list
    """
    if not items:
        return items

    # Flatten the list using itertools.chain
    return list(itertools.chain.from_iterable(
        [item] if not isinstance(item, list) else item for item in items
    ))

def get_unique(items: List[T]) -> List[T]:
    """Flatten list and get unique items preserving order.

    Works with any object type that supports equality comparison.
    Does not rely on hashability of objects.
    """
    if not items:
        return items

    # Flatten the list
    flat_items = flatten(items)

    # Create a list of unique items preserving order
    unique_items = []
    [unique_items.append(x) for x in flat_items if x not in unique_items]

    return unique_items

def retry(msg_arg=None):
    """Retries an async function with exponential backoff and optional error injection.

    The number of retries is determined by `self.settings.retries` if available
    and valid (non-negative integer), otherwise defaults to 3.
    Includes special handling for `ValueError` with a short delay.
    Can be configured to retry only specific exception types using `self.retry_on`.

    Args:
        msg_arg (str, optional): The name of the keyword argument in the
            decorated function where the string representation of the error
            from the previous failed attempt should be injected on retries.
            Defaults to None.

    Returns:
        function: The decorator function.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            # --- Determine max_retries ---
            retries = 3 # default
            try:
                settings_retries = int(self.settings.retries)
                assert 0 <= settings_retries
                retries = settings_retries
            except Exception:
                logger.warning(f"Invalid retries value in settings for {func.__name__}. Using default {retries}.")

            # --- Retry Logic ---
            current_retry = 0
            last_error = None

            while current_retry < retries:
                try:
                    call_kwargs = kwargs

                    # Inject error context if requested and if it's a retry attempt
                    if last_error and msg_arg is not None:
                        call_kwargs = copy.copy(kwargs)
                        call_kwargs[msg_arg] = f"\n\n{str(last_error)}"

                    # Call the wrapped function
                    return await func(self, *args, **call_kwargs)

                except Exception as e:
                    last_error = e # Store the error for potential injection

                    # If self.retry_on is specified, check if the exception should be retried
                    if hasattr(self, 'retry_on') and self.retry_on and not any(isinstance(e, exc_type) for exc_type in self.retry_on):
                        raise

                    current_retry += 1
                    if current_retry >= retries:
                        raise ValueError(f"Function {func.__name__} failed after {current_retry} retries. Last error: {str(e)}")

                    # Log the retry attempt
                    logger.warning(f"Retry {current_retry}/{retries} for {func.__name__}: {str(e)}", stacklevel=2)

                    # ~0 delay for ValueError, exponential backoff for other exceptions
                    if isinstance(e, ValueError):
                        delay = 0.5
                    else:
                        # N starts at 1 for the first retry
                        delay = max(0, 2 ** current_retry - 2)
                    await asyncio.sleep(delay)

            # Prepare final call kwargs (potentially with last error if msg_arg is set)
            final_call_kwargs = kwargs
            if last_error and msg_arg is not None:
                final_call_kwargs = copy.copy(kwargs)
                final_call_kwargs[msg_arg] = f"\n\n{str(last_error)}"

            return await func(self, *args, **final_call_kwargs) # Call one last time

        return wrapper
    return decorator

def timeit(func):
    """Decorator that logs the execution time of the decorated async function."""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time()
        result = await func(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        logger.debug(f"{func.__name__} took {execution_time:.3f} seconds")
        return result

    return async_wrapper

async def _fetch_available_models(
    apis: Iterable[UrlKey],
    use_cache: bool = True
) -> Dict[str, List[str]]:
    """
    Fetch available models from all APIs.
    Returns a dict: {url: [model_id, ...], ...}
    Uses a TTL cache (15 minutes) for caching results if use_cache is True.
    """
    if not apis:
        return {}

    if use_cache:
        # Check if all URLs are cached
        if all(api.url in URL_MODELS_CACHE for api in apis):
            return {api.url: URL_MODELS_CACHE[api.url] for api in apis}

    async def fetch_one(api: UrlKey) -> Tuple[str, List[str]]:
        headers = {"Authorization": f"Bearer {api.key}"}
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{api.url}/models", headers=headers)
                response.raise_for_status()
                resp_json = response.json()
                return api.url, [m["id"] for m in resp_json.get("data", [])]
        except Exception:
            return api.url, []

    results = await asyncio.gather(
        *(fetch_one(api) for api in apis),
        return_exceptions=False
    )
    # Merge into a single dict
    result_dict = {url: models for url, models in results}
    if use_cache:
        URL_MODELS_CACHE.update(result_dict)
    return result_dict

async def select_model(
    models: List[str],
    apis: Iterable[UrlKey],
    use_cache: bool = True,
) -> UrlKeyModel:
    """
    Selects the first model from the `models` list that is available
    from any of the APIs in `apis` (list of UrlKey).

    Args:
        models: A list of model IDs to check, in order of preference.
        apis: An iterable of UrlKey objects representing the APIs to check.
        use_cache: If True, use the TTL cache for available models.

    Returns:
        A UrlKeyModel object containing the URL, key, and selected model ID.

    Raises:
        Exception: If none of the specified models are available from any of the APIs.
    """

    available_models_by_url: Dict[str, List[str]] = await _fetch_available_models(apis, use_cache)

    for api in apis:
        available_models = available_models_by_url.get(api.url, [])
        for m in models:
            # Check if the model ID (or the part after the last slash) is in the available list
            if m.split('/')[-1] in available_models:
                return UrlKeyModel(api.url, api.key, m)

    logger.error(
        f"models={models!r}, apis={[('***' if api.key else None, api.url) for api in apis]}, "
        f"no valid model could be selected."
    )
    raise Exception("No valid model could be selected.")

def est_tokens(text: str) -> int:
    """
    Counts the number of tokens in a string using the tokenizer of GPT-4o.
    """
    try:
        encoding = tiktoken.get_encoding("o200k_base")
        num_tokens = len(encoding.encode(text))
        return num_tokens
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1