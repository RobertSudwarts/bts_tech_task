
import logging
from flask import Flask, render_template
from flask.ext import menu

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

menu.Menu(app=app)


@app.route('/')
def home():
    """Main page"""
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    """render customised 'page not found' template"""
    return render_template('404.html'), 404


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

# import and register blueprints
# Note that these imports must take place AFTER `app` has been defined
from pricing_app.mod_index_pricing.controllers import mod as idx_px_module
from pricing_app.mod_stubs.controllers import mod as stubs

app.register_blueprint(idx_px_module)
app.register_blueprint(stubs)


#  add file handler with customised format
lgfmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
fmt = logging.Formatter(lgfmt)
file_handler = logging.FileHandler('applog.log')
file_handler.setFormatter(fmt)

app.logger.addHandler(file_handler)

# Set logging level
if app.debug:
    app.logger.setLevel(logging.DEBUG)
else:
    pass
