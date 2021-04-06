# src/models/WalkerModel.py
from . import db
import datetime
from marshmallow import fields, Schema
from .LedModel import LedSchema

class WalkerModel(db.Model):

    __tablename__ = 'walker'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    led_list = db.relationship('LedModel', backref='walker', lazy=True)
    activity_list = db.relationship('ActivityModel', backref='walker', lazy=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.profile_id = data.get('profile_id')
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
        return WalkerModel.query.all()
  
    @staticmethod
    def get_one(id):
        return WalkerModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class WalkerSchema(Schema):
    id = fields.Int(dump_only=True)
    profile_id = fields.Int(required=True)
    led_list = fields.Nested(LedSchema, many=True)
    activity_list = fields.Nested(LedSchema, many=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)