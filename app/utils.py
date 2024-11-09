import os
import jwt
from app import db
from app.models import User
from datetime import datetime, timedelta
from flask import current_app, request, Response, Request, abort
from bcrypt import gensalt, hashpw, checkpw
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from functools import wraps


# DB funcs
def get_all(query): return db.session.scalars(query)


def get_first_or_false(query):
    result = db.session.scalar(query)
    return result if result else False


# Password hashing
def generate_hash(password: str) -> str:
    salt = gensalt()
    password_bytes = password.encode('utf-8')
    password_hash = hashpw(password_bytes, salt)
    return password_hash.decode('utf-8')


def check_hash(password: str, password_hash: str) -> bool:
    password_bytes = password.encode('utf-8')
    return checkpw(password_bytes, password_hash.encode('utf-8'))


# JWT funcs
def create_access_token(identity: str) -> str:
    exp = datetime.now() + timedelta(
        seconds=current_app.config.get("JWT_ACCESS_TOKEN_TIMEDELTA")
    )

    payload = {
        "identity": identity,
        "exp": exp
    }

    return jwt.encode(payload, current_app.config.get("JWT_SECRET_KEY"))


def set_access_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key='access_token',
        value=token,
        expires=datetime.now() + timedelta(
            seconds=current_app.config.get("JWT_ACCESS_TOKEN_TIMEDELTA")
        )
    )


def unset_cookies(response: Response) -> None:
    response.set_cookie('access_token', value='', expires=0)


def decode_token(token) -> dict | None:
    try:
        payload = jwt.decode(
            token, current_app.config.get('JWT_SECRET_KEY'), algorithms=['HS256']
        )
        return payload
    except ExpiredSignatureError:
        return
    except InvalidTokenError:
        return


def get_token(request: Request) -> str | None:
    locations = current_app.config.get('JWT_TOKEN_LOCATION')

    for location in locations:
        token = None
        match location:
            case "headers":
                try:
                    token = request.authorization.token
                except AttributeError:
                    pass
            case "cookies":
                token = request.cookies.get("access_token")
            case _:
                raise Exception(f'{location} is no valid token key.')
        if token:
            return token


def get_user():
    try:
        token = get_token(request)
        payload = decode_token(token)
        uuid = payload.get('identity')
    except AttributeError:
        return

    user = get_first_or_false(User.select().filter_by(uuid=uuid))

    return user


def jwt_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = get_token(request)

        if not token or not decode_token(token):
            return abort(401)  # TODO: errors handlers

        return func(*args, **kwargs)
    return decorator


# Other funcs
def get_preview(filename):
    return os.path.relpath(
        os.path.join(
            current_app.config.get('PREVIEWS_STORAGE'),
            filename
        ),
        start=current_app.config.get('STATIC_FOLDER')
    ).replace('\\', '/')
