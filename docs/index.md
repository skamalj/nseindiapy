# nseindiapy

Python client for NSE India — National Stock Exchange of India.
Clean, typed access to equity quotes, indices, derivatives, corporate actions,
market data, IPOs, reports, and archive downloads. Both sync and async interfaces included.

|  |  |
|--|--|
| Quick Start | Install and go from zero to your first data pull in five minutes |
| API Reference | Full parameter reference for every module |

## Data Coverage

| Data | Method | as_df |
|------|--------|-------|
| Equity Quote (OHLC, 52W H/L) | `client.equity.quote("RELIANCE")` | — |
| Equity Metadata (ISIN, industry) | `client.equity.meta("TCS")` | — |
| Historical OHLCV | `client.equity.history("INFY", "01-01-2026", "31-03-2026")` | ✅ |
| Corporate Actions | `client.equity.corporate_actions("RELIANCE", ...)` | ✅ |
| Chart Data (1D/1W/1M/1Y) | `client.equity.chart("TCS", "1M")` | — |
| All Indices (live values) | `client.indices.all()` | — |
| Index Constituents | `client.indices.constituents("NIFTY 50")` | ✅ |
| GIFT Nifty | `client.indices.gift_nifty()` | — |
| Option Chain (Indices/Equity) | `client.derivatives.option_chain("NIFTY")` | — |
| Contract Info (expiries, strikes) | `client.derivatives.contract_info("BANKNIFTY")` | — |
| OI Spurts | `client.derivatives.oi_spurts()` | — |
| Market Status | `client.market.status()` | — |
| Top Gainers / Losers | `client.market.gainers()` | ✅ |
| Most Active | `client.market.most_active("volume")` | ✅ |
| 52-Week High/Low | `client.market.high_low_52week("high")` | ✅ |
| FII/DII Activity | `client.market.fii_dii()` | — |
| Block Deals | `client.market.block_deals()` | — |
| ETF Listings | `client.market.etf()` | ✅ |
| Holidays | `client.market.holidays()` | — |
| Corporate Actions (all) | `client.corporate.actions()` | ✅ |
| Announcements | `client.corporate.announcements()` | ✅ |
| Board Meetings | `client.corporate.board_meetings()` | ✅ |
| Shareholding | `client.corporate.shareholding("RELIANCE")` | — |
| IPO Current | `client.ipo.current()` | ✅ |
| IPO Upcoming | `client.ipo.upcoming()` | ✅ |
| Daily Reports | `client.reports.daily("CM")` | — |
| Monthly Reports | `client.reports.monthly("FO")` | — |
| Equity Bhavcopy | `client.archives.equity_bhavcopy("06-May-2026")` | ✅ |
| F&O Bhavcopy | `client.archives.fo_bhavcopy("06-May-2026")` | ✅ |
| Commodity Bhavcopy | `client.archives.commodity_bhavcopy("06-May-2026")` | ✅ |
| Indices Snapshot | `client.archives.indices_snapshot("06-May-2026")` | ✅ |
| F&O Open Interest | `client.archives.fo_open_interest("06-May-2026")` | ✅ |
| Equity Volatility | `client.archives.equity_volatility("06-May-2026")` | ✅ |
| + 25 more archive reports | `client.archives.download(key, date)` | ✅ |

> `as_df=True` requires `pip install nseindiapy[polars]`.
