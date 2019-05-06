import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
