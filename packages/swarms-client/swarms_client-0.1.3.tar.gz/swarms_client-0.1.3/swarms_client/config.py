"""
Configuration module for Swarms API client.

This module handles API settings, defaults, and environment configuration.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SwarmsConfig:
    """Configuration class for Swarms API client."""

    # Default values - optimized for performance
    DEFAULT_BASE_URL = "https://swarms-api-285321057562.us-east1.run.app"
    ALTERNATE_BASE_URL = "https://swarms-api-285321057562.us-east1.run.app"
    DEFAULT_TIMEOUT = 120  # Increased timeout for reliability
    DEFAULT_MAX_RETRIES = 5  # Increased retries
    DEFAULT_RETRY_DELAY = 0.5  # Reduced initial delay
    DEFAULT_MAX_RETRY_DELAY = 10  # Reduced max delay
    DEFAULT_RETRY_ON_STATUS = [408, 429, 500, 502, 503, 504]  # Added 408 timeout
    DEFAULT_KEEPALIVE_TIMEOUT = 30  # Keep connections alive
    DEFAULT_MAX_CONCURRENT_REQUESTS = 25  # Increased concurrency
    DEFAULT_DNS_CACHE_TTL = 300  # 5 minutes DNS cache
    DEFAULT_TCP_NODELAY = True  # Disable Nagle's algorithm
    DEFAULT_RESPONSE_CACHE_TTL = 60  # 1 minute response cache

    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        Get API key from environment variables.

        Returns:
            Optional[str]: API key if found, None otherwise
        """
        return os.getenv("SWARMS_API_KEY")

    @staticmethod
    def get_base_url() -> str:
        """
        Get base URL from environment variables or use default.

        Returns:
            str: Base URL for API requests
        """
        return os.getenv("SWARMS_API_BASE_URL", SwarmsConfig.DEFAULT_BASE_URL)

    @staticmethod
    def get_timeout() -> int:
        """
        Get request timeout from environment variables or use default.

        Returns:
            int: Timeout in seconds
        """
        return int(os.getenv("SWARMS_API_TIMEOUT", SwarmsConfig.DEFAULT_TIMEOUT))

    @staticmethod
    def get_max_retries() -> int:
        """
        Get maximum retries from environment variables or use default.

        Returns:
            int: Maximum number of retries
        """
        return int(
            os.getenv("SWARMS_API_MAX_RETRIES", SwarmsConfig.DEFAULT_MAX_RETRIES)
        )

    @staticmethod
    def get_retry_delay() -> float:
        """
        Get initial retry delay from environment variables or use default.

        Returns:
            float: Retry delay in seconds
        """
        return float(
            os.getenv("SWARMS_API_RETRY_DELAY", SwarmsConfig.DEFAULT_RETRY_DELAY)
        )

    @staticmethod
    def get_max_retry_delay() -> int:
        """
        Get maximum retry delay from environment variables or use default.

        Returns:
            int: Maximum retry delay in seconds
        """
        return int(
            os.getenv(
                "SWARMS_API_MAX_RETRY_DELAY", SwarmsConfig.DEFAULT_MAX_RETRY_DELAY
            )
        )

    @staticmethod
    def get_keepalive_timeout() -> int:
        """Get keepalive timeout from environment variables or use default."""
        return int(
            os.getenv(
                "SWARMS_API_KEEPALIVE_TIMEOUT", SwarmsConfig.DEFAULT_KEEPALIVE_TIMEOUT
            )
        )

    @staticmethod
    def get_max_concurrent_requests() -> int:
        """Get max concurrent requests from environment variables or use default."""
        return int(
            os.getenv(
                "SWARMS_API_MAX_CONCURRENT_REQUESTS",
                SwarmsConfig.DEFAULT_MAX_CONCURRENT_REQUESTS,
            )
        )

    @staticmethod
    def get_dns_cache_ttl() -> int:
        """Get DNS cache TTL from environment variables or use default."""
        return int(
            os.getenv("SWARMS_API_DNS_CACHE_TTL", SwarmsConfig.DEFAULT_DNS_CACHE_TTL)
        )

    @staticmethod
    def get_tcp_nodelay() -> bool:
        """Get TCP_NODELAY setting from environment variables or use default."""
        return bool(
            os.getenv("SWARMS_API_TCP_NODELAY", SwarmsConfig.DEFAULT_TCP_NODELAY)
        )

    @staticmethod
    def get_response_cache_ttl() -> int:
        """Get response cache TTL from environment variables or use default."""
        return int(
            os.getenv(
                "SWARMS_API_RESPONSE_CACHE_TTL", SwarmsConfig.DEFAULT_RESPONSE_CACHE_TTL
            )
        )
