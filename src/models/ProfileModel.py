# src/models/ProfileModel.py
from . import db, association_profile_advertiser
import datetime
from marshmallow import fields, Schema
# from .AdvertiserModel import AdvertiserSchema

class ProfileModel(db.Model):

    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # user = db.relationship("UserModel", uselist=False, backref="profile")
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128))
    phone = db.Column(db.String(50))
    address1 = db.Column(db.String(250))
    address2 = db.Column(db.String(250))
    address3 = db.Column(db.String(250))
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(10))

    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.email = data.get('email')
        self.role = data.get('role')
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

    @staticmethod
    def get_profile_by_email(value):
        return ProfileModel.query.filter_by(email=value).first()

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    role = fields.Str(required=True)
    email = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    address1 = fields.Str(allow_none=True)
    address2 = fields.Str(allow_none=True)
    address3 = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)
    state = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    postcode = fields.Str(allow_none=True)

    # advertiser = fields.Nested(AdvertiserSchema, many=True)
    
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)