"""Session management for NSE India API.

Handles cookie acquisition, refresh, rate limiting, and request headers.
NSE requires a valid session cookie obtained by first visiting the homepage.
The session auto-retries on auth failures with a fresh cookie.
"""

from __future__ import annotations

import time
import random
from typing import Any

import httpx

BASE_URL = "https://www.nseindia.com"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Default cookie TTL — NSE cookies last ~5-10 min. We recommend 4 min (240s).
DEFAULT_COOKIE_TTL = 240

# Pages to visit for cookie warmup (rotate to look more human)
_WARMUP_PAGES = ["/", "/market-data/live-equity-market", "/option-chain"]


class NSESession:
    """Synchronous session with automatic cookie management and rate limiting.

    Features:
    - Auto-acquires cookies on first request
    - Refreshes cookies before they expire (configurable TTL, default 4 min)
    - Auto-retries once on 401/403 with fresh cookies (handles session expiry)
    - Rate limits requests to ~3/sec by default
    - Rotates warmup pages to reduce bot-detection risk
    - All of this is transparent to the user
    """

    def __init__(
        self,
        rate_limit: float = 0.34,
        cookie_ttl: int = DEFAULT_COOKIE_TTL,
        **httpx_kwargs: Any,
    ) -> None:
        """
        Args:
            rate_limit: Minimum seconds between requests (default 0.34 = ~3 req/s).
                        Recommended: 0.34 for normal use, 1.0 for conservative/batch use.
            cookie_ttl: Seconds before refreshing session cookies (default 240 = 4 min).
                        NSE cookies last ~5-10 min. Recommended range: 180-300.
                        Lower = more homepage hits but fresher session.
                        Higher = fewer hits but risk of stale cookies.
            **httpx_kwargs: Extra kwargs forwarded to httpx.Client (proxy, timeout, etc.)
        """
        self._rate_limit = rate_limit
        self._cookie_ttl = cookie_ttl
        self._last_request_time: float = 0.0
        self._cookie_time: float = 0.0
        self._warmup_idx = 0
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers=_HEADERS,
            follow_redirects=True,
            timeout=30.0,
            **httpx_kwargs,
        )
        self._refresh_cookies()

    def _refresh_cookies(self) -> None:
        """Visit a page to get fresh session cookies."""
        self._throttle()
        page = _WARMUP_PAGES[self._warmup_idx % len(_WARMUP_PAGES)]
        self._warmup_idx += 1
        self._client.get(page)
        self._cookie_time = time.time()

    def _throttle(self) -> None:
        """Enforce rate limit between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._rate_limit:
            time.sleep(self._rate_limit - elapsed)
        self._last_request_time = time.time()

    def _ensure_cookies(self) -> None:
        """Refresh cookies if they are stale."""
        if time.time() - self._cookie_time > self._cookie_ttl:
            self._refresh_cookies()

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make a GET request and return parsed JSON.

        Auto-retries once with fresh cookies on 401/403.

        Args:
            path: URL path (e.g. '/api/marketStatus'). Can include query string.
            params: Optional query parameters.

        Returns:
            Parsed JSON response.

        Raises:
            httpx.HTTPStatusError: On persistent 4xx/5xx responses.
        """
        self._ensure_cookies()
        self._throttle()
        resp = self._client.get(path, params=params)

        # Auto-retry on auth/session failures
        if resp.status_code in (401, 403):
            self._refresh_cookies()
            self._throttle()
            resp = self._client.get(path, params=params)

        resp.raise_for_status()
        return resp.json()

    def get_response(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """Make a GET request and return the raw httpx Response.

        Auto-retries once with fresh cookies on 401/403.

        Args:
            path: URL path.
            params: Optional query parameters.

        Returns:
            httpx.Response object.
        """
        self._ensure_cookies()
        self._throttle()
        resp = self._client.get(path, params=params)

        if resp.status_code in (401, 403):
            self._refresh_cookies()
            self._throttle()
            resp = self._client.get(path, params=params)

        resp.raise_for_status()
        return resp

    def get_bytes(self, url: str) -> bytes:
        """Download raw bytes from a URL (for archive/CSV downloads).

        Auto-retries once with fresh cookies on 401/403.

        Args:
            url: Full URL to download from.

        Returns:
            Raw response bytes.
        """
        self._ensure_cookies()
        self._throttle()
        resp = self._client.get(url)

        if resp.status_code in (401, 403):
            self._refresh_cookies()
            self._throttle()
            resp = self._client.get(url)

        resp.raise_for_status()
        return resp.content

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "NSESession":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncNSESession:
    """Async session with automatic cookie management and rate limiting.

    Same features as NSESession but for async/await usage.
    """

    def __init__(
        self,
        rate_limit: float = 0.34,
        cookie_ttl: int = DEFAULT_COOKIE_TTL,
        **httpx_kwargs: Any,
    ) -> None:
        self._rate_limit = rate_limit
        self._cookie_ttl = cookie_ttl
        self._last_request_time: float = 0.0
        self._cookie_time: float = 0.0
        self._warmup_idx = 0
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=_HEADERS,
            follow_redirects=True,
            timeout=30.0,
            **httpx_kwargs,
        )

    async def _refresh_cookies(self) -> None:
        """Visit a page to get fresh session cookies."""
        await self._async_throttle()
        page = _WARMUP_PAGES[self._warmup_idx % len(_WARMUP_PAGES)]
        self._warmup_idx += 1
        await self._client.get(page)
        self._cookie_time = time.time()

    async def _async_throttle(self) -> None:
        """Enforce rate limit between requests."""
        import asyncio

        elapsed = time.time() - self._last_request_time
        if elapsed < self._rate_limit:
            await asyncio.sleep(self._rate_limit - elapsed)
        self._last_request_time = time.time()

    async def _ensure_cookies(self) -> None:
        if self._cookie_time == 0.0 or time.time() - self._cookie_time > self._cookie_ttl:
            await self._refresh_cookies()

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make an async GET request and return parsed JSON."""
        await self._ensure_cookies()
        await self._async_throttle()
        resp = await self._client.get(path, params=params)

        if resp.status_code in (401, 403):
            await self._refresh_cookies()
            await self._async_throttle()
            resp = await self._client.get(path, params=params)

        resp.raise_for_status()
        return resp.json()

    async def get_response(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Make an async GET request and return raw response."""
        await self._ensure_cookies()
        await self._async_throttle()
        resp = await self._client.get(path, params=params)

        if resp.status_code in (401, 403):
            await self._refresh_cookies()
            await self._async_throttle()
            resp = await self._client.get(path, params=params)

        resp.raise_for_status()
        return resp

    async def get_bytes(self, url: str) -> bytes:
        """Download raw bytes from a URL."""
        await self._ensure_cookies()
        await self._async_throttle()
        resp = await self._client.get(url)

        if resp.status_code in (401, 403):
            await self._refresh_cookies()
            await self._async_throttle()
            resp = await self._client.get(url)

        resp.raise_for_status()
        return resp.content

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncNSESession":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
