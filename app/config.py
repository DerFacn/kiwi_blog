import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))  # this gives us full path to the app folder


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CHANGE_THIS_IN_PRODUCTION'
