# src/models/LocationModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class LocationModel(db.Model):

    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    location_type = db.Column(db.String(128), nullable=False)
    organization_code = db.Column(db.String(128), nullable=False)
    # title = db.Column(db.String(128), nullable=False)
    # contents = db.Column(db.Text, nullable=False)
    # owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.code = data.get('code')
        self.name = data.get('name')
        self.location_type = data.get('location_type')
        self.organization_code = data.get('organization_code')
        # self.owner_id = data.get('owner_id')
        # self.title = data.get('title')
        # self.contents = data.get('contents')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    @staticmethod
    def get_all():
        return LocationModel.query.all()
  
    @staticmethod
    def get_one(id):
        return LocationModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class LocationSchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    location_type = fields.Str(required=True)
    organization_code = fields.Str(required=True)
    # title = fields.Str(required=True)
    # contents = fields.Str(required=True)
    # owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)