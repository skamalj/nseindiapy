"""Derivatives module — option chains, F&O contracts, OI data."""

from __future__ import annotations

from typing import Any

from nseindiapy._df import to_dataframe


class Derivatives:
    """Access F&O derivatives data — option chains, contract info, OI spurts."""

    def __init__(self, session: Any) -> None:
        self._s = session

    def option_chain(
        self,
        symbol: str = "NIFTY",
        type: str = "Indices",
        expiry: str | None = None,
    ) -> Any:
        """Option chain data (v3) for indices or equities.

        Args:
            symbol: Symbol (e.g. 'NIFTY', 'BANKNIFTY', 'RELIANCE').
            type: 'Indices' or 'Equity'.
            expiry: Expiry date (DD-Mon-YYYY, e.g. '26-May-2026'). If None, returns all expiries.
        """
        params: dict[str, str] = {"type": type, "symbol": symbol}
        if expiry:
            params["expiry"] = expiry
        return self._s.get("/api/option-chain-v3", params=params)

    def contract_info(self, symbol: str = "NIFTY") -> Any:
        """Contract info — available expiry dates and strike prices.

        Args:
            symbol: Symbol (e.g. 'NIFTY', 'BANKNIFTY', 'RELIANCE').
        """
        return self._s.get("/api/option-chain-contract-info", params={"symbol": symbol})

    def oi_spurts(self) -> Any:
        """OI spurts in contracts."""
        return self._s.get("/api/live-analysis-oi-spurts-contracts")
