from flask import Flask, g
from .config import Config
from alchemical.flask import Alchemical
from flask_migrate import Migrate

db = Alchemical()
migrate = Migrate()


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .router import router
    app.register_blueprint(router)

    from .utils import get_user

    @app.before_request
    def before_request():
        user = get_user()
        g.user = user

    return app
