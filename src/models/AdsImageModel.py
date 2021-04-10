# src/models/AdsImageModel.py
from . import db
import datetime
from marshmallow import fields, Schema
from .AdvertiserModel import AdvertiserSchema

class AdsImageModel(db.Model):

    __tablename__ = 'ads_image'

    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    advertiser = db.relationship("AdvertiserModel", uselist=False, backref="ads_image")
    name = db.Column(db.String(50), nullable=False)
    # campaign_list = db.relationship(
    #     'CampaignModel',
    #     backref='ads_image',
    #     cascade='all, delete, delete-orphan',
    #     single_parent=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.name = data.get('name')
        self.advertiser_id = data.get('advertiser_id')
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
        return AdsImageModel.query.all()
  
    @staticmethod
    def get_one(id):
        return AdsImageModel.query.get(id)

    @staticmethod
    def get_by_advertiser_id(value):
        return AdsImageModel.query.filter_by(advertiser_id=value).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)

class AdsImageSchema(Schema):
    id = fields.Int(dump_only=True)
    advertiser_id = fields.Int(required=True)
    advertiser = fields.Nested(AdvertiserSchema, many=False)    
    name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)