import os

class Config:
    '''
    General configuration options
    '''
    SECRET_KEY =os.environ.get('SECRET_KEY')

class ProdConfig(Config):
    '''
    Production configurations
    '''
    pass

class DevConfig(Config):
    '''
    Development configurations
    '''

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    DEBUG=True

config_options = {
    'development':DevConfig,
    'production':ProdConfig
}
