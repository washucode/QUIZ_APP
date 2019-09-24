import os

class Config:
    '''
    General configuration options
    '''
    pass

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