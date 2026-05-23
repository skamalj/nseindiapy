"""Live integration tests against NSE India — covers ALL methods.

Rate limiting and cookie management is handled by the client itself.
Run with: uv run pytest tests/test_live.py -v -s
"""

import pytest

from nseindiapy import NSEClient


@pytest.fixture(scope="module")
def client():
    """Shared client — rate_limit=1s, cookie_ttl=180s (conservative)."""
    c = NSEClient(rate_limit=1.0, cookie_ttl=180)
    yield c
    c.close()


# ═══════════════════════════════════════════════════════════════════════════════
# MARKET MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class TestMarket:
    def test_status(self, client: NSEClient):
        data = client.market.status()
        assert data is not None
        assert "marketState" in data
        print(f"  ✓ market.status()")

    def test_all_status(self, client: NSEClient):
        data = client.market.all_status()
        assert data is not None
        print(f"  ✓ market.all_status()")

    def test_turnover(self, client: NSEClient):
        data = client.market.turnover()
        # None outside market hours — that's OK
        print(f"  ✓ market.turnover() -> {type(data).__name__}")

    def test_pre_open(self, client: NSEClient):
        data = client.market.pre_open("NIFTY")
        assert data is not None
        print(f"  ✓ market.pre_open('NIFTY')")

    def test_gainers(self, client: NSEClient):
        data = client.market.gainers()
        assert data is not None
        print(f"  ✓ market.gainers()")

    def test_losers(self, client: NSEClient):
        data = client.market.losers()
        assert data is not None
        print(f"  ✓ market.losers()")

    def test_most_active(self, client: NSEClient):
        data = client.market.most_active("volume")
        assert data is not None
        print(f"  ✓ market.most_active('volume')")

    def test_high_low_52week(self, client: NSEClient):
        data = client.market.high_low_52week("high")
        assert data is not None
        print(f"  ✓ market.high_low_52week('high')")

    def test_block_deals(self, client: NSEClient):
        data = client.market.block_deals()
        assert data is not None
        print(f"  ✓ market.block_deals()")

    def test_fii_dii(self, client: NSEClient):
        data = client.market.fii_dii()
        assert data is not None
        print(f"  ✓ market.fii_dii()")

    def test_holidays(self, client: NSEClient):
        data = client.market.holidays("trading")
        assert data is not None
        print(f"  ✓ market.holidays()")

    def test_etf(self, client: NSEClient):
        data = client.market.etf()
        assert data is not None
        print(f"  ✓ market.etf()")

    def test_equity_master(self, client: NSEClient):
        data = client.market.equity_master()
        assert data is not None
        print(f"  ✓ market.equity_master()")


# ═══════════════════════════════════════════════════════════════════════════════
# EQUITY MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class TestEquity:
    def test_quote(self, client: NSEClient):
        data = client.equity.quote("RELIANCE")
        assert data is not None
        print(f"  ✓ equity.quote('RELIANCE')")

    def test_meta(self, client: NSEClient):
        data = client.equity.meta("TCS")
        assert data is not None
        print(f"  ✓ equity.meta('TCS')")

    def test_trade_info(self, client: NSEClient):
        data = client.equity.trade_info("INFY")
        assert data is not None
        print(f"  ✓ equity.trade_info('INFY')")

    def test_history(self, client: NSEClient):
        data = client.equity.history("INFY", from_date="01-04-2026", to_date="30-04-2026")
        assert data is not None
        print(f"  ✓ equity.history('INFY')")

    def test_series(self, client: NSEClient):
        data = client.equity.series("RELIANCE")
        assert data is not None
        print(f"  ✓ equity.series('RELIANCE')")

    def test_corporate_actions(self, client: NSEClient):
        data = client.equity.corporate_actions("RELIANCE", "01-01-2026", "22-05-2026")
        assert data is not None
        print(f"  ✓ equity.corporate_actions('RELIANCE')")

    def test_chart(self, client: NSEClient):
        data = client.equity.chart("RELIANCE", "1D")
        assert data is not None
        print(f"  ✓ equity.chart('RELIANCE', '1D')")

    def test_yearwise(self, client: NSEClient):
        data = client.equity.yearwise("RELIANCE")
        assert data is not None
        print(f"  ✓ equity.yearwise('RELIANCE')")

    def test_index_list(self, client: NSEClient):
        data = client.equity.index_list("RELIANCE")
        assert data is not None
        print(f"  ✓ equity.index_list('RELIANCE')")


# ═══════════════════════════════════════════════════════════════════════════════
# INDICES MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class TestIndices:
    def test_all(self, client: NSEClient):
        data = client.indices.all()
        assert data is not None
        assert "data" in data
        print(f"  ✓ indices.all()")

    def test_names(self, client: NSEClient):
        data = client.indices.names()
        assert data is not None
        print(f"  ✓ indices.names()")

    def test_constituents(self, client: NSEClient):
        data = client.indices.constituents("NIFTY 50")
        assert data is not None
        assert "data" in data
        print(f"  ✓ indices.constituents('NIFTY 50')")

    def test_chart(self, client: NSEClient):
        data = client.indices.chart("NIFTY 50")
        assert data is not None
        print(f"  ✓ indices.chart('NIFTY 50')")

    def test_gift_nifty(self, client: NSEClient):
        data = client.indices.gift_nifty()
        assert data is not None
        print(f"  ✓ indices.gift_nifty()")


# ═══════════════════════════════════════════════════════════════════════════════
# DERIVATIVES MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class TestDerivatives:
    def test_option_chain(self, client: NSEClient):
        data = client.derivatives.option_chain("NIFTY", type="Indices")
        assert data is not None
        print(f"  ✓ derivatives.option_chain('NIFTY')")

    def test_contract_info(self, client: NSEClient):
        data = client.derivatives.contract_info("NIFTY")
        assert data is not None
        print(f"  ✓ derivatives.contract_info('NIFTY')")

    def test_oi_spurts(self, client: NSEClient):
        data = client.derivatives.oi_spurts()
        assert data is not None
        print(f"  ✓ derivatives.oi_spurts()")


# ═══════════════════════════════════════════════════════════════════════════════
# CORPORATE MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class TestCorporate:
    def test_actions(self, client: NSEClient):
        data = client.corporate.actions(index="equities")
        assert data is not None
        print(f"  ✓ corporate.actions()")

    def test_announcements(self, client: NSEClient):
        data = client.corporate.announcements(index="equities")
        assert data is not None
        print(f"  ✓ corporate.announcements()")

    def test_board_meetings(self, client: NSEClient):
        data = client.corporate.board_meetings()
        assert data is not None
        print(f"  ✓ corporate.board_meetings()")

    def test_shareholding(self, client: NSEClient):
        data = client.corporate.shareholding("RELIANCE")
        assert data is not None
        print(f"  ✓ corporate.shareholding('RELIANCE')")

    def test_annual_reports(self, client: NSEClient):
        data = client.corporate.annual_reports("RELIANCE")
        assert data is not None
        print(f"  ✓ corporate.annual_reports('RELIANCE')")

    def test_circulars(self, client: NSEClient):
        data = client.corporate.circulars()
        assert data is not None
        print(f"  ✓ corporate.circulars()")


# ═══════════════════════════════════════════════════════════════════════════════
# IPO MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class TestIPO:
    def test_current(self, client: NSEClient):
        data = client.ipo.current()
        assert data is not None
        print(f"  ✓ ipo.current()")

    def test_upcoming(self, client: NSEClient):
        data = client.ipo.upcoming()
        assert data is not None
        print(f"  ✓ ipo.upcoming()")


# ═══════════════════════════════════════════════════════════════════════════════
# REPORTS MODULE
# ═══════════════════════════════════════════════════════════════════════════════

class TestReports:
    def test_daily(self, client: NSEClient):
        data = client.reports.daily("CM")
        assert data is not None
        print(f"  ✓ reports.daily('CM')")

    def test_monthly(self, client: NSEClient):
        data = client.reports.monthly("CM")
        assert data is not None
        print(f"  ✓ reports.monthly('CM')")

    def test_merged_daily(self, client: NSEClient):
        data = client.reports.merged_daily("favCapital")
        assert data is not None
        print(f"  ✓ reports.merged_daily('favCapital')")


# ═══════════════════════════════════════════════════════════════════════════════
# ARCHIVES MODULE — uses /api/reports endpoint
# ═══════════════════════════════════════════════════════════════════════════════

class TestArchives:
    """Archives tests use 06-May-2026 (a confirmed trading day)."""

    TRADE_DATE = "06-May-2026"

    def test_available_reports(self, client: NSEClient):
        reports = client.archives.available_reports()
        assert len(reports) > 20
        print(f"  ✓ archives.available_reports() -> {len(reports)} reports")

    def test_equity_bhavcopy(self, client: NSEClient):
        data = client.archives.equity_bhavcopy(self.TRADE_DATE)
        assert data is not None
        print(f"  ✓ archives.equity_bhavcopy() -> {type(data).__name__}")

    def test_fo_bhavcopy(self, client: NSEClient):
        data = client.archives.fo_bhavcopy(self.TRADE_DATE)
        assert data is not None
        print(f"  ✓ archives.fo_bhavcopy() -> {type(data).__name__}")

    def test_indices_snapshot(self, client: NSEClient):
        data = client.archives.indices_snapshot(self.TRADE_DATE)
        assert data is not None
        print(f"  ✓ archives.indices_snapshot() -> {type(data).__name__}")

    def test_commodity_bhavcopy(self, client: NSEClient):
        data = client.archives.commodity_bhavcopy(self.TRADE_DATE)
        assert data is not None
        print(f"  ✓ archives.commodity_bhavcopy() -> {type(data).__name__}")

    def test_equity_volatility(self, client: NSEClient):
        data = client.archives.equity_volatility(self.TRADE_DATE)
        assert data is not None
        print(f"  ✓ archives.equity_volatility() -> {type(data).__name__}")

    def test_fo_open_interest(self, client: NSEClient):
        data = client.archives.fo_open_interest(self.TRADE_DATE)
        assert data is not None
        print(f"  ✓ archives.fo_open_interest() -> {type(data).__name__}")

    def test_generic_download(self, client: NSEClient):
        data = client.archives.download("commodity_market_activity", self.TRADE_DATE)
        assert data is not None
        print(f"  ✓ archives.download('commodity_market_activity') -> {type(data).__name__}")
