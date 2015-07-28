from flask.ext.testing import TestCase
from nose.tools import *
from pricing_app import app


class TestRoutes(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    # in production (ie for real pages) I'd use BeautifulSoup
    # for more comprehensive checks on content rather than
    # the rather simplistic `asset_in`
    def test_main_page(self):
        resp = self.client.get("/")
        self.assert200(resp)
        assert_in('pxTable', resp.data)

    # call a non-existing route to ensure that the
    # generic 404 is rendered
    def test_404(self):
        resp = self.client.get("/i/do/not/exist")
        self.assert404(resp)

    def test_robots(self):
        resp = self.client.get("/robots.txt")
        eq_(resp.mimetype, "text/plain")
