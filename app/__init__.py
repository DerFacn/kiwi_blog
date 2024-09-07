from flask import Flask
from .config import Config


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    from .router import router
    app.register_blueprint(router)

    return app
