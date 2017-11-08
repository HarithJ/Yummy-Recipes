class Config(object):
    """
    Common Configurations
    """

    """These are global variables that keep track of:
        1. registered users
        2. the user which is currently logged in
        3. The category which a user is at currently
    """
    users = {}
    current_user = None
    current_category = None

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