from flask import Flask
from config import app_config

def create_app(config_name):
    app = Flask(__name__, static_folder='../designs/UI', template_folder='../designs/UI', instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .categories import categories as categories_blueprint
    app.register_blueprint(categories_blueprint)

    from .recipes import recipes as recipes_blueprint
    app.register_blueprint(recipes_blueprint)

    return app