"""Listing module for TCBS (Techcom Securities) research reports."""

from __future__ import annotations

import json
import urllib.parse

import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag

from vietstock.core.exceptions import DataParsingError
from vietstock.core.utils.client import send_request, send_request_text
from vietstock.core.utils.logger import get_logger
from vietstock.core.utils.user_agent import get_headers

from .const import (
    _RESEARCH_REPORTS_ACTION,
    _RESEARCH_REPORTS_AJAX_URL,
    _RESEARCH_REPORTS_HEADERS,
    _RESEARCH_REPORTS_URL,
)

logger = get_logger(__name__)

_COLUMNS = ["date", "report_type", "title", "ticker", "hashtags", "url"]


class Listing:
    """
    Access the securities listing data published by TCBS.

    The free edition covers the research report feed only. Quote, company and
    financial data for TCBS live in the sponsor package `vnstock_data`.
    """

    def __init__(
        self,
        random_agent: bool | None = False,
        show_log: bool | None = False,
    ):
        """
        Initialise the TCBS Listing client.

        Args:
            random_agent: Deprecated and ignored. Defaults to False.
            show_log: Show debug logs. Defaults to False.
        """
        self.data_source = "TCBS"
        self.base_url = _RESEARCH_REPORTS_URL
        self.headers = get_headers(
            data_source=self.data_source,
            random_agent=random_agent,
            override_headers=_RESEARCH_REPORTS_HEADERS,
        )
        self.show_log = show_log

        if not show_log:
            logger.setLevel("CRITICAL")

    def research_reports(
        self,
        page: int = 1,
        all_pages: bool = False,
        filters: dict | None = None,
        show_log: bool | None = False,
    ) -> pd.DataFrame:
        """
        Retrieve TCBS research reports, one row per report.

        Each row carries the report date and the PDF link, so the caller can
        answer "what has TCBS published lately?" without scraping the page.

        Args:
            page: First page to fetch, 1-based. Defaults to 1.
            all_pages: Keep fetching from `page` until TCBS serves the last one.
                Defaults to False, which fetches `page` only.
            filters: Overrides for the page's own filter object, e.g.
                ``{"ticker": "VNM"}``. Keys not given keep the page defaults.
            show_log: Show debug logs. Defaults to False.

        Returns:
            DataFrame with columns ``date``, ``report_type``, ``title``,
            ``ticker``, ``hashtags`` and ``url``.

        Raises:
            ValueError: If `page` is below 1.
            DataParsingError: If the page no longer exposes its nonce button or
                its filter and page-count attributes.

        Examples:
            >>> df = Listing().research_reports(page=3)
            >>> df[["date", "title", "url"]].head()
        """
        if page < 1:
            raise ValueError("Tham số page phải >= 1 (page must be >= 1).")

        context = self._page_context()
        pages = range(page, context["max_pages"] + 1) if all_pages else [page]

        records: list[dict] = []
        for current_page in pages:
            payload = urllib.parse.urlencode(
                {
                    "action": _RESEARCH_REPORTS_ACTION,
                    "page": current_page,
                    "lang": context["lang"],
                    "filters": json.dumps({**context["filters"], **(filters or {})}),
                    "nonce": context["nonce"],
                },
            )
            json_data = send_request(
                url=context["url"],
                headers=self.headers,
                method="POST",
                payload=payload,
                show_log=show_log,
            )
            data = (json_data or {}).get("data") or {}
            records.extend(_parse_reports(data.get("html") or ""))

            # TCBS never names a total row count per call; it drops the button on
            # the last page. An empty fragment means the same thing, so stop there
            # rather than keep asking for pages that cannot exist.
            if data.get("hide_button") or not data.get("html"):
                break

        df = pd.DataFrame(records, columns=_COLUMNS)

        if not df.empty:
            df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")

        df.source = "TCBS"

        if show_log:
            logger.info(
                f"Truy xuất thành công {len(df)} báo cáo phân tích từ TCBS "
                f"(Successfully retrieved {len(df)} TCBS research reports).",
            )

        return df

    def _page_context(self) -> dict:
        """
        Read the token, endpoint, language and default filters off the page button.

        A fresh nonce is taken on every call on purpose: an expired one is answered
        with HTTP 403, which the shared client reads as a block signal and turns
        into a cooldown for the whole host.
        """
        html = send_request_text(
            url=_RESEARCH_REPORTS_URL,
            headers=self.headers,
            method="GET",
            show_log=self.show_log,
        )

        button = BeautifulSoup(html, "html.parser").select_one("[data-nonce]")
        if button is None:
            raise DataParsingError(
                "Không tìm thấy nút tải báo cáo (data-nonce) trên trang TCBS, "
                "trang có thể đã đổi cấu trúc. (The TCBS report page exposes no "
                "data-nonce button; the page layout likely changed.)",
                provider="TCBS",
            )

        try:
            default_filters = json.loads(button.get("data-filters") or "{}")
            max_pages = int(button.get("data-max-pages") or 1)
            if not isinstance(default_filters, dict):
                raise TypeError("data-filters phải là một object JSON (must be a JSON object)")
        except (TypeError, ValueError) as err:
            raise DataParsingError(
                f"Không đọc được data-filters/data-max-pages từ trang TCBS: {err} "
                "(Could not read data-filters/data-max-pages from the TCBS page.)",
                provider="TCBS",
            ) from err

        return {
            "nonce": button.get("data-nonce"),
            "url": button.get("data-url") or _RESEARCH_REPORTS_AJAX_URL,
            "lang": button.get("data-lang") or "en",
            "max_pages": max_pages,
            "filters": default_filters,
        }


def _parse_reports(html: str) -> list[dict]:
    """
    Turn one AJAX html fragment into a dict per report row.

    The first page opens with the column labels in the same row markup, so rows
    carrying the ``tcbs-report-header`` class are dropped.
    """
    reports: list[dict] = []

    for row in BeautifulSoup(html, "html.parser").select(".tcbs-report-row"):
        if "tcbs-report-header" in (row.get("class") or []):
            continue

        title_element = row.select_one(".tcbs-report-title")
        ticker_element = title_element.select_one(".tcbs-report-tag--ticker") if title_element else None
        hashtags = (
            [tag.get_text(strip=True) for tag in title_element.select(".tcbs-report-tag--hashtag")]
            if title_element
            else []
        )

        # The tags are nested inside the title container; drop them before
        # reading the title so they do not leak into it.
        if title_element:
            tags_element = title_element.select_one(".tcbs-report-tags")
            if tags_element:
                tags_element.extract()

        link = row.select_one('.tcbs-report-actions a[href$=".pdf"]')

        reports.append(
            {
                "date": _text(row.select_one(".tcbs-report-date")),
                "report_type": _text(row.select_one(".tcbs-report-type")),
                "title": " ".join(title_element.get_text(" ", strip=True).split()) if title_element else None,
                "ticker": _text(ticker_element),
                "hashtags": hashtags,
                "url": link.get("href") if link else None,
            },
        )

    return reports


def _text(element: Tag | None) -> str | None:
    """Return an element's trimmed text, or None when the element is absent."""
    return element.get_text(strip=True) if element is not None else None


# Register TCBS Listing provider
from vietstock.core.registry import ProviderRegistry  # noqa: E402, F401

ProviderRegistry.register("listing", "tcbs", Listing)
