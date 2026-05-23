# Equity

Access equity/stock data for individual symbols.

## `client.equity.quote(symbol)`

Full equity quote — price, OHLC, volume, 52W high/low.

```python
data = client.equity.quote("RELIANCE")
```

## `client.equity.meta(symbol)`

Equity metadata — ISIN, industry, listing date, face value.

```python
data = client.equity.meta("TCS")
```

## `client.equity.trade_info(symbol)`

Trade information — delivery %, traded volume.

```python
data = client.equity.trade_info("INFY")
```

## `client.equity.history(symbol, from_date, to_date, series="EQ", as_df=False)`

Historical OHLCV trade data for a date range.

```python
# JSON
data = client.equity.history("INFY", "01-04-2026", "30-04-2026")

# polars DataFrame
df = client.equity.history("INFY", "01-04-2026", "30-04-2026", as_df=True)
```

Date format: `DD-MM-YYYY`

## `client.equity.series(symbol)`

Available series for historical trade data (EQ, BE, etc.).

```python
data = client.equity.series("RELIANCE")
# → ["EQ", "BE", ...]
```

## `client.equity.corporate_actions(symbol, from_date, to_date, as_df=False)`

Corporate actions (dividends, bonus, splits) for a symbol.

```python
data = client.equity.corporate_actions("RELIANCE", "01-01-2026", "22-05-2026")
```

## `client.equity.chart(symbol, days="1D")`

Chart data for a symbol.

```python
data = client.equity.chart("RELIANCE", "1D")  # intraday
data = client.equity.chart("TCS", "1Y")       # 1 year
```

Values for `days`: `"1D"`, `"1W"`, `"1M"`, `"1Y"`

## `client.equity.yearwise(symbol)`

Year-wise historical performance summary.

```python
data = client.equity.yearwise("RELIANCE")
```

## `client.equity.index_list(symbol)`

List of indices a symbol belongs to.

```python
data = client.equity.index_list("RELIANCE")
```
