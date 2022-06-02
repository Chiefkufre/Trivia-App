import os

from dotenv import load_dotenv




SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



# Enable debug mode.
DEBUG = True

# Connect to the database


DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

SQLALCHEMY_TRACK_MODIFICATIONS = False

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')