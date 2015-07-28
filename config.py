import os


class Config(object):
    # Statement for enabling the development environment
    DEBUG = False

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True

    # Define the application directory
    # BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Secret key for signing cookies
    SECRET_KEY = "secret"


class ProductionConfig(Config):
    SECRET_KEY = "this one really needs to be kept a secret"


class TestingConfig(Config):
    TESTING = True
    CSRF_ENABLED = False
