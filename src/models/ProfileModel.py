# src/models/ProfileModel.py
from . import db, association_profile_advertiser
import datetime
from marshmallow import fields, Schema
from .AdvertiserModel import AdvertiserSchema

class ProfileModel(db.Model):

    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("UserModel", back_populates="user")

    email = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(50))
    address1 = db.Column(db.String(250))
    address2 = db.Column(db.String(250))
    address3 = db.Column(db.String(250))
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(10))

    advertiser = db.relationship('AdvertiserModel',
        secondary=association_profile_advertiser, lazy='subquery',
        backref=db.backref('profile', lazy=True))

    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.email = data.get('email')
        self.name = data.get('name')
        self.phone = data.get('phone')
        self.address1 = data.get('address1')
        self.address2 = data.get('address2')
        self.address3 = data.get('address3')
        self.country = data.get('country')
        self.state = data.get('state')
        self.city = data.get('city')
        self.postcode = data.get('postcode')
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
    user_id = fields.Int(required=True)
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    address1 = fields.Str(required=False)
    address2 = fields.Str(required=False)
    address3 = fields.Str(required=False)
    country = fields.Str(required=False)
    state = fields.Str(required=False)
    city = fields.Str(required=False)
    postcode = fields.Str(required=False)

    advertiser = fields.Nested(AdvertiserSchema, many=True)
    
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)