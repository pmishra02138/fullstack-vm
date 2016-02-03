import os
basedir = os.path.abspath(os.path.dirname(__file__))
import json

class Config:
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Enable protection agains CSRF
    CSRF_ENABLED = True
    APPLICATION_NAME = "Movie Catalog Application"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    # Credentials for Google Signin
    CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'moviecatalogwithusers.db')


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
