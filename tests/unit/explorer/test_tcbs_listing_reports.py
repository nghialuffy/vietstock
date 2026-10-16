"""
Unit tests for the TCBS research report feed.

TCBS serves the report list as HTML: the page hands out a nonce, and the ajax
endpoint hands back the next slice of rows. These tests pin that contract down
against the real markup, because a layout change is the failure mode most likely
to slip through — the parser would simply return nothing instead of raising.
"""

from __future__ import annotations

import json
from urllib.parse import parse_qsl

import pandas as pd
import pytest

from vietstock.core.exceptions import DataParsingError
from vietstock.explorer.tcbs.listing import Listing

PAGE_URL = "https://www.tcbs.com.vn/en/information/research-reports/"
AJAX_URL = "https://www.tcbs.com.vn/wp-content/custom-ajax.php"
NONCE = "df4298a918"


# The button is the whole handshake: endpoint, nonce, language, page count and the
# filter object the ajax call must echo back. Quotes are escaped the way the live
# page escapes them.
def _page_html(max_pages: int = 24) -> str:
    return (
        "<html><body>"
        '<button type="button" class="tcbs-report-load-more" data-page="1"'
        f' data-max-pages="{max_pages}"'
        ' data-lang="en"'
        ' data-filters="{&quot;report_type&quot;:[],&quot;year&quot;:[],&quot;quarter&quot;:[],'
        '&quot;ticker&quot;:&quot;&quot;,&quot;hashtag&quot;:&quot;&quot;}"'
        f' data-url="{AJAX_URL}" data-nonce="{NONCE}" data-loading="Loading...">Load more</button>'
        "</body></html>"
    )


# Trimmed from a live response: the column-label row (only on page one) followed by
# one ticker-tagged report and one market-wide report.
FRAGMENT = """
<div class="tcbs-report-list">
    <div class="tcbs-report-row tcbs-report-header">
        <div class="tcbs-report-date">Report date</div>
        <div class="tcbs-report-type">Report type</div>
        <div class="tcbs-report-title">Report name</div>
        <div aria-hidden="true" class="tcbs-report-actions"></div>
    </div>
    <div class="tcbs-report-row">
        <div class="tcbs-report-date">02/10/2026</div>
        <div class="tcbs-report-type">Initial report</div>
        <div class="tcbs-report-title">
            Initiation Report &mdash; VNM &middot; Vietnam Dairy Products JSC
            <div class="tcbs-report-tags">
                <span class="tcbs-report-tag tcbs-report-tag--ticker">VNM</span>
                <span class="tcbs-report-tag tcbs-report-tag--hashtag">#Initiation Report</span>
                <span class="tcbs-report-tag tcbs-report-tag--hashtag">#Food sector</span>
            </div>
        </div>
        <div class="tcbs-report-actions">
            <a href="https://www.tcbs.com.vn/wp-content/uploads/2026/10/20261002_Initiation_Report_VNM.pdf"
               target="_blank" rel="noopener"><span>View report</span></a>
            <a href="https://www.tcbs.com.vn/wp-content/uploads/2026/10/20261002_Initiation_Report_VNM.pdf"
               download><span>Download</span></a>
        </div>
    </div>
    <div class="tcbs-report-row">
        <div class="tcbs-report-date">02/10/2026</div>
        <div class="tcbs-report-type">Business result update</div>
        <div class="tcbs-report-title">
            Q3/2026 earnings preview: 35 large companies
            <div class="tcbs-report-tags">
                <span class="tcbs-report-tag tcbs-report-tag--hashtag">#Q3 2026 Earnings Preview</span>
                <span class="tcbs-report-tag tcbs-report-tag--hashtag">#Market-wide</span>
            </div>
        </div>
        <div class="tcbs-report-actions">
            <a href="https://www.tcbs.com.vn/wp-content/uploads/2026/10/20261002_Q3_2026_Earnings_Preview.pdf"
               target="_blank" rel="noopener"><span>View report</span></a>
        </div>
    </div>
</div>
"""


@pytest.fixture
def tcbs_api(monkeypatch):
    """
    Replay canned page and ajax responses, recording what was sent.

    Patches both names on the explorer module because it binds them at import time.
    """
    state: dict = {
        "page_html": _page_html(),
        "fragments": {1: FRAGMENT},
        "hide_button": {},
        "page_calls": [],
        "ajax_calls": [],
    }

    def _fake_send_request_text(url, headers, method="GET", params=None, payload=None, show_log=False, timeout=30):
        state["page_calls"].append({"url": url, "headers": headers})
        return state["page_html"]

    def _fake_send_request(url, headers, method="GET", params=None, payload=None, show_log=False, timeout=30):
        body = dict(parse_qsl(payload or ""))
        state["ajax_calls"].append({"url": url, "payload": body})
        page = int(body["page"])
        return {
            "success": True,
            "data": {
                "html": state["fragments"].get(page, ""),
                "hide_button": state["hide_button"].get(page, False),
            },
        }

    monkeypatch.setattr("vietstock.explorer.tcbs.listing.send_request_text", _fake_send_request_text)
    monkeypatch.setattr("vietstock.explorer.tcbs.listing.send_request", _fake_send_request)
    return state


@pytest.mark.unit
@pytest.mark.explorer
@pytest.mark.tcbs
class TestTCBSResearchReports:
    """Test suite for Listing.research_reports."""

    def test_payload_reuses_the_page_contract(self, tcbs_api):
        """The ajax call must echo the nonce, endpoint, language and filters."""
        Listing().research_reports()

        assert len(tcbs_api["page_calls"]) == 1
        assert tcbs_api["page_calls"][0]["url"] == PAGE_URL

        assert len(tcbs_api["ajax_calls"]) == 1
        call = tcbs_api["ajax_calls"][0]
        assert call["url"] == AJAX_URL
        assert call["payload"]["action"] == "tcbs_reports_load_more"
        assert call["payload"]["page"] == "1"
        assert call["payload"]["lang"] == "en"
        assert call["payload"]["nonce"] == NONCE
        assert json.loads(call["payload"]["filters"]) == {
            "report_type": [],
            "year": [],
            "quarter": [],
            "ticker": "",
            "hashtag": "",
        }

    def test_requested_page_is_the_one_sent(self, tcbs_api):
        """A page number must reach the payload unchanged."""
        Listing().research_reports(page=7)

        assert tcbs_api["ajax_calls"][0]["payload"]["page"] == "7"

    def test_filters_override_only_the_given_keys(self, tcbs_api):
        """Caller filters merge over the page defaults instead of replacing them."""
        Listing().research_reports(filters={"ticker": "VNM"})

        sent = json.loads(tcbs_api["ajax_calls"][0]["payload"]["filters"])
        assert sent["ticker"] == "VNM"
        assert sent["report_type"] == []
        assert sent["hashtag"] == ""

    def test_parses_rows_and_skips_the_header_row(self, tcbs_api):
        """Every report becomes a row; the column-label row must not."""
        df = Listing().research_reports()

        assert len(df) == 2
        assert list(df.columns) == ["date", "report_type", "title", "ticker", "hashtags", "url"]
        assert df["date"].dtype == "datetime64[ns]"
        assert df.source == "TCBS"

        first = df.iloc[0]
        assert first["date"] == pd.Timestamp("2026-10-02")
        assert first["report_type"] == "Initial report"
        assert first["title"] == "Initiation Report — VNM · Vietnam Dairy Products JSC"
        assert first["ticker"] == "VNM"
        assert first["hashtags"] == ["#Initiation Report", "#Food sector"]
        assert first["url"].endswith("20261002_Initiation_Report_VNM.pdf")

        # A report that covers the whole market carries no ticker tag.
        second = df.iloc[1]
        assert second["ticker"] is None
        assert second["hashtags"] == ["#Q3 2026 Earnings Preview", "#Market-wide"]
        assert second["url"].endswith("20261002_Q3_2026_Earnings_Preview.pdf")

    def test_all_pages_fetches_until_hide_button(self, tcbs_api):
        """all_pages walks the range and stops once TCBS drops the button."""
        tcbs_api["page_html"] = _page_html(max_pages=3)
        tcbs_api["fragments"] = {1: FRAGMENT, 2: FRAGMENT, 3: FRAGMENT}
        tcbs_api["hide_button"] = {3: True}

        df = Listing().research_reports(all_pages=True)

        assert [call["payload"]["page"] for call in tcbs_api["ajax_calls"]] == ["1", "2", "3"]
        assert len(df) == 6
        assert len(tcbs_api["page_calls"]) == 1  # one nonce for the whole walk

    def test_all_pages_stops_on_an_empty_fragment(self, tcbs_api):
        """A filtered feed can run dry before max-pages is reached."""
        tcbs_api["page_html"] = _page_html(max_pages=5)
        tcbs_api["fragments"] = {1: FRAGMENT}

        Listing().research_reports(all_pages=True)

        assert [call["payload"]["page"] for call in tcbs_api["ajax_calls"]] == ["1", "2"]

    def test_empty_fragment_returns_empty_frame_with_columns(self, tcbs_api):
        """No reports is still a usable frame, not a bare DataFrame."""
        tcbs_api["fragments"] = {}

        df = Listing().research_reports()

        assert df.empty
        assert list(df.columns) == ["date", "report_type", "title", "ticker", "hashtags", "url"]
        assert df.source == "TCBS"

    def test_missing_nonce_button_raises_parsing_error(self, tcbs_api):
        """A page without the button means the layout changed, not zero reports."""
        tcbs_api["page_html"] = "<html><body>not the report page</body></html>"

        with pytest.raises(DataParsingError):
            Listing().research_reports()

        assert tcbs_api["ajax_calls"] == []

    def test_page_below_one_is_rejected_before_any_request(self, tcbs_api):
        """page is 1-based; page 0 is silently page 1 on the server, so refuse it."""
        with pytest.raises(ValueError):
            Listing().research_reports(page=0)

        assert tcbs_api["page_calls"] == []
        assert tcbs_api["ajax_calls"] == []
