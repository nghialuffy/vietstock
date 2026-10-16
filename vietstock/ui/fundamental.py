from __future__ import annotations


class Fundamental:
    """
    Fundamental Data Layer (Layer 3).
    """

    def equity(self, symbol: str):
        """Access equity fundamental data."""
        from vietstock.ui.domains.fundamental.equity import EquityFundamental

        return EquityFundamental(symbol=symbol)
