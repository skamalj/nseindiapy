"""Reports module — daily and monthly reports for all market segments.

Reports return JSON metadata containing download URLs. By default, the raw JSON
is returned. Pass as_df=True to automatically download the first available CSV
and return it as a polars DataFrame.
"""

from __future__ import annotations

import io
from typing import Any


def _extract_download_url(data: Any) -> str | None:
    """Try to find a download URL in the report JSON response."""
    if isinstance(data, dict):
        # Common patterns in NSE report responses
        for key in ("link", "downloadLink", "url", "fileLink", "csvLink"):
            if key in data and data[key]:
                return data[key]
        # Check nested structures
        if "data" in data and isinstance(data["data"], list):
            for item in data["data"]:
                if isinstance(item, dict):
                    for key in ("link", "downloadLink", "url", "fileLink"):
                        if key in item and item[key]:
                            return item[key]
    elif isinstance(data, list) and data:
        for item in data:
            if isinstance(item, dict):
                for key in ("link", "downloadLink", "url", "fileLink"):
                    if key in item and item[key]:
                        return item[key]
    return None


class Reports:
    """Access NSE daily and monthly reports.

    Reports return JSON with metadata and download links. Use as_df=True
    to auto-download the CSV and get a polars DataFrame directly.
    """

    def __init__(self, session: Any) -> None:
        self._s = session

    def daily(self, key: str = "CM", as_df: bool = False) -> Any:
        """Daily report for a market segment.

        Args:
            key: Segment key — 'CM', 'INDEX', 'SLBS', 'SME', 'FO', 'COM',
                 'CD', 'NBF', 'WDM', 'CBM', 'TRI-PARTY', 'EGR'.
            as_df: If True, download the first CSV link and return polars DataFrame.

        Returns:
            JSON metadata (dict/list) or polars DataFrame.
        """
        data = self._s.get("/api/daily-reports", params={"key": key})
        if as_df:
            return self._download_as_df(data)
        return data

    def monthly(self, key: str = "CM", as_df: bool = False) -> Any:
        """Monthly report for a market segment.

        Args:
            key: Segment key — 'CM', 'INDICES', 'SLBS', 'FO', 'CD',
                 'COM', 'IRD', 'WDM', 'CBM'.
            as_df: If True, download the first CSV link and return polars DataFrame.

        Returns:
            JSON metadata (dict/list) or polars DataFrame.
        """
        data = self._s.get("/api/monthly-reports", params={"key": key})
        if as_df:
            return self._download_as_df(data)
        return data

    def merged_daily(self, key: str = "favCapital", as_df: bool = False) -> Any:
        """Merged daily report.

        Args:
            key: 'favCapital', 'favDerivatives', 'favDebt'.
            as_df: If True, download the first CSV link and return polars DataFrame.

        Returns:
            JSON metadata (dict/list) or polars DataFrame.
        """
        data = self._s.get("/api/merged-daily-reports", params={"key": key})
        if as_df:
            return self._download_as_df(data)
        return data

    def download_file(self, url: str) -> bytes:
        """Download a report file by URL (CSV, Excel, etc.).

        Args:
            url: Full URL to the report file.

        Returns:
            Raw bytes of the file.
        """
        return self._s.get_bytes(url)

    def _download_as_df(self, data: Any) -> Any:
        """Find a download URL in the response and return as DataFrame."""
        try:
            import polars as pl
        except ImportError:
            raise ImportError(
                "polars is required for as_df=True. Install with: pip install nseindiapy[polars]"
            )

        url = _extract_download_url(data)
        if url is None:
            # No download link found — try to convert the JSON data itself
            from nseindiapy._df import to_dataframe
            return to_dataframe(data)

        # Download the file
        file_bytes = self._s.get_bytes(url)

        # Determine format from URL
        if url.endswith(".csv") or url.endswith(".csv.zip"):
            if url.endswith(".zip"):
                import zipfile
                with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
                    csv_name = [n for n in zf.namelist() if n.endswith(".csv")][0]
                    file_bytes = zf.read(csv_name)
            return pl.read_csv(io.BytesIO(file_bytes))
        elif url.endswith(".xlsx") or url.endswith(".xls"):
            return pl.read_excel(io.BytesIO(file_bytes))
        else:
            # Try CSV first, fall back to returning raw data
            try:
                return pl.read_csv(io.BytesIO(file_bytes))
            except Exception:
                from nseindiapy._df import to_dataframe
                return to_dataframe(data)
