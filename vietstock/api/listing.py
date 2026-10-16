# vietstock/api/listing.py
from __future__ import annotations

from typing import Any

from vietstock.base import BaseAdapter, dynamic_method
from vietstock.core.utils.retry import api_retry


class Listing(BaseAdapter):
    _module_name = "listing"
    """
    Adapter for listing data:
      - all_symbols
      - symbols_by_industries
      - symbols_by_exchange
      - industries_icb
      - symbols_by_group
      - all_future_indices
      - all_government_bonds
      - all_covered_warrant
      - all_bonds

    Usage:
        lst = Listing(source="vci", random_agent=False, show_log=True)
        df = lst.all_symbols(to_df=True)
        df2 = lst.symbols_by_exchange(lang="en")
        idx = lst.industries_icb()
        group = lst.symbols_by_group(group="VN30")
        fu = lst.all_future_indices()
    """

    def __init__(
        self,
        source: str = "kbs",
        random_agent: bool = False,
        show_log: bool = False,
    ):
        # Lazy load to avoid deadlock
        from vietstock import _ensure_explorer_modules_loaded

        _ensure_explorer_modules_loaded()

        self.source = source
        self.random_agent = random_agent
        self.show_log = show_log

        # Validate the source to only accept vci or msn
        if source.lower() not in ["kbs", "vci", "msn"]:
            raise ValueError(
                "Lớp Listing chỉ nhận giá trị tham số source là 'KBS', 'VCI' hoặc 'MSN'.",
            )

        # BaseAdapter will discover vietstock.explorer.<real_source>.listing
        # and pass only the kwargs its __init__ accepts (random_agent, show_log).
        super().__init__(source=source, random_agent=random_agent, show_log=show_log)

    @api_retry
    @dynamic_method
    def all_symbols(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve all symbols (filtered to STOCK)."""
        pass

    @api_retry
    @dynamic_method
    def symbols_by_industries(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve symbols grouped by ICB industries."""
        pass

    @api_retry
    @dynamic_method
    def symbols_by_exchange(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve symbols by exchange/board."""
        pass

    @api_retry
    @dynamic_method
    def industries_icb(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve ICB code hierarchy and mapping."""
        pass

    @api_retry
    @dynamic_method
    def symbols_by_group(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve symbols by predefined group (VN30, HNX30, CW, etc.)."""
        pass

    @api_retry
    @dynamic_method
    def get_supported_groups(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve all supported index groups."""
        pass

    @dynamic_method
    def market_status(self, *args: Any, **kwargs: Any) -> Any:
        """Get live market status."""
        pass

    @dynamic_method
    def all_etf(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve all Exchange-Traded Funds (ETFs)."""
        pass

    @dynamic_method
    def search_symbol(self, *args: Any, **kwargs: Any) -> Any:
        """Search for symbols matching the query."""
        pass

    # @retry(
    #     stop=stop_after_attempt(Config.RETRIES),
    #     wait=wait_exponential(
    #         multiplier=Config.BACKOFF_MULTIPLIER,
    #         min=Config.BACKOFF_MIN,
    #         max=Config.BACKOFF_MAX
    #     )
    # )

    @dynamic_method
    def events_calendar(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve events calendar (dividends, AGM, etc.)."""
        pass

    @dynamic_method
    def info(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve detailed symbol/asset information."""
        pass

    # shortcuts that delegate to symbols_by_group
    @api_retry
    def all_future_indices(self, **kwargs: Any) -> Any:
        """Retrieve all futures indices (group='FU_INDEX')."""
        return self.symbols_by_group(group="FU_INDEX", **kwargs)

    @api_retry
    def all_government_bonds(self, **kwargs: Any) -> Any:
        """
        Retrieve all government bonds.

        Delegated to the provider rather than mapped onto a symbol group: there
        is no group code for government bonds, and a source that does not carry
        them (KBS) raises its own NotImplementedError telling the user to call
        all_bonds() for corporate bonds instead.
        """
        return self._delegate_to_provider("all_government_bonds", **kwargs)

    @api_retry
    def all_covered_warrant(self, **kwargs: Any) -> Any:
        """Retrieve all covered warrants (group='CW')."""
        return self.symbols_by_group(group="CW", **kwargs)

    @api_retry
    def all_bonds(self, **kwargs: Any) -> Any:
        """Retrieve all bonds (group='BOND')."""
        return self.symbols_by_group(group="BOND", **kwargs)

    def _delegate_to_provider(self, method_name: str, **kwargs: Any) -> Any:
        """
        Delegate method call to the provider.

        Args:
            method_name (str): Method name to call.
            **kwargs: Additional parameters.

        Returns:
            Any: Result from the provider.
        """
        # Standard vietstock implementation
        method = getattr(self.provider, method_name)
        return method(**kwargs)
