from nose.tools import *
from pricing_app.model.index import EquityIndex
from pricing_app.model.asset import Equity


class TestEquity(object):

    def setup(self):
        self.obj = Equity('XXX')

    def test_repr(self):
        eq_(self.obj.__repr__(), "<Equity(ticker='XXX')>")


class TestEquityIndex(object):

    def setup(self):
        self.idx = EquityIndex('TEST')

    def test_repr(self):
        eq_(self.idx.__repr__(), "<EquityIndex(name='TEST')>")

    def test_filename(self):
        eq_(self.idx.filename, 'test_idx.csv')

    def test_trade_file(self):
        expected = 'test_trades_HHMM.csv'
        eq_(self.idx.trade_file('HHMM'), expected)

    def test_component_tickers(self):
        expected = ['AAA', 'BBB', 'CCC', 'DDD']
        assert_list_equal(self.idx.component_tickers, expected)

    # tests that the first `Equity` found in the collection/list
    # is the one expected
    def test_component_equities(self):
        equity = self.idx.components()[0]
        eq_(equity.ticker, 'AAA')

    # just tests that a dict is returned
    def test_components_last_px(self):
        last_prices = self.idx.components_last_px('HHMM')
        assert_is_instance(last_prices, dict)

    @raises(Exception)
    def test_non_exist_index(self):
        EquityIndex('NOT_THERE')
