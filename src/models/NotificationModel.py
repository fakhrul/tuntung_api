# src/models/NotificationModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class NotificationModel(db.Model):

    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    information = db.Column(db.Text, nullable=False)
    # owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.title = data.get('title')
        self.information = data.get('information')
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
        return NotificationModel.query.all()
  
    @staticmethod
    def get_one(id):
        return NotificationModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    information = fields.Str(required=True)
    # title = fields.Str(required=True)
    # contents = fields.Str(required=True)
    # owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)