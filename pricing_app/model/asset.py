"""
Classes relating to Asset types.

The structure layed out here would map quite easily to using a database ORM
(eg SQLAlchemy.

As with the objects in `index.py` the inheritance model looks like overkill
but use of objects here again, makes it easy to add modular functionality...
"""
import os
import csv

pth = os.path.dirname(__file__)


class Asset(object):
    """Base asset object"""
    def __init__(self, ticker):
        self.ticker = ticker

    def __repr__(self):
        return "<%s(ticker='%s')>" % (self.__class__.__name__, self.ticker)


class Equity(Asset):

    def __init__(self, ticker, parent_index=None):
        super(Equity, self).__init__(ticker)

        self.parent_index = parent_index

    # commented out until the following are required.

    # def file_prices(self, timestamp):
    #     """parse price data from the trades file into a list"""

    #     trades_file = self.parent_index.trade_file(timestamp)

    #     f = os.path.join(pth, '..', 'static/data', trades_file)
    #     with open(f, 'rb') as fh:
    #         reader = csv.reader(fh, delimiter=",")
    #         data = [row for row in reader if row[0] == self.ticker]

    #     return data

    # def file_last_price(self, timestamp):

    #     return self.file_prices(timestamp)[-1]
