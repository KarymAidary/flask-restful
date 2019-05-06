import requests
from flask import request, jsonify
from app import db, parser, app
from models import Page, Tag, PageSchema


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
