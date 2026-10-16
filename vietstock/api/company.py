# vietstock/api/company.py
from __future__ import annotations

from typing import Any

from vietstock.base import BaseAdapter, dynamic_method
from vietstock.core.utils.retry import api_retry


class Company(BaseAdapter):
    _module_name = "company"
    """
    Adapter for company-related data:
      - overview
      - shareholders
      - officers
      - subsidiaries
      - affiliate
      - news
      - events

    Usage:
        c = Company(source="vci", symbol="VCI", random_agent=False, show_log=True)
        df_ov = c.overview()
        df_sh = c.shareholders()
        df_of = c.officers(filter_by="all")
        df_sub = c.subsidiaries(filter_by="subsidiary")
        df_aff = c.affiliate()
        df_news = c.news()
        df_evt = c.events()
    """

    def __init__(
        self,
        source: str = "KBS",
        symbol: str = None,
        random_agent: bool = False,
        show_log: bool = False,
    ):
        # Lazy load to avoid deadlock
        from vietstock import _ensure_explorer_modules_loaded

        _ensure_explorer_modules_loaded()

        self.source = source
        self.symbol = symbol if symbol else ""
        self.random_agent = random_agent
        self.show_log = show_log

        # Validate the source to only accept kbs, vci
        if source.lower() not in ["kbs", "vci"]:
            raise ValueError(
                "Lớp Company chỉ nhận giá trị tham số source là 'VCI' hoặc 'KBS'.",
            )

        # BaseAdapter will discover vietstock.explorer.<real_source>.company
        # and pass only the kwargs its __init__ accepts (random_agent, show_log).
        super().__init__(
            source=source,
            symbol=symbol,
            random_agent=random_agent,
            show_log=show_log,
        )

    @api_retry
    @dynamic_method
    def overview(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company overview data."""
        pass

    def info(self, *args: Any, **kwargs: Any) -> Any:
        """Alias for overview() to match vnstock_data parity."""
        return self.overview(*args, **kwargs)

    @api_retry
    @dynamic_method
    def shareholders(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company shareholders data."""
        pass

    @api_retry
    @dynamic_method
    def officers(self, *args: Any, **kwargs: Any) -> Any:
        """
        Retrieve company officers data.
        Supports kwargs like filter_by='working'|'resigned'|'all'.
        """
        pass

    @api_retry
    @dynamic_method
    def subsidiaries(self, *args: Any, **kwargs: Any) -> Any:
        """
        Retrieve company subsidiaries data.
        Supports kwargs like filter_by='all'|'subsidiary'.
        """
        pass

    @api_retry
    @dynamic_method
    def affiliate(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company affiliate data."""
        pass

    @api_retry
    @dynamic_method
    def news(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company news."""
        pass

    @api_retry
    @dynamic_method
    def events(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company events."""
        pass

    @api_retry
    @dynamic_method
    def ownership(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company ownership structure."""
        pass

    @api_retry
    @dynamic_method
    def capital_history(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company capital change history."""
        pass

    @api_retry
    @dynamic_method
    def insider_trading(self, *args: Any, **kwargs: Any) -> Any:
        """Retrieve company insider trading history."""
        pass

    def _delegate_to_provider(
        self,
        method_name: str,
        symbol: str = None,
        **kwargs: Any,
    ) -> Any:
        """
        Delegate method call to the provider with symbol update if needed.

        Args:
            method_name (str): Method name to call.
            symbol (str, optional): Symbol to use.
            **kwargs: Additional parameters.

        Returns:
            Any: Result from the provider.
        """
        # Standard vietstock implementation
        original_symbol = None
        try:
            if symbol:
                original_symbol = self.symbol
                self.symbol = symbol.upper()
                self._update_provider()

            # Get the method from the provider
            method = getattr(self.provider, method_name)
            return method(**kwargs)
        finally:
            if original_symbol:
                self.symbol = original_symbol
                self._update_provider()
