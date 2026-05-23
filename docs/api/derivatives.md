# Derivatives

Access F&O derivatives data — option chains, contract info, OI data.

## `client.derivatives.option_chain(symbol, type="Indices", expiry=None)`

Option chain data for indices or equities.

```python
# NIFTY index option chain
data = client.derivatives.option_chain("NIFTY")

# Equity option chain
data = client.derivatives.option_chain("RELIANCE", type="Equity")

# With specific expiry
data = client.derivatives.option_chain("NIFTY", expiry="26-May-2026")
```

| Parameter | Values |
|-----------|--------|
| `type` | `"Indices"`, `"Equity"` |
| `expiry` | `"DD-Mon-YYYY"` or `None` (all expiries) |

## `client.derivatives.contract_info(symbol)`

Contract info — available expiry dates and strike prices.

```python
data = client.derivatives.contract_info("NIFTY")
data = client.derivatives.contract_info("BANKNIFTY")
data = client.derivatives.contract_info("RELIANCE")
```

## `client.derivatives.oi_spurts()`

OI spurts in contracts.

```python
data = client.derivatives.oi_spurts()
```
