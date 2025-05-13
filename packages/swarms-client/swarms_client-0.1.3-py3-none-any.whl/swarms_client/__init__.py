"""
Swarms API Client Package

This package provides a production-grade client for interacting with the Swarms API.
"""

from .client import (
    SwarmsClient,
    SwarmsError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
)
from .config import SwarmsConfig

__all__ = [
    "SwarmsClient",
    "SwarmsConfig",
    "SwarmsError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "APIError",
]

__version__ = "0.1.0"
