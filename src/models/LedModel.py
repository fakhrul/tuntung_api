# src/models/LedModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class LedModel(db.Model):

    __tablename__ = 'led'

    id = db.Column(db.Integer, primary_key=True)
    led_type = db.Column(db.String(50), nullable=False)
    walker_id = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=False)
    serial_number = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.led_type = data.get('led_type')
        self.walker_id = data.get('walker_id')
        self.serial_number = data.get('serial_number')
        self.manufacturer = data.get('manufacturer')
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
        return LedModel.query.all()
  
    @staticmethod
    def get_one(id):
        return LedModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class LedSchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)