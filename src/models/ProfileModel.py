# src/models/ProfileModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class ProfileModel(db.Model):

    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_code = db.Column(db.String(128), nullable=False)
    organization_code = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.code = data.get('code')
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.role_code = data.get('role_code')
        self.organization_code = data.get('organization_code')
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
        return ProfileModel.query.all()
  
    @staticmethod
    def get_one(id):
        return ProfileModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role_code = fields.Str(required=True)
    organization_code = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)