from flask.ext.testing import TestCase
from nose.tools import *
from pricing_app import app


class TestRoutes(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_index_data(self):
        resp = self.client.get("/idx/px/cac")
        assert_in('data', resp.json)
