# src/models/CampaignEnrollModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class CampaignEnrollModel(db.Model):

    __tablename__ = 'campaign_enroll'

    id = db.Column(db.Integer, primary_key=True)
    walker_id = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    total_minutes = db.Column(db.Integer)
    wages = db.Column(db.Float)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.walker_id = data.get('walker_id')
        self.campaign_id = data.get('campaign_id')
        self.total_minutes = data.get('total_minutes')
        self.wages = data.get('wages')
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
        return CampaignEnrollModel.query.all()
  
    @staticmethod
    def get_one(id):
        return CampaignEnrollModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class CampaignEnrollSchema(Schema):

    id = fields.Int(dump_only=True)
    walker_id = fields.Str(required=True)
    campaign_id = fields.Str(required=True)
    total_minutes = fields.Str(required=False)
    wages = fields.Str(required=False)
    status = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)