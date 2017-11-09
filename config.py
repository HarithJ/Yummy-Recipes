class Config(object):
    """
    Common Configurations
    """
    DEBUG = True

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


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}