from flask.ext.testing import TestCase
from nose.tools import *
from pricing_app import app


class TestRoutes(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_subscribe(self):
        self.assert404(self.client.get("/stub/subscribe"))

    def test_support(self):
        self.assert404(self.client.get("/stub/support"))

    def test_mkt_data(self):
        self.assert404(self.client.get("/stub/market_data"))

    def test_news(self):
        self.assert404(self.client.get("/stub/news"))

    def test_features(self):
        self.assert404(self.client.get("/stub/features"))
