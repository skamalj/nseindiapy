# Market

Access market-wide data — status, movers, deals, FII/DII.

## `client.market.status()`

Current market status (open/closed) for all segments.

```python
data = client.market.status()
# → {"marketState": [...], "marketcap": {...}, "giftnifty": {...}}
```

## `client.market.all_status()`

All market segment statuses (CM, FO, CD, COM, etc.).

```python
data = client.market.all_status()
```

## `client.market.turnover()`

Market turnover data. Returns `None` if market is closed.

```python
data = client.market.turnover()
```

## `client.market.pre_open(key="NIFTY")`

Pre-open market data.

```python
data = client.market.pre_open("NIFTY")
data = client.market.pre_open("BANKNIFTY")
data = client.market.pre_open("ALL")
```

Values for `key`: `"ALL"`, `"NIFTY"`, `"BANKNIFTY"`, `"SME"`, `"FO"`

## `client.market.gainers(as_df=False)`

Top gainers.

```python
data = client.market.gainers()
df = client.market.gainers(as_df=True)
```

## `client.market.losers(as_df=False)`

Top losers.

```python
data = client.market.losers()
```

## `client.market.most_active(by="volume", as_df=False)`

Most active securities.

```python
data = client.market.most_active("volume")
data = client.market.most_active("value", as_df=True)
```

## `client.market.high_low_52week(which="high", as_df=False)`

52-week high or low stocks.

```python
data = client.market.high_low_52week("high")
data = client.market.high_low_52week("low", as_df=True)
```

## `client.market.block_deals()`

Block deals.

```python
data = client.market.block_deals()
```

## `client.market.fii_dii()`

FII/FPI and DII trading activity.

```python
data = client.market.fii_dii()
```

## `client.market.holidays(type="trading")`

Trading or clearing holidays.

```python
data = client.market.holidays("trading")
data = client.market.holidays("clearing")
```

## `client.market.etf(as_df=False)`

All ETFs listed on NSE.

```python
data = client.market.etf()
df = client.market.etf(as_df=True)
```

## `client.market.equity_master()`

Complete equity master data (all listed securities).

```python
data = client.market.equity_master()
```
