from flask import render_template
from app.utils import jwt_required


def index():
    return render_template('index.html')


@jwt_required
def secured_point():
    return "Hello authorized user!"
