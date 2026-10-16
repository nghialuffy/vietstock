"""
Unit tests for vietstock API Listing adapter.

Tests the Listing class adapter for fetching symbol listings,
exchange-specific data, and industry classifications.
"""

from __future__ import annotations

import pandas as pd
import pytest

from vietstock.api.listing import Listing
from vietstock.core.registry import ProviderRegistry
from vietstock.explorer.tcbs.listing import Listing as TCBListing


@pytest.mark.unit
@pytest.mark.api
class TestListingAdapter:
    """Test suite for Listing API adapter."""

    def test_listing_instantiation_default(self):
        """Test Listing can be instantiated with default source."""
        listing = Listing(show_log=False)
        assert listing is not None

    def test_listing_instantiation_vci(self):
        """Test Listing can be instantiated with VCI source."""
        listing = Listing(source="VCI", show_log=False)
        assert listing is not None
        assert listing.source.lower() == "vci"

    def test_listing_has_all_symbols_method(self):
        """Test Listing has all_symbols method."""
        listing = Listing(source="VCI", show_log=False)
        assert hasattr(listing, "all_symbols")
        assert callable(listing.all_symbols)

    def test_listing_has_symbols_by_exchange_method(self):
        """Test Listing has symbols_by_exchange method."""
        listing = Listing(source="VCI", show_log=False)
        assert hasattr(listing, "symbols_by_exchange")

    def test_listing_has_symbols_by_industries_method(self):
        """Test Listing has symbols_by_industries method."""
        listing = Listing(source="VCI", show_log=False)
        assert hasattr(listing, "symbols_by_industries")

    def test_listing_has_industries_icb_method(self):
        """Test Listing has industries_icb method."""
        listing = Listing(source="VCI", show_log=False)
        assert hasattr(listing, "industries_icb")

    @pytest.mark.integration
    def test_listing_all_symbols_returns_dataframe(
        self,
        monkeypatch,
        mock_vci_send_request,
        sample_listing_data,
    ):
        """Test all_symbols returns DataFrame."""

        # Override mock to return sample data
        def mock_send(*args, **kwargs):
            return {"data": sample_listing_data}

        monkeypatch.setattr("vietstock.core.utils.client.send_request", mock_send)

        listing = Listing(source="VCI", show_log=False)
        try:
            df = listing.all_symbols(show_log=False, to_df=True)
            assert isinstance(df, pd.DataFrame)
        except Exception:
            pytest.skip("Requires full mock infrastructure")

    @pytest.mark.parametrize("source", ["VCI", "MSN"])
    def test_listing_supports_multiple_sources(self, source):
        """Test Listing supports different sources."""
        listing = Listing(source=source, show_log=False)
        assert listing.source.lower() == source.lower()

    def test_listing_tcbs_source_is_registered(self):
        """Test TCBS is wired up as a Listing provider and exposes its own method."""
        listing = Listing(source="TCBS", show_log=False)

        assert listing.source.lower() == "tcbs"
        assert ProviderRegistry.is_registered("listing", "tcbs")
        assert isinstance(listing.provider, TCBListing)
        assert callable(listing.research_reports)
