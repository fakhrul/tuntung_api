#src/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

assocication_advertiser_business = db.Table('assocication_advertiser_business',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertiser.id')),
    db.Column('business_category_id', db.Integer, db.ForeignKey('business_category.id'))
)