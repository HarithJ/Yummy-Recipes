class Config(object):
    """
    Common Configurations
    """

class DevelopmentConfig(Config):
    """
    Developement configurations
    """
    DEBUG=True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}