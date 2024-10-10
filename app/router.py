from flask import Blueprint
from . import main, user, posts

router = Blueprint('root', __name__)

blueprints = [main, user, posts]

for blueprint in blueprints:
    router.register_blueprint(blueprint.bp)
