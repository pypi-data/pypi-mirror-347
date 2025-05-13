"""logctx package

This package provides a convenient way to manage logging contexts in Python.

It allows you to manage key-value pairs for log-contexts which can be automatically
added to log messages within their respective context.
"""

__author__ = "Alexander Schulte"
__maintainer__ = "Alexander Schulte"

__version__ = "0.4.0"

from logctx import decorators
from logctx._core import (
    ContextInjectingLoggingFilter,
    LogContext,
    clear,
    get_current,
    new_context,
    update,
)

__all__ = [
    "ContextInjectingLoggingFilter",
    "LogContext",
    "clear",
    "get_current",
    "new_context",
    "update",
    "decorators",
]
