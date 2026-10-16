from __future__ import annotations

from vietstock.ui.domains.fundamental.equity import EquityFundamental
from vietstock.ui.fundamental import Fundamental


def test_fundamental_instantiation():
    """Test Fundamental class can be instantiated."""
    fund = Fundamental()
    assert fund is not None


def test_fundamental_equity_method():
    """Test Fundamental.equity() returns EquityFundamental."""
    fund = Fundamental()
    equity = fund.equity(symbol="FPT")
    assert isinstance(equity, EquityFundamental)
