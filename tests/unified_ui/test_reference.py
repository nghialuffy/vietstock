from __future__ import annotations

import pandas as pd

from vietstock.ui.domains.reference.company import CompanyReference
from vietstock.ui.domains.reference.equity import EquityReference
from vietstock.ui.domains.reference.reports import ReportsReference
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


def test_reference_reports_property():
    """Test Reference.reports returns ReportsReference."""
    ref = Reference()
    assert isinstance(ref.reports, ReportsReference)


def test_reference_reports_routes_to_the_tcbs_provider(monkeypatch):
    """The registry entry must point at the source that implements the call."""
    calls: dict = {}

    def _fake_research_reports(self, *args, **kwargs):
        calls["source"] = self.source
        calls["kwargs"] = kwargs
        return pd.DataFrame({"url": ["report.pdf"]})

    monkeypatch.setattr("vietstock.api.listing.Listing.research_reports", _fake_research_reports)

    df = Reference().reports.list(page=3, filters={"ticker": "VNM"})

    assert isinstance(df, pd.DataFrame)
    assert calls["source"].lower() == "tcbs"
    assert calls["kwargs"]["page"] == 3
    assert calls["kwargs"]["all_pages"] is False
    assert calls["kwargs"]["filters"] == {"ticker": "VNM"}
