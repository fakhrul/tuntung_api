# src/models/AdsImageModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class AdsImageModel(db.Model):

    __tablename__ = 'ads_image'

    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    name = db.Column(db.String(50), nullable=False)
    img_filename = db.Column(db.String(250), nullable=False)
    img_data = db.Column(db.LargeBinary)

    def __init__(self, data):
        self.name = data.get('name')
        self.advertiser_id = data.get('advertiser_id')
        self.campaign_id = data.get('campaign_id')
        self.img_filename = data.get('img_filename')
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

    def __repr__(self):
        return '<id {}>'.format(self.id)

class AdsImageSchema(Schema):
    id = fields.Int(dump_only=True)
    advertiser_id = fields.Int(required=True)
    campaign_id = fields.Int(required=False)
    name = fields.Str(required=True)
    img_filename = fields.Str(required=True)
    # img_data = fields.LargeBinary(required=True)
    
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)