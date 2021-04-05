# src/models/CampaignModel.py
from . import db
import datetime
from marshmallow import fields, Schema
from .AdsImageModel import AdsImageSchema

class CampaignModel(db.Model):

    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    audience_id = db.Column(db.Integer, db.ForeignKey('audience.id'))
    name = db.Column(db.String(128), nullable=False)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    total_walker = db.Column(db.Integer)
    fee = db.Column(db.Float)
    status = db.Column(db.String(50))
    ads_image = db.relationship('AdsImageModel', backref='campaign', lazy=True)

    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.advertiser_id = data.get('advertiser_id')
        self.audience_id = data.get('audience_id')
        self.name = data.get('name')
        self.start = data.get('start')
        self.end = data.get('end')
        self.total_walker = data.get('total_walker')
        self.fee = data.get('fee')
        self.status = data.get('status')

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
        return CampaignModel.query.all()
  
    @staticmethod
    def get_one(id):
        return CampaignModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class CampaignSchema(Schema):

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    advertiser_id = fields.Str(required=True)
    audience_id = fields.Str(required=True)
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)
    total_walker = fields.Int(required=False)
    fee = fields.Float(required=False)
    status = fields.Str(required=False)
    ads_image = fields.Nested(AdsImageSchema, many=True)

    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)