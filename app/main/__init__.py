from flask import Blueprint
from .routes import index, secured_point

bp = Blueprint("main", __name__, url_prefix='/')

bp.add_url_rule('/', 'index', index, methods=['GET'])
bp.add_url_rule('/secure', 'secure', secured_point, methods=['GET'])
