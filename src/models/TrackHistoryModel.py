# src/models/TrackHistoryModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class TrackHistoryModel(db.Model):

    __tablename__ = 'trackhistory'

    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(128), nullable=False)
    remarks = db.Column(db.String(128), nullable=True)
    product_code = db.Column(db.String(128), nullable=False)
    activity_code = db.Column(db.String(128), nullable=False)
    profile_code = db.Column(db.String(128), nullable=False)
    location_code = db.Column(db.String(128), nullable=False)
    gps = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.info = data.get('info')
        self.remarks = data.get('remarks')
        self.product_code = data.get('product_code')
        self.activity_code = data.get('activity_code')
        self.profile_code = data.get('profile_code')
        self.location_code = data.get('location_code')
        self.gps = data.get('gps')
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
        return TrackHistoryModel.query.all()
  
    @staticmethod
    def get_one(id):
        return TrackHistoryModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class TrackHistorySchema(Schema):
    id = fields.Int(dump_only=True)
    info = fields.Str(required=True)
    remarks = fields.Str(required=False)
    product_code = fields.Str(required=True)
    activity_code = fields.Str(required=True)
    profile_code = fields.Str(required=True)
    location_code = fields.Str(required=True)
    gps = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)