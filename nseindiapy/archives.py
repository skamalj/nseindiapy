"""Archives module — download NSE reports via the /api/reports endpoint.

All methods return raw bytes by default. Pass as_df=True to get a polars DataFrame
(CSV/zip is parsed transparently).
"""

from __future__ import annotations

import io
import json
import zipfile
from datetime import date, datetime
from typing import Any


# ─── Report catalog ──────────────────────────────────────────────────────────

_REPORTS = {
    # Capital Market — Equities
    "equities_bhavcopy": {"name": "CM - Bhavcopy (PR.zip)", "type": "archives", "category": "capital-market", "section": "equities"},
    "equities_full_bhavcopy": {"name": "Full Bhavcopy and Security Deliverable data", "type": "daily-reports", "category": "capital-market", "section": "equities"},
    "equities_volatility": {"name": "CM - Daily Volatility", "type": "archives", "category": "capital-market", "section": "equities"},
    "equities_var_margin": {"name": "CM - VaR Margin Rates (End of day)", "type": "archives", "category": "capital-market", "section": "equities"},
    "equities_turnover": {"name": "CM - Category-wise Turnover", "type": "archives", "category": "capital-market", "section": "equities"},
    "equities_market_pulse": {"name": "NSE Market Pulse (.pdf)", "type": "archives", "category": "capital-market", "section": "equities"},
    # Capital Market — Indices
    "indices_snapshot": {"name": "Daily Snapshot", "type": "archives", "category": "capital-market", "section": "indices"},
    "indices_mcap_weight_beta": {"name": "Market Capitalisation, Weightage,Beta for NIFTY 50 & NIFTY Next 50", "type": "archives", "category": "capital-market", "section": "indices"},
    "indices_impact_cost": {"name": "Impact Cost", "type": "archives", "category": "capital-market", "section": "indices"},
    "indices_mcap_weight": {"name": "Indices - Market Capitalisation & Weightage", "type": "archives", "category": "capital-market", "section": "indices"},
    "indices_fixed_income": {"name": "Index Dashboard - Fixed Income", "type": "archives", "category": "capital-market", "section": "indices"},
    "indices_nifty50_top10": {"name": "NIFTY 50 Top 10 Holdings (csv)", "type": "archives", "category": "capital-market", "section": "indices"},
    # Derivatives — F&O (Equity)
    "fo_bhavcopy": {"name": "F&O - Bhavcopy (fo.zip)", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_market_activity": {"name": "F&O - Market Activity Report", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_volatility": {"name": "F&O - Daily Volatility", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_settlement_prices": {"name": "F&O - Daily Settlement Prices", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_combined": {"name": "F&O - Combined Report", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_open_interest": {"name": "F&O - NCL Open Interest", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_ban_period": {"name": "F&O - Security in ban period", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_position_limits": {"name": "F&O - Clientwise Position Limits", "type": "archives", "category": "derivatives", "section": "equity"},
    "fo_span_risk": {"name": "F&O - Span Risk Parameter File (2nd intra-day)", "type": "archives", "category": "derivatives", "section": "equity"},
    # Derivatives — Commodity
    "commodity_bhavcopy": {"name": "COM - Bhavcopy (zip)", "type": "archives", "category": "derivatives", "section": "commodity"},
    "commodity_stock_position": {"name": "COM - Daily Stock Position Report", "type": "archives", "category": "derivatives", "section": "commodity"},
    "commodity_volatility": {"name": "COM - Volatility", "type": "archives", "category": "derivatives", "section": "commodity"},
    "commodity_base_price": {"name": "COM - Base Price", "type": "archives", "category": "derivatives", "section": "commodity"},
    "commodity_market_activity": {"name": "COM - Market Activity Report", "type": "archives", "category": "derivatives", "section": "commodity"},
    # Derivatives — Currency
    "currency_settlement": {"name": "CD - Settlement Prices", "type": "archives", "category": "derivatives", "section": "currency"},
    "currency_volatility": {"name": "CD - Volatility", "type": "archives", "category": "derivatives", "section": "currency"},
    "currency_base_price": {"name": "CD - Base Price", "type": "archives", "category": "derivatives", "section": "currency"},
    "currency_market_activity": {"name": "CD - Market Activity Report", "type": "archives", "category": "derivatives", "section": "currency"},
    "currency_mode_of_trading": {"name": "CD - Mode of Trading", "type": "archives", "category": "derivatives", "section": "currency"},
    "currency_bhavcopy": {"name": "CD-Bhavcopy File (DAT)", "type": "archives", "category": "derivatives", "section": "currency"},
    "currency_contract_files": {"name": "CD-MII - Contract Files (.gz)", "type": "archives", "category": "derivatives", "section": "currency"},
}


def _bytes_to_df(data: bytes, is_zip: bool = False) -> Any:
    """Convert CSV bytes (or zipped CSV) to a polars DataFrame."""
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "polars is required for as_df=True. Install with: pip install nseindiapy[polars]"
        )

    if is_zip:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            csv_names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if csv_names:
                csv_bytes = zf.read(csv_names[0])
                return pl.read_csv(io.BytesIO(csv_bytes))
            # If no CSV in zip, try first file
            csv_bytes = zf.read(zf.namelist()[0])
            return pl.read_csv(io.BytesIO(csv_bytes))
    else:
        return pl.read_csv(io.BytesIO(data))


class Archives:
    """Download NSE reports and archives.

    Uses the /api/reports endpoint which returns JSON with download URLs.
    Pass as_df=True to auto-download and parse as polars DataFrame.

    Available report keys (use with client.archives.download()):
        Equities: equities_bhavcopy, equities_full_bhavcopy, equities_volatility,
                  equities_var_margin, equities_turnover, equities_market_pulse
        Indices:  indices_snapshot, indices_mcap_weight_beta, indices_impact_cost,
                  indices_mcap_weight, indices_fixed_income, indices_nifty50_top10
        F&O:      fo_bhavcopy, fo_market_activity, fo_volatility, fo_settlement_prices,
                  fo_combined, fo_open_interest, fo_ban_period, fo_position_limits, fo_span_risk
        Commodity: commodity_bhavcopy, commodity_stock_position, commodity_volatility,
                   commodity_base_price, commodity_market_activity
        Currency: currency_settlement, currency_volatility, currency_base_price,
                  currency_market_activity, currency_mode_of_trading, currency_bhavcopy,
                  currency_contract_files
    """

    def __init__(self, session: Any) -> None:
        self._s = session

    @staticmethod
    def available_reports() -> list[str]:
        """List all available report keys."""
        return sorted(_REPORTS.keys())

    def download(self, report_key: str, date: str, as_df: bool = False) -> bytes | Any:
        """Download a report by key and date.

        Args:
            report_key: Report identifier (e.g. 'equities_bhavcopy', 'fo_bhavcopy').
                       Use Archives.available_reports() to see all options.
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, parse CSV/zip and return polars DataFrame.

        Returns:
            Raw bytes or polars DataFrame.
        """
        if report_key not in _REPORTS:
            raise ValueError(
                f"Unknown report_key '{report_key}'. "
                f"Use Archives.available_reports() to see valid keys."
            )

        report_desc = _REPORTS[report_key]
        archives_param = json.dumps([report_desc])

        # Get the report — NSE may return JSON (with link) or file bytes directly
        resp = self._s.get_response(
            "/api/reports",
            params={
                "archives": archives_param,
                "date": date,
                "type": report_desc["section"],
                "mode": "single",
            },
        )

        content_type = resp.headers.get("content-type", "")

        # If response is JSON, it contains a download link
        if "application/json" in content_type:
            resp_data = resp.json()
            download_url = self._extract_url(resp_data)
            if download_url is None:
                # JSON data itself is the result
                if as_df:
                    from nseindiapy._df import to_dataframe
                    return to_dataframe(resp_data)
                return resp_data
            # Download the actual file from the link
            file_bytes = self._s.get_bytes(download_url)
        else:
            # Response IS the file (binary)
            file_bytes = resp.content

        if as_df:
            is_zip = (
                "zip" in content_type
                or report_key.endswith("_bhavcopy")
                or "(zip)" in report_desc["name"].lower()
                or "(fo.zip)" in report_desc["name"].lower()
            )
            return _bytes_to_df(file_bytes, is_zip=is_zip)
        return file_bytes

    # ─── Convenience methods ─────────────────────────────────────────────────

    def equity_bhavcopy(self, date: str, as_df: bool = False) -> bytes | Any:
        """Download equity bhavcopy (PR.zip).

        Args:
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, return polars DataFrame.
        """
        return self.download("equities_bhavcopy", date, as_df=as_df)

    def equity_full_bhavcopy(self, date: str, as_df: bool = False) -> bytes | Any:
        """Download full bhavcopy with delivery data.

        Args:
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, return polars DataFrame.
        """
        return self.download("equities_full_bhavcopy", date, as_df=as_df)

    def fo_bhavcopy(self, date: str, as_df: bool = False) -> bytes | Any:
        """Download F&O bhavcopy (fo.zip).

        Args:
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, return polars DataFrame.
        """
        return self.download("fo_bhavcopy", date, as_df=as_df)

    def commodity_bhavcopy(self, date: str, as_df: bool = False) -> bytes | Any:
        """Download commodity bhavcopy.

        Args:
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, return polars DataFrame.
        """
        return self.download("commodity_bhavcopy", date, as_df=as_df)

    def indices_snapshot(self, date: str, as_df: bool = False) -> bytes | Any:
        """Download daily indices snapshot.

        Args:
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, return polars DataFrame.
        """
        return self.download("indices_snapshot", date, as_df=as_df)

    def fo_open_interest(self, date: str, as_df: bool = False) -> bytes | Any:
        """Download F&O NCL open interest.

        Args:
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, return polars DataFrame.
        """
        return self.download("fo_open_interest", date, as_df=as_df)

    def equity_volatility(self, date: str, as_df: bool = False) -> bytes | Any:
        """Download daily equity volatility.

        Args:
            date: Date in DD-Mon-YYYY format (e.g. '06-May-2026').
            as_df: If True, return polars DataFrame.
        """
        return self.download("equities_volatility", date, as_df=as_df)

    @staticmethod
    def _extract_url(data: Any) -> str | None:
        """Extract download URL from the /api/reports response."""
        if isinstance(data, list) and data:
            for item in data:
                if isinstance(item, dict):
                    for key in ("link", "downloadLink", "url", "fileLink"):
                        if key in item and item[key]:
                            url = item[key]
                            if not url.startswith("http"):
                                url = f"https://www.nseindia.com{url}"
                            return url
        elif isinstance(data, dict):
            for key in ("link", "downloadLink", "url", "fileLink"):
                if key in data and data[key]:
                    url = data[key]
                    if not url.startswith("http"):
                        url = f"https://www.nseindia.com{url}"
                    return url
            # Check nested
            if "data" in data and isinstance(data["data"], list):
                return Archives._extract_url(data["data"])
        return None
