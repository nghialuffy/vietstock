from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vietstock.ui.domains.reference.bond import BondReference
    from vietstock.ui.domains.reference.company import CompanyReference
    from vietstock.ui.domains.reference.equity import EquityReference
    from vietstock.ui.domains.reference.etf import ETFReference
    from vietstock.ui.domains.reference.events import EventsReference
    from vietstock.ui.domains.reference.fund import FundReference
    from vietstock.ui.domains.reference.futures import FuturesReference
    from vietstock.ui.domains.reference.index import IndexReference
    from vietstock.ui.domains.reference.industry import IndustryReference
    from vietstock.ui.domains.reference.market import MarketReference
    from vietstock.ui.domains.reference.reports import ReportsReference
    from vietstock.ui.domains.reference.search import SearchReference
    from vietstock.ui.domains.reference.warrant import WarrantReference


class Reference:
    """
    Reference Data Layer (Layer 1).
    """

    @property
    def bond(self) -> BondReference:
        """Access bond reference data."""
        from vietstock.ui.domains.reference.bond import BondReference

        return BondReference()

    def company(self, symbol: str = None) -> CompanyReference:
        """Access company-specific reference data."""
        from vietstock.ui.domains.reference.company import CompanyReference

        return CompanyReference(symbol=symbol)

    @property
    def equity(self) -> EquityReference:
        """Access equity reference data."""
        from vietstock.ui.domains.reference.equity import EquityReference

        return EquityReference()

    @property
    def etf(self) -> ETFReference:
        """Access ETF reference data."""
        from vietstock.ui.domains.reference.etf import ETFReference

        return ETFReference()

    @property
    def events(self) -> EventsReference:
        """Access events reference data."""
        from vietstock.ui.domains.reference.events import EventsReference

        return EventsReference()

    @property
    def fund(self) -> FundReference:
        """Master data for Mutual Funds."""
        from vietstock.ui.domains.reference.fund import FundReference

        return FundReference()

    def futures(self, symbol: str = None) -> FuturesReference:
        """Access index futures reference data."""
        from vietstock.ui.domains.reference.futures import FuturesReference

        return FuturesReference(symbol=symbol)

    @property
    def index(self) -> IndexReference:
        """Access index reference data."""
        from vietstock.ui.domains.reference.index import IndexReference

        return IndexReference()

    @property
    def industry(self) -> IndustryReference:
        """Access industry reference data."""
        from vietstock.ui.domains.reference.industry import IndustryReference

        return IndustryReference()

    @property
    def market(self) -> MarketReference:
        """Access live market status."""
        from vietstock.ui.domains.reference.market import MarketReference

        return MarketReference()

    @property
    def search(self) -> SearchReference:
        """Access global symbol search."""
        from vietstock.ui.domains.reference.search import SearchReference

        return SearchReference()

    @property
    def reports(self) -> ReportsReference:
        """Access research reports published by the data sources."""
        from vietstock.ui.domains.reference.reports import ReportsReference

        return ReportsReference()

    def warrant(self, symbol: str = None) -> WarrantReference:
        """Access covered warrant reference data."""
        from vietstock.ui.domains.reference.warrant import WarrantReference

        return WarrantReference(symbol=symbol)
