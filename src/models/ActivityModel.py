# src/models/ActivityModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class ActivityModel(db.Model):

    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    walker_id = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    info = db.Column(db.String(250), nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.walker_id = data.get('walker_id')
        self.activity_type = data.get('activity_type')
        self.info = data.get('info')
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
        return ActivityModel.query.all()
  
    @staticmethod
    def get_one(id):
        return ActivityModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ActivitySchema(Schema):

    id = fields.Int(dump_only=True)
    walker_id = fields.Int(required=True)
    activity_type = fields.Str(required=True)
    info = fields.Str(required=True)
    latitude = fields.Str(required=False)
    longitude = fields.Str(required=False)

    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)