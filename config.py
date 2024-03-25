import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'testsecretkey')
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cc_tweaked_turtle_swarm')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False