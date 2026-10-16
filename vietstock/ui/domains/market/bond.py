from __future__ import annotations

from typing import Any

from vietstock.ui._base import BaseDetailUI


class BondMarket(BaseDetailUI):
    """Bond market data."""

    def ohlcv(
        self,
        start: str | None = None,
        end: str | None = None,
        interval: str = "1D",
        count: int = 100,
        source: str = "kbs",
        **kwargs,
    ) -> Any:
        """Get historical OHLCV data."""
        interval = kwargs.pop("resolution", interval)
        count_back = kwargs.pop("length", count)
        return self._dispatch(
            "bond_market",
            "ohlcv",
            start=start,
            end=end,
            interval=interval,
            count_back=count_back,
            source=source,
            **kwargs,
        )

    def trades(self, source: str = "kbs", **kwargs) -> Any:
        """Get intraday trades."""
        kwargs.pop("interval", None)
        return self._dispatch("bond_market", "trades", source=source, **kwargs)

    def quote(self, source: str = "kbs", **kwargs) -> Any:
        """Get in-session quote snapshot (source-delayed)."""
        return self._dispatch("bond_market", "quote", source=source, **kwargs)
