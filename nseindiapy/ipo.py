"""IPO module — current and upcoming IPOs."""

from __future__ import annotations

from typing import Any

from nseindiapy._df import to_dataframe


class IPO:
    """Access IPO data."""

    def __init__(self, session: Any) -> None:
        self._s = session

    def current(self, as_df: bool = False) -> Any:
        """Currently open IPOs."""
        data = self._s.get("/api/ipo-current-issue")
        if as_df:
            return to_dataframe(data)
        return data

    def upcoming(self, as_df: bool = False) -> Any:
        """Upcoming IPOs."""
        data = self._s.get("/api/all-upcoming-issues", params={"category": "ipo"})
        if as_df:
            return to_dataframe(data)
        return data
