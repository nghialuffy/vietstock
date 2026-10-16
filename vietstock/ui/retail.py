from __future__ import annotations


class Retail:
    """
    Retail Data Layer for vietstock (Gold, Exchange Rates).
    """

    def __init__(self):
        from vietstock.ui.domains.retail.commodity import Retail as RetailDomain

        self._retail = RetailDomain()

    def gold(self, source: str = "sjc", date: str = None):
        """Access gold price data."""
        return self._retail.gold(source=source, date=date)

    def exchange_rate(self, date: str = ""):
        """Access exchange rate data."""
        return self._retail.exchange_rate(date=date)
