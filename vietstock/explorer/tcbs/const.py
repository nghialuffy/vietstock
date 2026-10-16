"""Constants for the TCBS (Techcom Securities) research report feed."""

from __future__ import annotations

_TCBS_BASE_URL = "https://www.tcbs.com.vn"

# The report list is server-rendered; the page carries the nonce and the ajax
# endpoint as data attributes of its "load more" button.
_RESEARCH_REPORTS_URL = f"{_TCBS_BASE_URL}/en/information/research-reports/"
_RESEARCH_REPORTS_AJAX_URL = f"{_TCBS_BASE_URL}/wp-content/custom-ajax.php"
_RESEARCH_REPORTS_ACTION = "tcbs_reports_load_more"

# One header set serves both calls: the page GET and the form-encoded POST.
# Referer/Origin must override the "TCBS" mapping in get_headers(), which points
# at the legacy tcinvest.tcbs.com.vn host this feed does not live on.
_RESEARCH_REPORTS_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": _RESEARCH_REPORTS_URL,
    "Origin": _TCBS_BASE_URL,
}
