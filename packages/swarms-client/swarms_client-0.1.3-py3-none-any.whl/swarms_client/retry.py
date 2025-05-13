"""
Retry handler module for Swarms API client.

This module provides retry functionality with exponential backoff for API requests.
"""

import asyncio
import random
from typing import Callable, Optional, Set, TypeVar, Any, Dict
from loguru import logger

from .config import SwarmsConfig

T = TypeVar("T")


class RetryHandler:
    """Handles retry logic with exponential backoff for API requests."""

    def __init__(
        self,
        max_retries: int = SwarmsConfig.DEFAULT_MAX_RETRIES,
        retry_delay: float = SwarmsConfig.DEFAULT_RETRY_DELAY,
        max_retry_delay: int = SwarmsConfig.DEFAULT_MAX_RETRY_DELAY,
        retry_on_status: Optional[Set[int]] = None,
        jitter: bool = True,
    ):
        """
        Initialize retry handler with optimized settings.

        Args:
            max_retries (int): Maximum number of retry attempts
            retry_delay (float): Initial delay between retries in seconds
            max_retry_delay (int): Maximum delay between retries in seconds
            retry_on_status (Optional[Set[int]]): HTTP status codes to retry on
            jitter (bool): Whether to add random jitter to retry delays
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_retry_delay = max_retry_delay
        self.retry_on_status = retry_on_status or set(
            SwarmsConfig.DEFAULT_RETRY_ON_STATUS
        )
        self.jitter = jitter

        # Track retry statistics
        self.retry_stats: Dict[str, int] = {
            "total_retries": 0,
            "successful_retries": 0,
            "failed_retries": 0,
        }

    def calculate_delay(self, attempt: int, error_type: Optional[str] = None) -> float:
        """
        Calculate optimized delay for current retry attempt.

        Args:
            attempt (int): Current retry attempt number
            error_type (Optional[str]): Type of error that triggered the retry

        Returns:
            float: Delay in seconds
        """
        # Base exponential backoff
        delay = min(self.retry_delay * (1.5 ** (attempt - 1)), self.max_retry_delay)

        # Adjust delay based on error type
        if error_type == "rate_limit":
            # Add extra delay for rate limit errors
            delay *= 1.5
        elif error_type == "timeout":
            # Reduce delay for timeout errors as they might be temporary
            delay *= 0.8
        elif error_type == "server_error":
            # Standard delay for server errors
            pass

        # Add controlled jitter to prevent thundering herd
        if self.jitter:
            jitter_range = min(delay * 0.2, 1.0)  # Max 1 second jitter
            delay += random.uniform(-jitter_range, jitter_range)

        return max(delay, self.retry_delay)  # Ensure minimum delay

    def should_retry(
        self, exception: Exception, attempt: int
    ) -> tuple[bool, Optional[str]]:
        """
        Determine if retry should be attempted based on exception.

        Args:
            exception: The exception that occurred
            attempt: Current attempt number

        Returns:
            tuple[bool, Optional[str]]: (should_retry, error_type)
        """
        if attempt > self.max_retries:
            return False, None

        if hasattr(exception, "status"):
            status = getattr(exception, "status")
            if status in self.retry_on_status:
                error_type = None
                if status == 429:
                    error_type = "rate_limit"
                elif status in {408, 504}:
                    error_type = "timeout"
                elif status >= 500:
                    error_type = "server_error"
                return True, error_type

        return False, None

    async def execute_with_retry(
        self, func: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """
        Execute function with optimized retry logic.

        Args:
            func (Callable): Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            T: Function result

        Raises:
            Exception: If all retries fail
        """
        last_exception = None
        start_time = asyncio.get_event_loop().time()

        for attempt in range(1, self.max_retries + 2):  # +2 for initial try
            try:
                result = await func(*args, **kwargs)

                # Log success after retries
                if attempt > 1:
                    self.retry_stats["successful_retries"] += 1
                    duration = asyncio.get_event_loop().time() - start_time
                    logger.info(
                        f"Request succeeded after {attempt-1} retries in {duration:.2f}s"
                    )

                return result

            except Exception as e:
                last_exception = e
                self.retry_stats["total_retries"] += 1

                should_retry, error_type = self.should_retry(e, attempt)
                if not should_retry:
                    self.retry_stats["failed_retries"] += 1
                    if attempt > 1:
                        logger.error(
                            f"Request failed after {attempt-1} retries: {str(e)}"
                        )
                    raise

                delay = self.calculate_delay(attempt, error_type)
                logger.warning(
                    f"Attempt {attempt} failed ({error_type or 'unknown error'}): {str(e)}. "
                    f"Retrying in {delay:.2f}s..."
                )

                await asyncio.sleep(delay)

        # This should never be reached due to the raise in the loop
        raise last_exception if last_exception else Exception("Retry failed")
