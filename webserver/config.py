#!/usr/bin/env python3
class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    APPLICATION_ROOT = '/'


class DevelopmentConfig(Config):
    DEBUG = True
    APPLICATION_ROOT = '/'
