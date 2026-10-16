"""
Integration tests for Vietstock main client interface.

Tests end-to-end workflows using the Vietstock class.
"""

from __future__ import annotations

import pytest

from vietstock.common.client import Vietstock


@pytest.mark.integration
class TestVietstockClient:
    """Test suite for Vietstock main client."""

    def test_vietstock_instantiation(self):
        """Test Vietstock can be instantiated."""
        stock = Vietstock(show_log=False)
        assert stock is not None

    def test_vietstock_stock_method(self):
        """Test Vietstock.stock() method."""
        stock = Vietstock(show_log=False)
        acb = stock.stock("ACB", source="VCI")
        assert acb is not None
        assert hasattr(acb, "quote")
        assert hasattr(acb, "company")
        assert hasattr(acb, "finance")

    def test_vietstock_stock_components_quote(self):
        """Test StockComponents has working quote component."""
        stock = Vietstock(show_log=False)
        acb = stock.stock("ACB", source="VCI")
        assert hasattr(acb.quote, "history")

    def test_vietstock_stock_components_company(self):
        """Test StockComponents has working company component."""
        stock = Vietstock(show_log=False)
        acb = stock.stock("ACB", source="VCI")
        assert hasattr(acb.company, "overview")
        assert hasattr(acb.company, "profile")

    def test_vietstock_stock_components_finance(self):
        """Test StockComponents has working finance component."""
        stock = Vietstock(show_log=False)
        acb = stock.stock("ACB", source="VCI")
        assert hasattr(acb.finance, "balance_sheet")
        assert hasattr(acb.finance, "income_statement")
        assert hasattr(acb.finance, "cash_flow")

    def test_vietstock_supported_sources(self):
        """Test Vietstock supports expected sources."""
        expected_sources = ["KBS", "VCI", "MSN"]
        assert expected_sources == Vietstock.SUPPORTED_SOURCES

    @pytest.mark.parametrize("source", ["VCI", "KBS"])
    def test_vietstock_stock_with_different_sources(self, source):
        """Test Vietstock.stock() works with different sources."""
        stock = Vietstock(show_log=False)
        acb = stock.stock("ACB", source=source)
        assert acb is not None
        assert acb.source.upper() == source

    def test_vietstock_fx_method(self):
        """Test Vietstock.fx() method for forex data."""
        stock = Vietstock(show_log=False)
        fx = stock.fx("USDVND", source="MSN")
        assert fx is not None
        assert hasattr(fx, "quote")

    def test_vietstock_crypto_method(self):
        """Test Vietstock.crypto() method."""
        stock = Vietstock(show_log=False)
        btc = stock.crypto("BTC")
        assert btc is not None
        assert hasattr(btc, "quote")

    def test_vietstock_world_index_method(self):
        """Test Vietstock.world_index() method."""
        stock = Vietstock(show_log=False)
        dji = stock.world_index("DJI")
        assert dji is not None
        assert hasattr(dji, "quote")
