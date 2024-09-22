import jwt
from datetime import datetime, timedelta
from flask import current_app, Response, Request, make_response
from bcrypt import gensalt, hashpw, checkpw
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


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
        expires=current_app.config.get("JWT_ACCESS_TOKEN_EXP")
    )


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
