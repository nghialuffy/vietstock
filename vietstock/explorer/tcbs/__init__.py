"""
TCBS (Techcom Securities) data explorer, free edition.

Kept deliberately small: it covers the public research report feed only. Quote,
company, financial and trading data for TCBS are not part of this package.
"""

from __future__ import annotations

from vietstock.explorer.tcbs.listing import Listing  # noqa: E402

__all__ = ["Listing"]
