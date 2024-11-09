from flask import Flask
from app import user, main, posts


def register_blueprints(app: Flask):
    app.register_blueprint(user.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(posts.bp)
