"""Equity module — quotes, metadata, historical data, corporate actions for individual stocks."""

from __future__ import annotations

from typing import Any

from nseindiapy._df import to_dataframe


class Equity:
    """Access equity/stock data for individual symbols."""

    def __init__(self, session: Any) -> None:
        self._s = session

    def quote(self, symbol: str) -> dict[str, Any]:
        """Full equity quote — price, OHLC, volume, 52W high/low.

        Args:
            symbol: NSE symbol (e.g. 'RELIANCE', 'TCS').
        """
        return self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={"functionName": "getSymbolData", "marketType": "N", "series": "EQ", "symbol": symbol},
        )

    def meta(self, symbol: str) -> dict[str, Any]:
        """Equity metadata — ISIN, industry, listing date, face value.

        Args:
            symbol: NSE symbol.
        """
        return self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={"functionName": "getMetaData", "symbol": symbol},
        )

    def trade_info(self, symbol: str) -> dict[str, Any]:
        """Trade information — delivery %, traded volume, market type.

        Args:
            symbol: NSE symbol.
        """
        return self._s.get("/api/quote-equity", params={"symbol": symbol, "section": "trade_info"})

    def history(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        series: str = "EQ",
        as_df: bool = False,
    ) -> Any:
        """Historical OHLCV trade data for a date range.

        Args:
            symbol: NSE symbol.
            from_date: Start date (DD-MM-YYYY).
            to_date: End date (DD-MM-YYYY).
            series: Series type (default 'EQ').
            as_df: If True, return polars DataFrame.

        Returns:
            JSON response or polars DataFrame.
        """
        data = self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={
                "functionName": "getHistoricalTradeData",
                "symbol": symbol,
                "series": series,
                "fromDate": from_date,
                "toDate": to_date,
            },
        )
        if as_df:
            return to_dataframe(data)
        return data

    def series(self, symbol: str) -> Any:
        """Available series for historical trade data (EQ, BE, etc.).

        Args:
            symbol: NSE symbol.
        """
        return self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={"functionName": "histTradeDataSeries", "symbol": symbol},
        )

    def corporate_actions(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        as_df: bool = False,
    ) -> Any:
        """Corporate actions (dividends, bonus, splits) for a symbol.

        Args:
            symbol: NSE symbol.
            from_date: Start date (DD-MM-YYYY).
            to_date: End date (DD-MM-YYYY).
            as_df: If True, return polars DataFrame.
        """
        data = self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={
                "functionName": "getCorpAction",
                "symbol": symbol,
                "type": "W",
                "marketApiType": "equities",
                "ex_from_date": from_date,
                "ex_to_date": to_date,
            },
        )
        if as_df:
            return to_dataframe(data)
        return data

    def chart(self, symbol: str, days: str = "1D") -> Any:
        """Chart data for a symbol.

        Args:
            symbol: NSE symbol.
            days: Period — '1D' (intraday), '1W', '1M', '1Y'.
        """
        return self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={"functionName": "getSymbolChartData", "symbol": f"{symbol}EQN", "days": days},
        )

    def yearwise(self, symbol: str) -> Any:
        """Year-wise historical performance summary.

        Args:
            symbol: NSE symbol.
        """
        return self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={"functionName": "getYearwiseData", "symbol": f"{symbol}EQN"},
        )

    def index_list(self, symbol: str) -> Any:
        """List of indices a symbol belongs to.

        Args:
            symbol: NSE symbol.
        """
        return self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={"functionName": "getIndexList", "symbol": symbol},
        )
