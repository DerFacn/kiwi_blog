from app import db
from flask import request, render_template, flash, make_response, url_for, redirect
from app.utils import (get_first_or_false, generate_hash, create_access_token, set_access_cookie, unset_cookies,
                       check_hash)
from app.models import User
from sqlalchemy.exc import IntegrityError


def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password is required.')
            return render_template('auth/signup.html')

        user = get_first_or_false(User.select().filter_by(username=username))

        if user:
            flash('User already exists.')
            return render_template('auth/signup.html')

        new_user = User(
            username=username,
            password=generate_hash(password)
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:  # TODO: Logging
            flash('Something went wrong. Please try again, and if the error occurs again, contact an administrator.')
            return render_template('auth/signup.html')

        identity = new_user.uuid
        access_token = create_access_token(identity)
        response = make_response(redirect(url_for('root.main.index')))
        set_access_cookie(response, access_token)

        return response

    return render_template('auth/signup.html')


def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password is required.')
            return render_template('auth/login.html')

        user = get_first_or_false(User.select().filter_by(username=username))

        if not user:
            flash('User not founded.')
            return render_template('auth/login.html')
        elif not check_hash(password, user.password):
            flash('Wrong password.')
            return render_template('auth/login.html')

        identity = user.uuid
        token = create_access_token(identity)
        response = make_response(redirect(url_for('root.main.index')))
        set_access_cookie(response, token)

        return response

    return render_template('auth/login.html')


def logout():
    response = make_response(redirect(url_for('root.main.index')))
    unset_cookies(response)
    return response
