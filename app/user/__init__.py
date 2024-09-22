from flask import Blueprint
from . import auth

bp = Blueprint('user', __name__, url_prefix='/user')

bp.register_blueprint(auth.bp)
