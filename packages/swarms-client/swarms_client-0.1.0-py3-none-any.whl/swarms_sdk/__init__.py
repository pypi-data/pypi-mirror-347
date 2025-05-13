"""
Swarms SDK - A production-grade Python client for the Swarms API.

This package provides a simple and intuitive interface for creating and managing AI swarms.
"""

from .client import (
    SwarmsClient,
    SwarmsError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
)

__version__ = "0.1.0"

__all__ = [
    "SwarmsClient",
    "SwarmsError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "APIError",
]
