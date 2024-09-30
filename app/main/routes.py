from flask import render_template
from app.utils import jwt_required


posts = [
    {
        "author_name": "Oleg Ivanenko",
        "author_avatar": "/static/assets/images/avatar.png",
        "author_url": "/static/assets/images/avatar.png",
        "title": "How to grow kiwi.",
        "description": "Short guide about growing kiwis at home.",
        "image_url": "/static/assets/images/kiwi.png",
        "url": "#",
        "tags": ["Kiwi", "Growing", "Fruits"]
    },
    {
        "author_name": "Kateryna Petrivna",
        "author_avatar": "/static/assets/images/avatar.png",
        "author_url": "/static/assets/images/avatar.png",
        "title": "Useful properties of kiwi.",
        "description": "Why kiwi is super-fruit?",
        "image_url": "/static/assets/images/kiwi.png",
        "url": "#",
        "tags": ["Kiwi", "Health", "Vitamins"]
    },
    {
        "author_name": "Dmitro Oleksi",
        "author_avatar": "/static/assets/images/avatar.png",
        "author_url": "/static/assets/images/avatar.png",
        "title": "How to make kiwi-jam",
        "description": "Recipe of kiwi jam.",
        "image_url": "/static/assets/images/kiwi.png",
        "url": "/posts/3",
        "tags": ["Kiwi", "Recipies", "Jam"]
    },
    {
        "author_name": "Dmitro Oleksi",
        "author_avatar": "/static/assets/images/avatar.png",
        "author_url": "/static/assets/images/avatar.png",
        "title": "How to make kiwi-jam",
        "description": "Recipe of kiwi jam.",
        "image_url": "/static/assets/images/kiwi.png",
        "url": "/posts/3",
        "tags": ["Kiwi", "Recipies", "Jam"]
    }
]


def index():
    return render_template('index.html', posts=posts)


@jwt_required
def you():
    return render_template('user/you.html', title='Profile', posts=posts)
