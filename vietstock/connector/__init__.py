"""
vietstock connectors.

Provides connectors to various data sources for financial data.
"""

# Import submodules to trigger provider registration
from __future__ import annotations

from . import fmp  # noqa: F401
from .fmp import Quote as FMPQuote

# For direct imports

__all__ = ["fmp", "FMPQuote"]
