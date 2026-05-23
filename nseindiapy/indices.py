"""Indices module — all indices, constituents, chart data, GIFT Nifty."""

from __future__ import annotations

from typing import Any

from nseindiapy._df import to_dataframe


class Indices:
    """Access NSE index data."""

    def __init__(self, session: Any) -> None:
        self._s = session

    def all(self) -> Any:
        """All indices with current values (NIFTY 50, Bank NIFTY, VIX, etc.)."""
        return self._s.get("/api/allIndices")

    def names(self) -> Any:
        """List of all index names."""
        return self._s.get("/api/index-names")

    def constituents(self, index: str = "NIFTY 50", as_df: bool = False) -> Any:
        """Stocks in a specific index.

        Args:
            index: Index name (e.g. 'NIFTY 50', 'NIFTY BANK', 'NIFTY 100').
            as_df: If True, return polars DataFrame.
        """
        import urllib.parse
        encoded = urllib.parse.quote(index, safe="")
        self._s._ensure_cookies()
        self._s._throttle()
        resp = self._s._client.request(
            "GET", f"/api/equity-stock-indices?index={encoded}&selectValFormat=crores"
        )

        if resp.status_code in (401, 403):
            self._s._refresh_cookies()
            self._s._throttle()
            resp = self._s._client.request(
                "GET", f"/api/equity-stock-indices?index={encoded}&selectValFormat=crores"
            )

        resp.raise_for_status()
        data = resp.json()
        if as_df:
            return to_dataframe(data)
        return data

    def chart(self, index: str = "NIFTY 50") -> Any:
        """Intraday chart data for an index.

        Args:
            index: Index name.
        """
        return self._s.get("/api/chart-databyindex", params={"index": index})

    def gift_nifty(self) -> Any:
        """GIFT Nifty (SGX Nifty) data."""
        return self._s.get(
            "/api/NextApi/apiClient",
            params={"functionName": "getGiftNifty"},
        )
