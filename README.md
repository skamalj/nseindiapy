# nseindiapy

Python client for NSE India — National Stock Exchange of India.

Clean, typed access to equity quotes, indices, derivatives, corporate actions,
market data, IPOs, reports, and archive downloads. Both sync and async interfaces included.

📖 [Full documentation → skamalj.github.io/nseindiapy](https://skamalj.github.io/nseindiapy/)

## Installation

```bash
pip install nseindiapy
```

With polars DataFrame support:

```bash
pip install nseindiapy[polars]
```

## Quick Start

```python
from nseindiapy import NSEClient

client = NSEClient()

# Equity quote
quote = client.equity.quote("RELIANCE")

# Historical OHLCV data
hist = client.equity.history("TCS", from_date="01-01-2026", to_date="31-03-2026")

# All indices
indices = client.indices.all()

# Option chain
oc = client.derivatives.option_chain("NIFTY")

# Market movers
gainers = client.market.gainers()

# Download bhavcopy as polars DataFrame
df = client.archives.equity_bhavcopy("06-May-2026", as_df=True)

client.close()
```

### Async

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
# Default — good for interactive use
client = NSEClient()

# Conservative — for batch downloads, long-running scripts
client = NSEClient(rate_limit=1.0, cookie_ttl=180)

# With proxy
client = NSEClient(proxy="http://myproxy:8080")
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `rate_limit` | 0.34 (~3 req/s) | Minimum seconds between requests |
| `cookie_ttl` | 240 (4 min) | Seconds before refreshing session cookies. Recommended: 180-300 |

## Modules

| Module | Methods | Description |
|--------|---------|-------------|
| `client.equity` | quote, meta, trade_info, history, series, corporate_actions, chart, yearwise, index_list | Equity/stock data for individual symbols |
| `client.indices` | all, names, constituents, chart, gift_nifty | Index data — values, constituents, charts |
| `client.derivatives` | option_chain, contract_info, oi_spurts | F&O option chains, contract info, OI data |
| `client.market` | status, all_status, turnover, pre_open, gainers, losers, most_active, high_low_52week, block_deals, fii_dii, holidays, etf, equity_master | Market-wide data |
| `client.corporate` | actions, announcements, board_meetings, shareholding, annual_reports, circulars | Corporate filings |
| `client.ipo` | current, upcoming | IPO listings |
| `client.reports` | daily, monthly, merged_daily | Daily/monthly reports for all segments |
| `client.archives` | equity_bhavcopy, fo_bhavcopy, commodity_bhavcopy, indices_snapshot, equity_volatility, fo_open_interest, + 25 more via download() | Archive downloads (bhavcopy, volatility, OI, etc.) |

## Archives — Available Reports

Use `client.archives.download(report_key, date)` with any of these keys:

**Equities:** `equities_bhavcopy`, `equities_full_bhavcopy`, `equities_volatility`, `equities_var_margin`, `equities_turnover`

**Indices:** `indices_snapshot`, `indices_mcap_weight_beta`, `indices_impact_cost`, `indices_mcap_weight`, `indices_nifty50_top10`

**F&O:** `fo_bhavcopy`, `fo_market_activity`, `fo_volatility`, `fo_settlement_prices`, `fo_combined`, `fo_open_interest`, `fo_ban_period`, `fo_position_limits`

**Commodity:** `commodity_bhavcopy`, `commodity_stock_position`, `commodity_volatility`, `commodity_base_price`, `commodity_market_activity`

**Currency:** `currency_settlement`, `currency_volatility`, `currency_base_price`, `currency_market_activity`, `currency_bhavcopy`

```python
# Download any report — returns bytes or DataFrame
data = client.archives.download("fo_open_interest", "06-May-2026")
df = client.archives.download("equities_volatility", "06-May-2026", as_df=True)
```

## Features

- **Sync + Async** — `NSEClient` and `AsyncNSEClient` with identical APIs
- **Typed & documented** — full docstrings, type hints throughout
- **Polars support** — optional `as_df=True` returns a polars DataFrame
- **Smart session management** — auto cookie refresh, retry on auth failures, rotating warmup pages
- **Rate limiting** — built-in, configurable, respects NSE's ~3 req/s limit
- **No heavy deps** — only `httpx` required

## License

MIT
