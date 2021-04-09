# src/models/AudienceModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class AudienceModel(db.Model):

    __tablename__ = 'audience'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    latitude = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.name = data.get('name')
        self.location = data.get('location')
        self.latitude = data.get('latitude')
        self.longitude = data.get('longitude')

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
        return AudienceModel.query.all()
  
    @staticmethod
    def get_one(id):
        return AudienceModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class AudienceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    latitude = fields.Str(allow_none=True)
    longitude = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)