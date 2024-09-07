from flask import request


def index():
    return f"Hello, World! Flask application running on {request.host_url}"
