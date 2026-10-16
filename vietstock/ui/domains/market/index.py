from __future__ import annotations

from typing import Any

from vietstock.ui._base import BaseDetailUI


class IndexMarket(BaseDetailUI):
    """Index market data."""

    def ohlcv(
        self,
        start: str | None = None,
        end: str | None = None,
        interval: str = "1D",
        count: int = 100,
        source: str = "kbs",
        **kwargs,
    ) -> Any:
        """Historical OHLCV bars for indices."""
        # Handle parameter aliases
        interval = kwargs.pop("resolution", interval)
        count_back = kwargs.pop("length", count)

        # Switch source for global indices if scope is global
        if self.params.get("scope") == "global" and source == "kbs":
            source = "msn"

        return self._dispatch(
            "Market",
            "index",
            "ohlcv",
            start=start,
            end=end,
            interval=interval,
            count_back=count_back,
            source=source,
            **kwargs,
        )
