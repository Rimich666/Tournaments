from os import getenv

from flask import url_for

SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", "postgresql://user:password@localhost:5454/tournament")
#SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", "postgresql://user:password@localhost:5432/app")


class Config:
    DEBUG = False
    TESTING = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

    SECRET_KEY = getenv('SECRET_KEY', 'das-ist-fantastish-privater-Schlüssel')
    PHONE = '79272117466'
    API_ID = 'ADBBA8A6-5136-9B60-F45A-AD869ACD9BE8'
    DEF_USER = 'admin'
    DEF_PASSWORD = '1'
    SMS_TIMEOUT = 300
    MAIN_PAGE = 'start_app.start'


class ProductionConfig(Config):
    """"""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
#"!/usr/bin/env bash"
