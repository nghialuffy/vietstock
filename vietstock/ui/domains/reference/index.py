from __future__ import annotations

from typing import Any

from vietstock.ui._base import BaseUI


class IndexReference(BaseUI):
    """Market index reference data."""

    def __init__(self, symbol: str = None, **kwargs):
        super().__init__(**kwargs)
        self.symbol = symbol

    def __call__(self, symbol: str = None) -> IndexReference:
        """Allow calling the domain object with a symbol."""
        self.symbol = self._normalize_symbol(symbol)
        return self

    def _normalize_symbol(self, symbol: str) -> str:
        """Normalize common index names (HOSE -> VNINDEX)."""
        if not symbol:
            return None
        mapping = {"HOSE": "VNINDEX", "HNX": "HNXINDEX", "UPCOM": "UPCOMINDEX"}
        return mapping.get(symbol.upper(), symbol.upper())

    def list(self, source: str = None) -> Any:
        """List all market indices."""
        return self._dispatch("Reference", "index", "list", source=source)

    def groups(self, source: str = None) -> Any:
        """List supported index groups (e.g., HOSE Indices, Sector Indices)."""
        return self._dispatch("Reference", "index", "groups", source=source)

    def members(self, symbol: str = None, source: str = None) -> Any:
        """List constituents/members of an index (e.g., VN30, HOSE, HNX)."""
        target = self._normalize_symbol(symbol or self.symbol)
        if not target:
            raise ValueError("Vui lòng cung cấp mã index (ví dụ: 'VN30', 'HOSE').")

        return self._dispatch(
            "Reference",
            "index",
            "members",
            group=target,
            source=source,
        )
