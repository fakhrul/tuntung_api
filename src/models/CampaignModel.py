# src/models/CampaignModel.py
from . import db
import datetime
from marshmallow import fields, Schema, EXCLUDE
from .AdsImageModel import AdsImageSchema
from .CampaignScheduleModel import CampaignScheduleSchema
from .AudienceModel import AudienceSchema
from .AdvertiserModel import AdvertiserSchema

class CampaignModel(db.Model):

    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    advertiser = db.relationship("AdvertiserModel", uselist=False, backref="campaign")
    audience_id = db.Column(db.Integer, db.ForeignKey('audience.id'))
    audience = db.relationship("AudienceModel", uselist=False, backref="campaign")
    name = db.Column(db.String(128), nullable=False)
    # start = db.Column(db.DateTime)
    # end = db.Column(db.DateTime)
    total_walker = db.Column(db.Integer)
    # fee = db.Column(db.Float)
    status = db.Column(db.String(50))
    campaign_schedule_list = db.relationship(
        'CampaignScheduleModel',
        backref='campaign',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(CampaignScheduleModel.start_at)')
        # lazy=True)
    # ads_image = db.relationship('AdsImageModel', backref='campaign', lazy=True)
    ads_image_list = db.relationship(
        'AdsImageModel',
        backref='campaign',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(AdsImageModel.created_at)')

    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.advertiser_id = data.get('advertiser_id')
        self.audience_id = data.get('audience_id')
        self.name = data.get('name')
        # self.advertiser = data.get('advertiser')
        # self.start = data.get('start')
        # self.end = data.get('end')
        self.total_walker = data.get('total_walker')
        # self.fee = data.get('fee')
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
    advertiser_id = fields.Int(required=True)
    audience_id = fields.Int(required=True)
    # start = fields.DateTime(required=True)
    # end = fields.DateTime(required=True)
    total_walker = fields.Int(allow_none=True)
    # fee = fields.Float(required=False)
    status = fields.Str(allow_none=True)
    # advertiser = fields.Nested(AdvertiserSchema, many=False,  default=None, only=('id', 'name'))
    # audience = fields.Nested(AudienceSchema, many=False, default=None, only=('id', 'name'))
    # campaign_schedule_list = fields.Nested(CampaignScheduleSchema, many=True, default=None)
    # advertiser = fields.Nested(AdvertiserSchema, exclude=('advertiser.id',))
    advertiser = fields.Nested(AdvertiserSchema, many=False,)
    audience = fields.Nested(AudienceSchema)
    campaign_schedule_list = fields.Nested(CampaignScheduleSchema, many=True, default=None)
    ads_image_list = fields.Nested(AdsImageSchema, many=True, default=None)

    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)