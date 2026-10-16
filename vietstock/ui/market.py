from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vietstock.ui._base import BaseUI

if TYPE_CHECKING:
    from vietstock.ui.domains.market.bond import BondMarket
    from vietstock.ui.domains.market.commodity_market import CommodityMarket
    from vietstock.ui.domains.market.crypto import CryptoMarket
    from vietstock.ui.domains.market.equity import EquityMarket
    from vietstock.ui.domains.market.etf import ETFMarket
    from vietstock.ui.domains.market.forex import ForexMarket
    from vietstock.ui.domains.market.fund import FundMarket
    from vietstock.ui.domains.market.futures import FuturesMarket
    from vietstock.ui.domains.market.index import IndexMarket
    from vietstock.ui.domains.market.warrant import WarrantMarket


class Market(BaseUI):
    """
    Market Data Layer (Layer 2).
    """

    def quote(self, symbol: Any = None, **kwargs) -> Any:
        """Global in-session quote for one or more symbols (source-delayed)."""
        if symbol is None:
            raise ValueError("Tham số 'symbol' là bắt buộc cho phương thức quote().")
        return self._dispatch("Market", "quote", symbols_list=symbol, **kwargs)

    def equity(self, symbol: str = None, **kwargs) -> EquityMarket:
        """Access equity market data."""
        from vietstock.ui.domains.market.equity import EquityMarket

        return EquityMarket(symbol=symbol, **kwargs)

    def index(self, symbol: str = None, **kwargs) -> IndexMarket:
        """Access index market data."""
        from vietstock.ui.domains.market.index import IndexMarket

        return IndexMarket(symbol=symbol, **kwargs)

    def etf(self, symbol: str = None, **kwargs) -> ETFMarket:
        """Access ETF market data."""
        from vietstock.ui.domains.market.etf import ETFMarket

        return ETFMarket(symbol=symbol, **kwargs)

    def futures(self, symbol: str = None, **kwargs) -> FuturesMarket:
        """Access futures market data."""
        from vietstock.ui.domains.market.futures import FuturesMarket

        return FuturesMarket(symbol=symbol, **kwargs)

    def warrant(self, symbol: str = None, **kwargs) -> WarrantMarket:
        """Access warrant market data."""
        from vietstock.ui.domains.market.warrant import WarrantMarket

        return WarrantMarket(symbol=symbol, **kwargs)

    def fund(self, symbol: str = None, **kwargs) -> FundMarket:
        """Access Mutual Fund market data."""
        from vietstock.ui.domains.market.fund import FundMarket

        return FundMarket(symbol=symbol, **kwargs)

    def crypto(self, symbol: str = None, **kwargs) -> CryptoMarket:
        """Access crypto market data."""
        from vietstock.ui.domains.market.crypto import CryptoMarket

        return CryptoMarket(symbol=symbol, **kwargs)

    def forex(self, symbol: str = None, **kwargs) -> ForexMarket:
        """Access forex market data."""
        from vietstock.ui.domains.market.forex import ForexMarket

        return ForexMarket(symbol=symbol, **kwargs)

    def commodity(self, symbol: str = None, **kwargs) -> CommodityMarket:
        """Access commodity market data."""
        from vietstock.ui.domains.market.commodity_market import CommodityMarket

        return CommodityMarket(symbol=symbol, **kwargs)

    def bond(self, symbol: str = None, **kwargs) -> BondMarket:
        """Access bond market data."""
        from vietstock.ui.domains.market.bond import BondMarket

        return BondMarket(symbol=symbol, **kwargs)
