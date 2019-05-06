from app import db, ma
from marshmallow import fields


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(125))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    page = db.relationship('Page', backref='tags')
    name = db.Column(db.String(10))
    count = db.Column(db.Integer)


class PageSchema(ma.ModelSchema):
    tags = fields.Nested('TagSchema', many=True, only=('count', 'name'))

    class Meta:
        model = Page


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
