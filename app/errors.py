from flask import Flask, redirect, url_for


def not_authorized_401(e):
    # In case when user is not authorized - we're redirecting user to sign in page
    return redirect(url_for('user.auth.login'))


def register_error_handlers(app: Flask):
    app.register_error_handler(401, not_authorized_401)
