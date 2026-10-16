"""
Unit tests for VCI Listing.events_calendar (market-wide corporate events).

The market-wide calendar is the only path that answers "which symbols go
ex-dividend in the next two months?", so these tests pin down the two things
that made the ticker-bound Company.events() unusable for that question:
no ``ticker`` parameter is ever sent, and the date range is caller-controlled.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import pytest

from vietstock.explorer.vci.listing import Listing


def _event(ticker: str, **overrides) -> dict:
    """Build one VCI events record, in the API's camelCase shape."""
    row = {
        "ticker": ticker,
        "eventCode": "DIV",
        "exrightDate": "2026-10-22T00:00:00",
        "recordDate": "2026-10-23T00:00:00",
        "valuePerShare": 400.0,
    }
    row.update(overrides)
    return row


@pytest.fixture
def events_api(monkeypatch):
    """
    Capture the request parameters and replay a canned VCI response.

    Patches ``vietstock.explorer.vci.listing.send_request`` because the module
    binds the name at import time.
    """
    state: dict = {"calls": [], "response": {"data": {"content": []}}}

    def _fake_send_request(
        url,
        headers,
        method="GET",
        params=None,
        payload=None,
        show_log=False,
        timeout=30,
    ):
        state["calls"].append({"url": url, "params": dict(params or {})})
        return state["response"]

    monkeypatch.setattr(
        "vietstock.explorer.vci.listing.send_request",
        _fake_send_request,
    )
    return state


@pytest.mark.unit
@pytest.mark.explorer
@pytest.mark.vci
class TestEventsCalendar:
    """Test suite for the market-wide events calendar."""

    def test_default_window_covers_today_to_thirty_days(self, events_api):
        """An omitted range defaults to the upcoming 30 days."""
        Listing(show_log=False).events_calendar()

        params = events_api["calls"][0]["params"]
        today = datetime.now()
        assert params["fromDate"] == today.strftime("%Y%m%d")
        assert params["toDate"] == (today + timedelta(days=30)).strftime("%Y%m%d")
        assert params["size"] == 500
        # No event type requested means every type is returned.
        assert "eventCode" not in params

    def test_date_range_and_event_type_are_forwarded(self, events_api):
        """An explicit range replaces the default one."""
        Listing(show_log=False).events_calendar("DIV", "2026-10-16", "2026-12-17")

        params = events_api["calls"][0]["params"]
        assert params["fromDate"] == "2026-10-16"
        assert params["toDate"] == "2026-12-17"
        assert params["eventCode"] == "DIV"

    def test_request_is_never_bound_to_a_single_ticker(self, events_api):
        """The whole point: no ``ticker`` param, so every symbol is covered."""
        Listing(show_log=False).events_calendar(event_type="DIV")

        call = events_api["calls"][0]
        assert "ticker" not in call["params"]
        assert "ticker=" not in call["url"]
        assert call["url"].endswith("/v1/events")

    def test_response_columns_and_dates_are_standardised(self, events_api):
        """camelCase becomes snake_case and dates become YYYY-MM-DD strings."""
        events_api["response"] = {
            "data": {
                "content": [
                    _event("MCP"),
                    _event("VIC", exrightDate=None, recordDate=None),
                ],
            },
        }

        df = Listing(show_log=False).events_calendar(event_type="DIV")

        assert isinstance(df, pd.DataFrame)
        assert "exright_date" in df.columns
        assert "exrightDate" not in df.columns

        assert df.loc[0, "ticker"] == "MCP"
        assert df.loc[0, "exright_date"] == "2026-10-22"
        assert df.loc[0, "record_date"] == "2026-10-23"
        assert df.loc[0, "value_per_share"] == 400.0

        # Absent dates stay missing instead of raising.
        assert pd.isna(df.loc[1, "exright_date"])

    def test_empty_or_null_result_returns_empty_dataframe(self, events_api):
        """An empty calendar, and the ``data: null`` answer, are both not errors."""
        empty = Listing(show_log=False).events_calendar(event_type="DIV")
        assert isinstance(empty, pd.DataFrame)
        assert empty.empty
        assert empty.source == "VCI"

        events_api["response"] = {"data": None}
        null = Listing(show_log=False).events_calendar(event_type="DIV")
        assert null.empty
