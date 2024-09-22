import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))  # this gives us full path to the app folder


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CHANGE_THIS_IN_PRODUCTION'

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'CHANGE_THIS_IN_PRODUCTION'

    JWT_ACCESS_TOKEN_NAME = os.environ.get('JWT_ACCESS_TOKEN_NAME') or 'access_token'
    JWT_ACCESS_TOKEN_TIMEDELTA = os.environ.get('JWT_ACCESS_TOKEN_TIMEDELTA') or 2_592_000

    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION') or ['cookies', 'headers']
