from flask import render_template
from app.utils import jwt_required, get_user, get_all
from app.models import Post


def index():
    posts = get_all(Post.select().order_by(Post.created_at.desc()))
    return render_template('index.html', posts=posts)


@jwt_required
def you():
    user = get_user()
    posts = get_all(Post.select().where(Post.author_id == user.uuid).order_by(Post.created_at.desc()))
    return render_template('user/you.html', title='Profile', posts=posts)
