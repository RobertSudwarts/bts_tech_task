"""
Classes relating to Indexes.

The structure layed out here would map quite easily to using a database ORM
(eg SQLAlchemy.

The inheritance model looks like overkill but in terms of structure would
afford flexibility when adding, for example, different properties, methods
and computations for index weightings etc.
"""
import os
import csv
from decimal import Decimal
from .asset import Equity

pth = os.path.dirname(__file__)

# fix prices to four places using the decimal library
DP4 = Decimal(10) ** -4


class Index(object):
    """Base class for all index types"""

    def __init__(self, name):
        self.name = name

        if not self.exists:
            raise Exception("index file does not exist")

    @property
    def exists(self):
        """Check if index file exists"""
        f = os.path.join(pth, '..', 'static/data', self.filename)
        return os.path.isfile(f)

    @property
    def filename(self):
        return "%s_idx.csv" % self.name.lower()

    @property
    def component_tickers(self):
        """return a list of UMTS contained in the index file"""

        f = os.path.join(pth, '..', 'static/data', self.filename)
        with open(f, 'rb') as fh:
            tickers = [rw.rstrip() for rw in fh.readlines()]

        return tickers

    def trade_file(self, timestamp):
        """
        parameters
        -----------
        timestamp is simply hour and minute "HHMM"
        """
        return "%s_trades_%s.csv" % (self.name.lower(), timestamp)

    def components_last_px(self, timestamp):
        """
        The key here is that we want to read:
          a. the last/final price in the file
          b. we don't want to hold the others in memory
        """
        # we're including the timestamp so that if the price hasn't
        # been found in this run it'll poke through from the previous.

        # we start by using a dict generator over `component_tickers`
        # to build a set of key value pairs where the value is initially
        # set to None.
        # When parsing the text file, the data is pushed into the hash,
        # (and overwritten each time) to leave the final value as the
        # lattermost row in the text file.
        data = {ticker: None for ticker in self.component_tickers}

        f = os.path.join(pth, '..', 'static/data', self.trade_file(timestamp))
        with open(f, 'rb') as fh:
            reader = csv.reader(fh, delimiter=",")
            for row in reader:
                data[row[0]] = {
                    'px': str(Decimal(row[1]).quantize(DP4)),
                    'ccy': row[2],
                    'ts': timestamp
                    }

        return data

    def __repr__(self):
        return "<%s(name='%s')>" % (self.__class__.__name__, self.name)


class EquityIndex(Index):

    def __init__(self, name):
        super(EquityIndex, self).__init__(name)

    def components(self):
        """
        notice that the Equity is constructed by passing `self`
        this is a reasonable proxy for the relationship which could be
        made inherent when using a database.
        """
        return [Equity(t, self) for t in self.component_tickers]


# class OtherIndexType(Index):
#   .....
