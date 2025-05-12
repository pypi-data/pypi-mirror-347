try:
    from ._version import version

    __version__ = version
except ImportError:
    __version__ = "0.0.0"

from .client import Client  # noqa: F401
from .error import APIError, RateLimitError  # noqa: F401
from .iterator import SearchIterator  # noqa: F401
