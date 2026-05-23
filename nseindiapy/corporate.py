"""Corporate module — actions, announcements, board meetings, shareholding, circulars."""

from __future__ import annotations

from typing import Any

from nseindiapy._df import to_dataframe


class Corporate:
    """Access corporate filings — actions, announcements, board meetings."""

    def __init__(self, session: Any) -> None:
        self._s = session

    def actions(
        self,
        index: str = "equities",
        symbol: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        as_df: bool = False,
    ) -> Any:
        """Corporate actions (dividends, bonus, splits).

        Args:
            index: 'equities', 'debt', 'mf', 'sme'.
            symbol: Filter by symbol (optional).
            from_date: Start date DD-MM-YYYY (optional).
            to_date: End date DD-MM-YYYY (optional).
            as_df: If True, return polars DataFrame.
        """
        params: dict[str, str] = {"index": index}
        if symbol:
            params["symbol"] = symbol
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        data = self._s.get("/api/corporates-corporateActions", params=params)
        if as_df:
            return to_dataframe(data)
        return data

    def announcements(
        self,
        index: str = "equities",
        symbol: str | None = None,
        as_df: bool = False,
    ) -> Any:
        """Corporate announcements.

        Args:
            index: 'equities', 'debt', 'mf', 'sme', 'sse', 'invitsreits', 'municipalBond'.
            symbol: Filter by symbol (optional).
            as_df: If True, return polars DataFrame.
        """
        params: dict[str, str] = {"index": index}
        if symbol:
            params["symbol"] = symbol
        data = self._s.get("/api/corporate-announcements", params=params)
        if as_df:
            return to_dataframe(data)
        return data

    def board_meetings(self, index: str = "equities", as_df: bool = False) -> Any:
        """Board meetings.

        Args:
            index: 'equities' or 'sme'.
            as_df: If True, return polars DataFrame.
        """
        data = self._s.get("/api/corporate-board-meetings", params={"index": index})
        if as_df:
            return to_dataframe(data)
        return data

    def shareholding(self, symbol: str) -> Any:
        """Shareholding pattern for a symbol.

        Args:
            symbol: NSE symbol.
        """
        return self._s.get(
            "/api/NextApi/apiClient/GetQuoteApi",
            params={"functionName": "getRegDetails", "symbol": symbol},
        )

    def annual_reports(self, symbol: str, index: str = "equities") -> Any:
        """Annual reports for a specific symbol.

        Args:
            symbol: NSE symbol (required).
            index: 'equities' or 'debt'.
        """
        return self._s.get("/api/annual-reports", params={"index": index, "symbol": symbol})

    def circulars(self, from_date: str | None = None, to_date: str | None = None) -> Any:
        """NSE circulars.

        Args:
            from_date: Start date DD-MM-YYYY (optional).
            to_date: End date DD-MM-YYYY (optional).
        """
        params: dict[str, str] = {}
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        return self._s.get("/api/circulars", params=params)
