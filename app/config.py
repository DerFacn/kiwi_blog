import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))  # this gives us full path to the app folder
# instance path for database file (if it's file)
instance = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))

if not os.path.exists(instance):
    try:
        os.makedirs(instance)
    except OSError as e:
        print(f"Error creating instance folder: {e}")


class Config:
    ALCHEMICAL_DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(instance, 'app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CHANGE_THIS_IN_PRODUCTION'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'CHANGE_THIS_IN_PRODUCTION'

    JWT_ACCESS_TOKEN_NAME = os.environ.get('JWT_ACCESS_TOKEN_NAME') or 'access_token'
    JWT_ACCESS_TOKEN_TIMEDELTA = os.environ.get('JWT_ACCESS_TOKEN_TIMEDELTA') or 2_592_000

    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION') or ['cookies', 'headers']
