import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.dirname(__file__)  # this gives us full path to the app folder
# instance path for database file (if it's file)
instance = os.path.abspath(os.path.join(basedir, '..', 'instance'))
static_folder = os.path.join(basedir, 'static')
previews_storage = os.path.join(static_folder, 'storage', 'previews')

folders = [instance, previews_storage]

for folder in folders:
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except OSError as e:
            print(f"Error creating instance folder: {e}")


class Config:
    STATIC_FOLDER = static_folder
    PREVIEWS_STORAGE = os.environ.get('PREVIEWS_STORAGE') or previews_storage

    ALCHEMICAL_DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(instance, 'app.db')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CHANGE_THIS_IN_PRODUCTION'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'CHANGE_THIS_IN_PRODUCTION'

    JWT_ACCESS_TOKEN_NAME = os.environ.get('JWT_ACCESS_TOKEN_NAME') or 'access_token'
    JWT_ACCESS_TOKEN_TIMEDELTA = os.environ.get('JWT_ACCESS_TOKEN_TIMEDELTA') or 2_592_000

    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION') or ['cookies', 'headers']
