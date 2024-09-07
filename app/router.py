from flask import Blueprint
from . import main

router = Blueprint('root', __name__)

router.register_blueprint(main.bp)
