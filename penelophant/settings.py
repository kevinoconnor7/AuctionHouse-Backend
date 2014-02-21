""" Penelophant Settings """

from os import environ as CONFIG

DEBUG = bool(int(CONFIG['DEBUG']))
ASSETS_DEBUG = bool(int(CONFIG.get('ASSETS_DEBUG', DEBUG)))
SQLALCHEMY_DATABASE_URI = CONFIG['DATABASE_URL']
SECRET_KEY = CONFIG['SECRET_KEY']

del CONFIG