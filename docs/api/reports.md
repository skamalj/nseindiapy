# Reports

Access NSE daily and monthly reports.

## `client.reports.daily(key="CM")`

Daily report for a market segment.

```python
data = client.reports.daily("CM")
data = client.reports.daily("FO")
data = client.reports.daily("INDEX")
```

Values for `key`: `"CM"`, `"INDEX"`, `"SLBS"`, `"SME"`, `"FO"`, `"COM"`, `"CD"`, `"NBF"`, `"WDM"`, `"CBM"`, `"TRI-PARTY"`, `"EGR"`

## `client.reports.monthly(key="CM")`

Monthly report for a market segment.

```python
data = client.reports.monthly("CM")
data = client.reports.monthly("INDICES")
```

Values for `key`: `"CM"`, `"INDICES"`, `"SLBS"`, `"FO"`, `"CD"`, `"COM"`, `"IRD"`, `"WDM"`, `"CBM"`

## `client.reports.merged_daily(key="favCapital")`

Merged daily report.

```python
data = client.reports.merged_daily("favCapital")
data = client.reports.merged_daily("favDerivatives")
data = client.reports.merged_daily("favDebt")
```
