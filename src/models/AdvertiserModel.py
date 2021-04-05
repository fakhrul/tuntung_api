# src/models/AdvertiserModel.py
from . import db, 
import datetime
from marshmallow import fields, Schema
from .BusinessCategoryModel import BusinessCategorySchema

class AdvertiserModel(db.Model):

    __tablename__ = 'advertiser'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    email = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.Numeric(14, 0))
    address1 = db.Column(db.String(250))
    address2 = db.Column(db.String(250))
    address3 = db.Column(db.String(250))
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(10))

    contact_name = db.Column(db.String(250))
    contact_email = db.Column(db.String(250))
    contact_phone = db.Column(db.String(250))

    business_category = db.relationship('BusinessCategoryModel',
        secondary=assocication_advertiser_business, lazy='subquery',
        backref=db.backref('advertiser', lazy=True))
        
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.code = data.get('code')
        self.name = data.get('name')
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
        
        self.contact_name = data.get('contact_name')
        self.contact_email = data.get('contact_email')
        self.contact_phone = data.get('contact_phone')
        
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
        return AdvertiserModel.query.all()
  
    @staticmethod
    def get_one(id):
        return AdvertiserModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class AdvertiserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=False)
    name = fields.Str(required=True)
    phone = fields.Str(required=False)
    address1 = fields.Str(required=False)
    address2 = fields.Str(required=False)
    address3 = fields.Str(required=False)
    country = fields.Str(required=False)
    state = fields.Str(required=False)
    city = fields.Str(required=False)
    postcode = fields.Str(required=False)

    contact_name = fields.Str(required=False)
    contact_email = fields.Str(required=False)
    contact_phone = fields.Str(required=False)

    business_category = fields.Nested(BusinessCategorySchema, many=True)
    
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)