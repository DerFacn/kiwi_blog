from flask import Blueprint
from .routes import fetch_tags, view_post, create_post, edit_post, delete_post

bp = Blueprint('posts', __name__, url_prefix='/posts')

bp.add_url_rule('/tags', 'fetch_tags', fetch_tags, methods=['GET'])
bp.add_url_rule('/<int:post_id>', 'view_post', view_post, methods=['GET'])
bp.add_url_rule('/create', 'create', create_post, methods=['GET', 'POST'])
bp.add_url_rule('/edit/<int:post_id>', 'edit', edit_post, methods=['GET', 'POST'])
bp.add_url_rule('/delete/<int:post_id>', 'delete', delete_post, methods=['GET'])
