"""
UI Module - Unified Interface for vietstock
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from vietstock.ui.broker import Broker
    from vietstock.ui.fundamental import Fundamental
    from vietstock.ui.market import Market
    from vietstock.ui.reference import Reference
    from vietstock.ui.retail import Retail

__all__ = ["Reference", "Market", "Fundamental", "Retail", "Broker"]


def __getattr__(name: str) -> Any:
    """
    Lazy load UI modules using PEP 562.
    Allows IDE autocomplete and type hints to work correctly.
    """
    if name == "Reference":
        from vietstock.ui.reference import Reference as _Reference

        return _Reference
    elif name == "Market":
        from vietstock.ui.market import Market as _Market

        return _Market
    elif name == "Fundamental":
        from vietstock.ui.fundamental import Fundamental as _Fundamental

        return _Fundamental
    elif name == "Retail":
        from vietstock.ui.retail import Retail as _Retail

        return _Retail
    elif name == "Broker":
        from vietstock.ui.broker import Broker as _Broker

        return _Broker
    elif name == "show_api":
        from vietstock.ui.helper import show_api as _show_api

        return _show_api
    elif name == "show_doc":
        from vietstock.ui.helper import show_doc as _show_doc

        return _show_doc

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
