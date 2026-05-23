# Indices

Access NSE index data.

## `client.indices.all()`

All indices with current values (NIFTY 50, Bank NIFTY, VIX, etc.).

```python
data = client.indices.all()
# → {"data": [...], "timestamp": "...", "advances": N, "declines": N}
```

## `client.indices.names()`

List of all index names.

```python
data = client.indices.names()
```

## `client.indices.constituents(index, as_df=False)`

Stocks in a specific index.

```python
data = client.indices.constituents("NIFTY 50")
data = client.indices.constituents("NIFTY BANK", as_df=True)
```

## `client.indices.chart(index)`

Intraday chart data for an index.

```python
data = client.indices.chart("NIFTY 50")
```

## `client.indices.gift_nifty()`

GIFT Nifty (SGX Nifty) data.

```python
data = client.indices.gift_nifty()
```
