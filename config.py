import os

class Config:
    '''
    General configuration options
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class ProdConfig(Config):
    '''
    Production configurations
    '''
    pass

class DevConfig(Config):
    '''
    Development configurations
    '''
    Debug=True

config_options = {
    'development':DevConfig,
    'production':ProdConfig
}