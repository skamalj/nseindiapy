"""Market module — status, pre-open, gainers/losers, most active, deals, FII/DII."""

from __future__ import annotations

from typing import Any

from nseindiapy._df import to_dataframe


class Market:
    """Access market-wide data — status, movers, deals, FII/DII."""

    def __init__(self, session: Any) -> None:
        self._s = session

    def status(self) -> Any:
        """Current market status (open/closed) for all segments."""
        return self._s.get("/api/marketStatus")

    def all_status(self) -> Any:
        """All market segment statuses (CM, FO, CD, COM, etc.)."""
        return self._s.get("/api/allMarketStatus")

    def turnover(self) -> Any:
        """Market turnover data. Returns None if market is closed (empty response)."""
        self._s._ensure_cookies()
        self._s._throttle()
        resp = self._s._client.get("/api/market-turnover")
        if resp.status_code == 200 and resp.content:
            return resp.json()
        return None

    def pre_open(self, key: str = "NIFTY") -> Any:
        """Pre-open market data.

        Args:
            key: 'ALL', 'NIFTY', 'BANKNIFTY', 'SME', 'FO'.
        """
        return self._s.get("/api/market-data-pre-open", params={"key": key})

    def gainers(self, as_df: bool = False) -> Any:
        """Top gainers."""
        data = self._s.get("/api/live-analysis-variations", params={"index": "gainers"})
        if as_df:
            return to_dataframe(data)
        return data

    def losers(self, as_df: bool = False) -> Any:
        """Top losers."""
        data = self._s.get("/api/live-analysis-variations", params={"index": "losers"})
        if as_df:
            return to_dataframe(data)
        return data

    def most_active(self, by: str = "volume", as_df: bool = False) -> Any:
        """Most active securities.

        Args:
            by: 'volume' or 'value'.
            as_df: If True, return polars DataFrame.
        """
        data = self._s.get("/api/live-analysis-most-active-securities", params={"index": by})
        if as_df:
            return to_dataframe(data)
        return data

    def high_low_52week(self, which: str = "high", as_df: bool = False) -> Any:
        """52-week high or low stocks.

        Args:
            which: 'high' or 'low'.
            as_df: If True, return polars DataFrame.
        """
        data = self._s.get("/api/live-analysis-52Week", params={"index": which})
        if as_df:
            return to_dataframe(data)
        return data

    def block_deals(self) -> Any:
        """Block deals."""
        return self._s.get("/api/block-deal")

    def fii_dii(self) -> Any:
        """FII/FPI and DII trading activity."""
        return self._s.get("/api/fiidiiTradeReact")

    def holidays(self, type: str = "trading") -> Any:
        """Trading or clearing holidays.

        Args:
            type: 'trading' or 'clearing'.
        """
        return self._s.get("/api/holiday-master", params={"type": type})

    def etf(self, as_df: bool = False) -> Any:
        """All ETFs listed on NSE."""
        data = self._s.get("/api/etf")
        if as_df:
            return to_dataframe(data)
        return data

    def equity_master(self) -> Any:
        """Complete equity master data (all listed securities)."""
        return self._s.get("/api/equity-master")
