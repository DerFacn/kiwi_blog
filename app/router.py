from flask import Blueprint
from . import main, user

router = Blueprint('root', __name__)

router.register_blueprint(main.bp)
router.register_blueprint(user.bp)
