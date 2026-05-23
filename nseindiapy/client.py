"""Main client classes — NSEClient (sync) and AsyncNSEClient (async)."""

from __future__ import annotations

from typing import Any

from nseindiapy._session import NSESession, AsyncNSESession
from nseindiapy.equity import Equity
from nseindiapy.indices import Indices
from nseindiapy.derivatives import Derivatives
from nseindiapy.market import Market
from nseindiapy.corporate import Corporate
from nseindiapy.ipo import IPO
from nseindiapy.reports import Reports
from nseindiapy.archives import Archives


class NSEClient:
    """Synchronous client for NSE India.

    Usage:
        client = NSEClient()
        quote = client.equity.quote("RELIANCE")
        indices = client.indices.all()
        client.close()

    Or as context manager:
        with NSEClient() as client:
            quote = client.equity.quote("TCS")

    Session configuration:
        # Conservative settings for batch downloads
        client = NSEClient(rate_limit=1.0, cookie_ttl=180)

        # Default (recommended for interactive use)
        client = NSEClient()  # rate_limit=0.34, cookie_ttl=240
    """

    def __init__(
        self,
        rate_limit: float = 0.34,
        cookie_ttl: int = 240,
        **httpx_kwargs: Any,
    ) -> None:
        """
        Args:
            rate_limit: Minimum seconds between requests (default 0.34 = ~3 req/s).
                        Use 1.0 for batch/bulk operations to be safe.
            cookie_ttl: Seconds before refreshing session cookies (default 240 = 4 min).
                        NSE cookies last ~5-10 min. Recommended: 180-300.
            **httpx_kwargs: Extra kwargs forwarded to httpx.Client
                (proxy, timeout, verify, etc.)
        """
        self._session = NSESession(rate_limit=rate_limit, cookie_ttl=cookie_ttl, **httpx_kwargs)
        self.equity = Equity(self._session)
        self.indices = Indices(self._session)
        self.derivatives = Derivatives(self._session)
        self.market = Market(self._session)
        self.corporate = Corporate(self._session)
        self.ipo = IPO(self._session)
        self.reports = Reports(self._session)
        self.archives = Archives(self._session)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> "NSEClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncNSEClient:
    """Async client for NSE India. Identical API to NSEClient — just await the calls.

    Usage:
        async with AsyncNSEClient() as client:
            quote = await client.equity.quote("RELIANCE")
    """

    def __init__(
        self,
        rate_limit: float = 0.34,
        cookie_ttl: int = 240,
        **httpx_kwargs: Any,
    ) -> None:
        """
        Args:
            rate_limit: Minimum seconds between requests (default 0.34 = ~3 req/s).
            cookie_ttl: Seconds before refreshing session cookies (default 240 = 4 min).
            **httpx_kwargs: Extra kwargs forwarded to httpx.AsyncClient.
        """
        self._session = AsyncNSESession(rate_limit=rate_limit, cookie_ttl=cookie_ttl, **httpx_kwargs)
        self.equity = Equity(self._session)
        self.indices = Indices(self._session)
        self.derivatives = Derivatives(self._session)
        self.market = Market(self._session)
        self.corporate = Corporate(self._session)
        self.ipo = IPO(self._session)
        self.reports = Reports(self._session)
        self.archives = Archives(self._session)

    async def close(self) -> None:
        await self._session.close()

    async def __aenter__(self) -> "AsyncNSEClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
