from flask import Flask, g
from .config import Config
from alchemical.flask import Alchemical
from flask_migrate import Migrate

db = Alchemical()
migrate = Migrate()


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Jinja environment
    from .utils import get_preview

    app.jinja_env.globals['get_preview'] = get_preview

    # Initialisation
    db.init_app(app)
    migrate.init_app(app, db)

    # Models (for database)
    from . import models

    # Registering all routes
    from .router import router
    app.register_blueprint(router)

    # Registering all error handlers
    from .errors import register_error_handlers
    register_error_handlers(app)

    # User lookup
    from .utils import get_user

    @app.before_request
    def before_request():
        user = get_user()
        g.user = user

    return app
