# /src/config.py

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = False
    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    # MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    IMAGE_FOLDER = os.getenv('IMAGE_FOLDER')

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = False
    ETHEREUM_ENDPOINT_URI = os.getenv('ETHEREUM_ENDPOINT_URI')
    IMAGE_FOLDER = os.getenv('IMAGE_FOLDER')

app_config = {
    'development': Development,
    'production': Production,
}