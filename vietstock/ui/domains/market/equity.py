from __future__ import annotations

from typing import Any

from vietstock.ui._base import BaseDetailUI


class EquityMarket(BaseDetailUI):
    """Equity market data."""

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
        # Handle parameter aliases
        interval = kwargs.pop("resolution", interval)
        count_back = kwargs.pop("length", count)
        return self._dispatch(
            "equity_market",
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
        # Handle interval clash if any (intraday might use interval/resolution too)
        kwargs.pop("interval", None)
        return self._dispatch("equity_market", "trades", source=source, **kwargs)

    def quote(self, source: str = "kbs", **kwargs) -> Any:
        """Get in-session quote snapshot (source-delayed)."""
        return self._dispatch("equity_market", "quote", source=source, **kwargs)
