import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from parser import TegHTMLParser

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ma = Marshmallow(app)

parser = TegHTMLParser()


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(125))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    page = db.relationship('Page', backref='tags')
    name = db.Column(db.String(10))
    count = db.Column(db.Integer)


db.create_all()


class PageSchema(ma.ModelSchema):
    tags = fields.Nested('TagSchema', many=True, only=('count', 'name'))

    class Meta:
        model = Page


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag


@app.route('/tags/', methods=['POST'])
def add_page():
    if request.method == 'POST':
        try:
            url = request.json['url']
            req = requests.get(url)
        except requests.exceptions.ConnectionError:
            return jsonify({'error': 'Invalid url'})
        except TypeError:
            return jsonify({'error': 'You must use json'})
        new_page = Page(url=url)
        db.session.add(new_page)
        for key, value in parser.get_el(req):
            tag = Tag(name=key, count=value, page=new_page)
            db.session.add(tag)
        db.session.commit()
        return jsonify(new_page.id)


@app.route('/tags/', methods=['GET'])
def get_pages():
    pages = Page.query.all()
    page_schema = PageSchema(many=True)
    output = page_schema.dump(pages).data
    return jsonify({'pages': output})


@app.route('/tags/<id>/', methods=['GET'])
def get_page(id):
    tag = Page.query.get(id)
    page_schema = PageSchema()
    output = page_schema.dump(tag).data
    return jsonify({'page': output})


if __name__ == '__main__':
    app.run(debug=True)
