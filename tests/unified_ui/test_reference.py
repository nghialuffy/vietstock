from __future__ import annotations

from vietstock.ui.domains.reference.company import CompanyReference
from vietstock.ui.domains.reference.equity import EquityReference
from vietstock.ui.reference import Reference


def test_reference_instantiation():
    """Test Reference class can be instantiated."""
    ref = Reference()
    assert ref is not None


def test_reference_equity_property():
    """Test Reference.equity returns EquityReference."""
    ref = Reference()
    equity = ref.equity
    assert isinstance(equity, EquityReference)


def test_reference_company_method():
    """Test Reference.company() returns CompanyReference."""
    ref = Reference()
    company = ref.company(symbol="FPT")
    assert isinstance(company, CompanyReference)
