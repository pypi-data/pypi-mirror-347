"""
securitydev - A modern Python client for the security.dev API.
Provides both synchronous (default) and asynchronous clients.
"""

__version__ = "1.0.2"

from .async_client import AsyncSecurityClient  # Async client
from .client import SecurityClient  # Default Sync client
from .exceptions import SecurityDevApiError, SecurityDevError
from .models import ip_intel, user_intel

# Make primary classes and exceptions easily accessible
__all__ = [
    "SecurityClient",
    "AsyncSecurityClient",
    "SecurityDevError",
    "SecurityDevApiError",
    "ip_intel",
    "user_intel",
]
