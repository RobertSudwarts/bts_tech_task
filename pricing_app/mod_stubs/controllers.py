
from flask import Blueprint, abort
from flask.ext import menu

# from pricing_app import app

mod = Blueprint('stubs', __name__, url_prefix='/stub')


@mod.route('/subscribe')
@menu.register_menu(mod, '.subscribe', 'subscribe', order=0)
def subscribe():
    abort(404)


@mod.route('/support')
@menu.register_menu(mod, '.support', 'support', order=1)
def support():
    abort(404)


@mod.route('/market_data')
@menu.register_menu(mod, '.market_data', 'market data', order=2)
def mktdata():
    abort(404)


@mod.route('/news')
@menu.register_menu(mod, '.news', 'news', order=3)
def news():
    abort(404)


@mod.route('/features')
@menu.register_menu(mod, '.features', 'features', order=4)
def features():
    abort(404)
