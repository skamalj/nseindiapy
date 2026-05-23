# Archives

Download NSE reports and archives via the `/api/reports` endpoint.
All methods return raw bytes by default. Pass `as_df=True` to auto-download
and parse as a polars DataFrame.

## Convenience Methods

### `client.archives.equity_bhavcopy(date, as_df=False)`

Download equity bhavcopy (PR.zip).

```python
raw = client.archives.equity_bhavcopy("06-May-2026")
df = client.archives.equity_bhavcopy("06-May-2026", as_df=True)
```

### `client.archives.equity_full_bhavcopy(date, as_df=False)`

Full bhavcopy with delivery data.

```python
df = client.archives.equity_full_bhavcopy("06-May-2026", as_df=True)
```

### `client.archives.fo_bhavcopy(date, as_df=False)`

F&O bhavcopy (fo.zip).

```python
df = client.archives.fo_bhavcopy("06-May-2026", as_df=True)
```

### `client.archives.commodity_bhavcopy(date, as_df=False)`

Commodity bhavcopy.

```python
df = client.archives.commodity_bhavcopy("06-May-2026", as_df=True)
```

### `client.archives.indices_snapshot(date, as_df=False)`

Daily indices snapshot.

```python
df = client.archives.indices_snapshot("06-May-2026", as_df=True)
```

### `client.archives.fo_open_interest(date, as_df=False)`

F&O NCL open interest.

```python
df = client.archives.fo_open_interest("06-May-2026", as_df=True)
```

### `client.archives.equity_volatility(date, as_df=False)`

Daily equity volatility.

```python
df = client.archives.equity_volatility("06-May-2026", as_df=True)
```

## Generic Download

### `client.archives.download(report_key, date, as_df=False)`

Download any report by key.

```python
data = client.archives.download("fo_settlement_prices", "06-May-2026")
df = client.archives.download("commodity_volatility", "06-May-2026", as_df=True)
```

### `Archives.available_reports()`

List all available report keys.

```python
keys = client.archives.available_reports()
# → ['commodity_base_price', 'commodity_bhavcopy', ..., 'indices_snapshot', ...]
```

## All Report Keys

**Equities (capital-market):**

- `equities_bhavcopy` — CM - Bhavcopy (PR.zip)
- `equities_full_bhavcopy` — Full Bhavcopy and Security Deliverable data
- `equities_volatility` — CM - Daily Volatility
- `equities_var_margin` — CM - VaR Margin Rates (End of day)
- `equities_turnover` — CM - Category-wise Turnover
- `equities_market_pulse` — NSE Market Pulse (.pdf)

**Indices (capital-market):**

- `indices_snapshot` — Daily Snapshot
- `indices_mcap_weight_beta` — Market Capitalisation, Weightage, Beta for NIFTY 50 & NIFTY Next 50
- `indices_impact_cost` — Impact Cost
- `indices_mcap_weight` — Indices - Market Capitalisation & Weightage
- `indices_fixed_income` — Index Dashboard - Fixed Income
- `indices_nifty50_top10` — NIFTY 50 Top 10 Holdings (csv)

**F&O (derivatives — equity):**

- `fo_bhavcopy` — F&O - Bhavcopy (fo.zip)
- `fo_market_activity` — F&O - Market Activity Report
- `fo_volatility` — F&O - Daily Volatility
- `fo_settlement_prices` — F&O - Daily Settlement Prices
- `fo_combined` — F&O - Combined Report
- `fo_open_interest` — F&O - NCL Open Interest
- `fo_ban_period` — F&O - Security in ban period
- `fo_position_limits` — F&O - Clientwise Position Limits
- `fo_span_risk` — F&O - Span Risk Parameter File (2nd intra-day)

**Commodity (derivatives):**

- `commodity_bhavcopy` — COM - Bhavcopy (zip)
- `commodity_stock_position` — COM - Daily Stock Position Report
- `commodity_volatility` — COM - Volatility
- `commodity_base_price` — COM - Base Price
- `commodity_market_activity` — COM - Market Activity Report

**Currency (derivatives):**

- `currency_settlement` — CD - Settlement Prices
- `currency_volatility` — CD - Volatility
- `currency_base_price` — CD - Base Price
- `currency_market_activity` — CD - Market Activity Report
- `currency_mode_of_trading` — CD - Mode of Trading
- `currency_bhavcopy` — CD-Bhavcopy File (DAT)
- `currency_contract_files` — CD-MII - Contract Files (.gz)

## Date Format

All archive methods use `DD-Mon-YYYY` format: `"06-May-2026"`, `"15-Jan-2026"`.
