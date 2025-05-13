import os
import tempfile
import aiofiles
import asyncio
import asyncpg
from asyncpg import Pool, Connection
from typing import Any, List, Optional, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from ragchat.utils import get_logger
from ragchat.definitions import FileMetadata

logger = get_logger(__name__)

class PgSettings(BaseSettings):
    url: Optional[str] = None
    local_hosts: Optional[List[str]] = ["localhost", "host.docker.internal"]
    user: str
    password: str
    port: int = 5432
    dbname: str
    prefetch: int = 5

    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="PG_")

    async def initialize(self):
        """Attempts to connect to the PostgreSQL database."""
        urls_to_check = set()
        if self.url:
            urls_to_check.add(self.url)
        
        for host in self.local_hosts:
            urls_to_check.add(f"postgresql://{self.user}:{self.password}@{host}:{self.port}/{self.dbname}")

        connection_attempts = [self._attempt_connection(url) for url in urls_to_check]
        results = await asyncio.gather(*connection_attempts, return_exceptions=True)
        self.url = next((result for result in results if result), None)

        if not self.url:
            error_message = "Could not connect to PostgreSQL using any of the default hosts or the provided URL."
            if urls_to_check:
                # Mask the password in the URLs for logging
                masked_urls = [url.split('@')[-1] for url in urls_to_check]
                error_message += f" Attempted connections to: {', '.join(masked_urls)}"
            raise ConnectionError(error_message)

        logger.info(f"Connection established using ...{self.url.split('@')[-1]}")

    async def _attempt_connection(self, url):
        """Attempts to connect to PostgreSQL at the given url and returns the url if successful."""
        try:
            conn = await asyncpg.connect(url)
            await conn.close()
            return url
        except Exception:
            return None
        
class Pg():
    def __init__(self, settings: Optional[PgSettings] = None):
        """
        Initialize the Pg database.

        Args:
            settings (PgSettings): Configuration object
        """
        self.settings = settings or PgSettings()
        self.pool: Pool = None

    async def initialize(self):
        """Initialize the connection pool and create tables if needed"""
        await self.settings.initialize()
        self.pool = await asyncpg.create_pool(self.settings.url)

    async def download_files(self, file_ids: List[str], exclude_nones: bool = True) -> List[Optional[FileMetadata]]:
        """
        Retrieves file content for given IDs, streams to temporary files,
        and returns a list of dictionaries or None for each ID.

        Args:
            file_ids: A list of file IDs (strings).

        Returns:
            A list where each element corresponds to an input file_id.
            If the file was found and had content, the element is a dictionary
            {'id': str, 'name': str, 'path': str}.
            If the file was not found or had no content, the element is None.
        """
        if not file_ids:
            return []

        temp_dir = tempfile.mkdtemp(prefix="file_stream_cursor_")
        logger.debug(f"Created temporary directory: {temp_dir}")

        query_contents = """
		with 
		folders as (
			select id as folder_id,
			json_array_elements_text(data->'file_ids') as id
			from knowledge
		)
        select
            id as file_id,
            folder_id,
            filename,
            data->>'content' as file_text
        from file inner join folders using(id)
        where id = ANY($1::text[])
        """
        fetched_data_map: Dict[str, FileMetadata] = {}
        conn: Connection = None
        try:
            conn = await self.pool.acquire()
            async with conn.transaction():
                async for record in conn.cursor(query_contents, file_ids, prefetch=self.settings.prefetch):
                    file_id = str(record["file_id"])
                    file_text = record.get("file_text")

                    if file_text is not None:
                        temp_filename = f"{file_id}.txt"
                        temp_path = os.path.join(temp_dir, temp_filename)
                        try:
                            async with aiofiles.open(temp_path, mode='w', encoding='utf-8') as f:
                                await f.write(file_text)
                            fetched_data_map[file_id] = FileMetadata(
                                path=temp_path,
                                folder_id=record.get("folder_id"),
                                file_id=file_id,
                                title=record.get("filename"),
                            )
                            logger.debug(f"Successfully wrote file {file_id} to {temp_path}")
                        except Exception as e:
                            logger.warning(f"Could not write file {file_id} to temp path {temp_path}: {e}")
                    else:
                         logger.debug(f"File {file_id} found but had no content.")
        except Exception as db_error:
            logger.error(f"Error fetching files from database using cursor: {db_error}")
            raise db_error
        finally:
            if conn:
                await self.pool.release(conn)

        result_list: List[Optional[FileMetadata]] = [fetched_data_map.get(file_id) for file_id in file_ids]
        if exclude_nones:
            result_list = [item for item in result_list if item is not None]
        return result_list
    
    async def close(self):
        """Close the connection pool"""
        if self.pool:
            await self.pool.close()