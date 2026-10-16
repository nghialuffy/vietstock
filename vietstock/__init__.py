"""
vietstock: fetch and standardise Vietnamese stock market data.

This is the free package. Extended features (derivatives price board, longer
financial statement history, odd-lot prices...) live in `vnstock_data`, the sponsor
package, which mirrors the classes and arguments here: switching
`from vietstock import ...` to `from vnstock_data import ...` is enough.
"""

# Lazy import Vietstock to avoid circular import deadlock
from __future__ import annotations

_Vietstock = None


def _get_vietstock():
    """Lazy load Vietstock class."""
    global _Vietstock
    if _Vietstock is None:
        from vietstock.common.client import Vietstock as _VietstockClass

        _Vietstock = _VietstockClass
    return _Vietstock


# Create a lazy proxy for Vietstock
class Vietstock:
    """Lazy proxy for vietstock.common.client.Vietstock to avoid circular import."""

    def __new__(cls, *args, **kwargs):
        actual_class = _get_vietstock()
        return actual_class(*args, **kwargs)


# Use standard vietstock classes
# Load UI and helper classes
from vietstock.ui import (  # noqa: E402
    Broker,
    Fundamental,
    Market,
    Reference,
    Retail,
    show_api,
    show_doc,
)

from .api.company import Company  # noqa: E402
from .api.financial import Finance  # noqa: E402
from .api.listing import Listing  # noqa: E402
from .api.quote import Quote  # noqa: E402
from .api.trading import Trading  # noqa: E402
from .explorer.fmarket import Fund  # noqa: E402

show_docs = show_doc  # Alias for better parity


# Market constants
# Load connector modules to register providers
from . import connector  # noqa: E402
from .constants import (  # noqa: E402
    EXCHANGES,
    INDEX_GROUPS,
    INDICES_INFO,
    INDICES_MAP,
    SECTOR_IDS,
)

# Load explorer modules to register providers (lazy to avoid deadlock)
_explorer_modules_loaded = False


def _ensure_explorer_modules_loaded():
    """Lazy load explorer modules to avoid circular import deadlock."""
    global _explorer_modules_loaded
    if _explorer_modules_loaded:
        return
    try:
        from .explorer import kbs, msn, vci  # noqa: F401

        _explorer_modules_loaded = True
    except Exception as e:
        _explorer_modules_loaded = True  # Mark as loaded to avoid retry loops
        import warnings

        warnings.warn(f"Failed to load explorer modules: {e}", stacklevel=2)


__all__ = [
    "Vietstock",
    "Quote",
    "Listing",
    "Company",
    "Finance",
    "Trading",
    "Fund",
    "ui",
    "show_api",
    "show_doc",
    "Reference",
    "Market",
    "Fundamental",
    "Retail",
    "Broker",
    "connector",
    "INDICES_INFO",
    "INDICES_MAP",
    "INDEX_GROUPS",
    "SECTOR_IDS",
    "EXCHANGES",
]
