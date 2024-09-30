from flask import Blueprint
from .routes import index, you

bp = Blueprint("main", __name__, url_prefix='/')

bp.add_url_rule('/', 'index', index, methods=['GET'])
bp.add_url_rule('/you', 'you', you, methods=['GET'])
