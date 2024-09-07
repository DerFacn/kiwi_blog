from flask import Blueprint
from .routes import index

bp = Blueprint("main", __name__, url_prefix='/')

bp.add_url_rule('/', 'index', index, methods=['GET'])
