# src/models/CampaignScheduleModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class CampaignScheduleModel(db.Model):

    __tablename__ = 'campaign_schedule'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.campaign_id = data.get('campaign_id')
        self.start_at = data.get('start_at')
        self.end_at = data.get('end_at')
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
        return CampaignScheduleModel.query.all()
  
    @staticmethod
    def get_one(id):
        return CampaignScheduleModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class CampaignScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    campaign_id = fields.Int(required=True)
    start_at = fields.DateTime(required=True)
    end_at = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)