import os
import time
import asyncio
import copy
from typing import Dict, Optional, List

# Import necessary types
from ragchat.definitions import BatchStatusSummary, FileState, FileStatus
from ragchat.log import get_logger

logger = get_logger(__name__)


class BatchProgress:
    """Tracks the progress of a batch of file upserts and manages reporting."""
    def __init__(self, total_files: int):
        self.total_files = total_files
        self.file_states: Dict[str, FileState] = {}
        self._lock = asyncio.Lock()
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None

        # State for managing progress reporting frequency
        self._last_yielded_percentage: float = -1.0
        self._last_progress_summary: Optional[BatchStatusSummary] = None

    async def handle_file_state(self, file_state: FileState):
        """Processes an updated FileState object and updates the internal batch state."""
        async with self._lock:
            task_id = file_state.task_id
            previous_state = self.file_states.get(task_id)

            was_in_terminal_state = previous_state.is_terminal if previous_state else False

            # Update the internal state with the new FileState object
            self.file_states[task_id] = file_state

            is_now_in_terminal_state = file_state.is_terminal

            # Adjust the terminal state count based on the transition
            if not is_now_in_terminal_state and was_in_terminal_state:
                # File transitioned *out* of a terminal state (e.g., retry), decrement count
                logger.warning(f"File {file_state.file_path} transitioned from terminal state '{previous_state.status.value}' to '{file_state.status.value}'.")

            # If this is the first state update for any file, record the start time
            if self._start_time is None:
                 self._start_time = time.time()

            # Check if all files are done and record end time if so
            if sum(f.is_terminal for f in self.file_states.values()) == self.total_files and self._end_time is None:
                self._end_time = time.time()
                logger.info(f"Done: {self.total_files}/{self.total_files} files.")

    def _get_status_summary_unlocked(self) -> BatchStatusSummary:
        """Internal helper to get the status summary. Assumes the lock is already held."""
        current_time = time.time()
        elapsed_time = current_time - self._start_time if self._start_time else 0
        
        # states
        all_states = list(self.file_states.values())
        known_chunk_states = [s for s in all_states if s.total_chunks is not None] # Files where total chunks are known

        # 1. Chunk processing aggregates
        total_known_chunks = sum(s.total_chunks for s in known_chunk_states)
        avg_chunks_per_file = total_known_chunks / max(1.0, len(known_chunk_states))
        processed_chunks = sum(len(s.chunk_results) for s in all_states)
        avg_time_per_chunk = elapsed_time / max(1.0, processed_chunks)
        total_chunks_est = total_known_chunks + (self.total_files - len(known_chunk_states)) * avg_chunks_per_file

        # 2. Estimate remaining time and pct completed
        remaining_time = None
        current_percentage = 0.0
        if processed_chunks > 0:
            remaining_time = (total_chunks_est - processed_chunks) * avg_time_per_chunk
            current_percentage =  (processed_chunks / max(1.0, total_chunks_est))  * 100.0

        if self.total_files == 0:
            current_percentage = 100.0
        
        # Create and return the status summary model
        return BatchStatusSummary(
            total_files=self.total_files,
            files_done=sum(s.is_terminal for s in all_states),
            processing_files=sum(s.status == FileStatus.PROCESSING for s in all_states),
            percentage=round(min(100.0, max(0.0, current_percentage)), 2),
            elapsed_time=round(elapsed_time, 2),
            remaining_time=round(remaining_time, 2) if remaining_time is not None else None,
            file_states=copy.deepcopy(self.file_states)
        )

    async def get_status_summary(self) -> BatchStatusSummary:
        """Provides a summary dictionary of the current batch state."""
        async with self._lock:
            return self._get_status_summary_unlocked()

    async def maybe_get_progress_update(self, with_files: bool = False) -> Optional[str]:
        """
        Checks if a progress update is needed based on internal state changes
        and returns a formatted progress string if so, otherwise None.
        """
        async with self._lock:
            current_summary = self._get_status_summary_unlocked()
            current_percentage = current_summary.percentage

            # Determine if we should yield a progress message based on various conditions
            yield_needed = (
                self._last_progress_summary is None # Always yield the first update
                or current_percentage >= 100.0 # Always yield the final update
                or current_summary.files_done > (self._last_progress_summary.files_done if self._last_progress_summary else -1) # Yield if a file finished
                or current_summary.processing_files != (self._last_progress_summary.processing_files if self._last_progress_summary else -1) # Yield if processing count changes
                or (current_percentage - self._last_yielded_percentage) >= 1.0 # Yield if percentage increased by 1% or more
            )

            if yield_needed:
                chunk = self.format_progress_chunk(current_summary, with_files)
                self._last_yielded_percentage = current_percentage
                self._last_progress_summary = current_summary # Store the summary that was actually yielded
                return chunk
            else:
                return None

    async def get_non_terminal_file_paths(self) -> List[str]:
        """
        Gets a list of file paths not currently in a terminal state.
        Returns paths that have reported state and are not terminal.
        Assumes self.file_states contains all files once their state is first reported.
        """
        async with self._lock:
            # Filter file states to find those not in a terminal state
            return [fp for fp, state in self.file_states.items() if not state.is_terminal]
        
    def format_time(self, seconds: float) -> str:
        """Formats seconds into a human-readable string (e.g., 1m 30s)."""
        if seconds is None or seconds < 0: return "N/A"
        if seconds < 60: return f"{int(seconds)}s"
        if seconds < 3600: return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        return f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m"

    def format_progress_chunk(self, summary: BatchStatusSummary, with_files: bool = False) -> str:
        """
        Formats the batch progress summary into an OpenAI-like chat completion chunk.
        Includes file statuses if available (for the final update).
        """
        lines = []

        # Add overall progress line
        overall_progress_parts = [
            f"`{summary.percentage:.0f}%",
            f"Files: {summary.files_done}/{summary.total_files} done ({summary.processing_files} processing)",
            f"Time elapsed: {self.format_time(summary.elapsed_time)}",
        ]
        if summary.remaining_time is not None:
            overall_progress_parts.append(f"Remaining: {self.format_time(summary.remaining_time)}")

        # Join overall parts and add to lines. Note: Removed the final '`\n`' from the original.
        lines.append(" - ".join(overall_progress_parts) + "`")

        # Add file statuses if the dictionary is not empty
        if with_files and summary.file_states:
            lines.append("\nFiles:") # Add a header/separator line
            sorted_task_ids = summary.file_states.keys()
            for task_id in sorted_task_ids:
                file_state = summary.file_states[task_id]
                # Format the status line
                status_str = file_state.status.value.capitalize()
                successful_chunks = sum(not c.error for c in file_state.chunk_results)
                file_line = f"`{status_str:<10} (Successful chunks: {successful_chunks:>3}/{(file_state.total_chunks or 0):>3}) - {os.path.basename(file_state.file_path)}`"

                lines.append(file_line)

        # Join all collected lines with newlines and add a final newline
        return "\n".join(lines) + "\n"
