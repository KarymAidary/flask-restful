from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from parser import TegHTMLParser

app = Flask(__name__)

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

ma = Marshmallow(app)

parser = TegHTMLParser()

from views import *

if __name__ == '__main__':
    app.run()
