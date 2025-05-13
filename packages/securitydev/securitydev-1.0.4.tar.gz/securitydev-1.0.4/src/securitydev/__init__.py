"""
securitydev - A modern Python client for the security.dev API.
Provides both synchronous (default) and asynchronous clients.
"""

__version__ = "1.0.4"

from .async_client import AsyncSecurityClient  # Async client
from .client import SecurityClient  # Default Sync client
from .exceptions import SecurityDevApiError, SecurityDevError

# Make primary classes and exceptions easily accessible
__all__ = [
    "SecurityClient",
    "AsyncSecurityClient",
    "SecurityDevError",
    "SecurityDevApiError",
    "ip_intel",
    "user_intel",
]

# Global default client for module-level access
_default_client = None

def _get_default_client():
    """Get or initialize the default client for module-level access."""
    global _default_client
    if _default_client is None:
        from os import environ
        key = environ.get("SECURITYDEV_KEY")
        if not key:
            raise SecurityDevError("No API key found. Set SECURITYDEV_KEY environment variable or use SecurityClient directly.")
        _default_client = SecurityClient(key=key)
    return _default_client

# Create proxy objects for module-level access
class _NamespaceProxy:
    """Base proxy for module-level access to API endpoints."""
    _namespace_attr = None

    def __getattr__(self, name):
        client = _get_default_client()
        namespace = getattr(client, self._namespace_attr)
        return getattr(namespace, name)

class _IpIntelProxy(_NamespaceProxy):
    """Proxy for module-level access to IP intel endpoints."""
    _namespace_attr = "ip_intel"

class _UserIntelProxy(_NamespaceProxy):
    """Proxy for module-level access to User intel endpoints."""
    _namespace_attr = "user_intel"

# Export these as module-level attributes
ip_intel = _IpIntelProxy()
user_intel = _UserIntelProxy()
