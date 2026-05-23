# Quick Start

## Installation

```bash
pip install nseindiapy
```

Add polars DataFrame support (needed for `as_df=True`):

```bash
pip install nseindiapy[polars]
```

## Your first data pull

```python
from nseindiapy import NSEClient

client = NSEClient()

# Market status
status = client.market.status()

# Equity quote — full OHLC, volume, 52W high/low
quote = client.equity.quote("RELIANCE")

# Historical data as polars DataFrame
hist_df = client.equity.history(
    "TCS", from_date="01-01-2026", to_date="31-03-2026", as_df=True
)

# Option chain for NIFTY
oc = client.derivatives.option_chain("NIFTY")

# Download bhavcopy as DataFrame
bhavcopy_df = client.archives.equity_bhavcopy("06-May-2026", as_df=True)

client.close()
```

## Context Manager

```python
with NSEClient() as client:
    gainers = client.market.gainers()
    losers = client.market.losers()
```

## Async

`AsyncNSEClient` has an identical API — just `await` the calls:

```python
import asyncio
from nseindiapy import AsyncNSEClient

async def main():
    async with AsyncNSEClient() as client:
        quote = await client.equity.quote("RELIANCE")
        indices = await client.indices.all()

asyncio.run(main())
```

## Session Configuration

```python
# Default — good for interactive use (~3 requests/sec)
client = NSEClient()

# Conservative — for batch downloads, long-running scripts
client = NSEClient(rate_limit=1.0, cookie_ttl=180)

# With proxy
client = NSEClient(proxy="http://myproxy:8080")
```

| Parameter | Default | Recommended | Description |
|-----------|---------|-------------|-------------|
| `rate_limit` | 0.34 | 0.34–1.0 | Minimum seconds between requests |
| `cookie_ttl` | 240 | 180–300 | Seconds before refreshing session cookies |

## What next?

- [API Reference](api/equity.md) — full parameter docs for every module
