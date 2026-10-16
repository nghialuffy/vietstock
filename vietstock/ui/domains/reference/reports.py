from __future__ import annotations

from typing import Any

from vietstock.ui._base import BaseUI


class ReportsReference(BaseUI):
    """Research reports published by the data sources."""

    def list(
        self,
        page: int = 1,
        all_pages: bool = False,
        filters: dict | None = None,
    ) -> Any:
        """List research reports (report date + PDF link, paged)."""
        return self._dispatch(
            "Reference",
            "reports",
            "list",
            page=page,
            all_pages=all_pages,
            filters=filters,
        )
