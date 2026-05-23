# Corporate

Access corporate filings — actions, announcements, board meetings.

## `client.corporate.actions(index="equities", symbol=None, from_date=None, to_date=None, as_df=False)`

Corporate actions (dividends, bonus, splits).

```python
# All equity corporate actions
data = client.corporate.actions()

# For a specific symbol
data = client.corporate.actions(symbol="RELIANCE")

# Within date range
data = client.corporate.actions(from_date="01-01-2026", to_date="31-03-2026")

# Different segments
data = client.corporate.actions(index="debt")
data = client.corporate.actions(index="sme")
```

Values for `index`: `"equities"`, `"debt"`, `"mf"`, `"sme"`

## `client.corporate.announcements(index="equities", symbol=None, as_df=False)`

Corporate announcements.

```python
data = client.corporate.announcements()
data = client.corporate.announcements(index="sme")
data = client.corporate.announcements(index="invitsreits")
```

Values for `index`: `"equities"`, `"debt"`, `"mf"`, `"sme"`, `"sse"`, `"invitsreits"`, `"municipalBond"`

## `client.corporate.board_meetings(index="equities", as_df=False)`

Board meetings.

```python
data = client.corporate.board_meetings()
data = client.corporate.board_meetings(index="sme")
```

## `client.corporate.shareholding(symbol)`

Shareholding pattern for a symbol.

```python
data = client.corporate.shareholding("RELIANCE")
```

## `client.corporate.annual_reports(symbol, index="equities")`

Annual reports for a specific symbol.

```python
data = client.corporate.annual_reports("RELIANCE")
```

## `client.corporate.circulars(from_date=None, to_date=None)`

NSE circulars.

```python
data = client.corporate.circulars()
data = client.corporate.circulars(from_date="01-01-2026", to_date="31-03-2026")
```
