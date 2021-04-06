from flask import Flask
from flask_cors import CORS
from flask_seeder import FlaskSeeder

from .config import app_config
from .models import db, bcrypt

from .shared import mail

from .views.UserView import user_api as user_blueprint
# from .views.BlogpostView import blogpost_api as blogpost_blueprint
from .views.PaymentView import payment_api as payment_blueprint

from .views.ActivityView import activity_api as activity_blueprint
from .views.AdsImageView import ads_image_api as ads_image_blueprint
from .views.AdvertiserView import advertiser_api as advertiser_blueprint
from .views.AudienceView import audience_api as audience_blueprint
from .views.BusinessCategoryView import business_category_api as business_category_blueprint
from .views.CampaignEnrollView import campaign_enroll_api as campaign_enroll_blueprint
from .views.CampaignView import campaign_api as campaign_blueprint
from .views.LedView import led_api as led_blueprint
from .views.ProfileView import profile_api as profile_blueprint
from .views.WalkerView import walker_api as walker_blueprint
from .views.ConfigView import config_api as config_blueprint
# from .views.NotificationView import species_api as species_blueprint


def create_app(env_name):
    """
    Create app
    """
    # app initiliazation
    app = Flask(__name__)
    # cors
    CORS(app, supports_credentials=True)
    # cors = CORS(app)
    # cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
    # cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})
    # cors = CORS(app, resources={r"*": {"origins": "http://localhost:8080"}})
    # CORS(app, resources={ r'/*': {'origins': 'http://localhost:8080'}}, supports_credentials=True)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    mail.init_app(app)

    db.init_app(app)

    seeder = FlaskSeeder()
    seeder.init_app(app, db)


    app.register_blueprint(user_blueprint, url_prefix='/api/auth')
    # app.register_blueprint(blogpost_blueprint, url_prefix='/api/v1/blogposts')
    app.register_blueprint(payment_blueprint, url_prefix='/api/v1/payment')

    app.register_blueprint(activity_blueprint, url_prefix='/api/activity')
    app.register_blueprint(ads_image_blueprint, url_prefix='/api/ads')
    app.register_blueprint(advertiser_blueprint, url_prefix='/api/advertiser')
    app.register_blueprint(audience_blueprint,url_prefix='/api/audience')
    app.register_blueprint(business_category_blueprint, url_prefix='/api/business')
    app.register_blueprint(campaign_enroll_blueprint, url_prefix='/api/campaign_enroll')
    app.register_blueprint(campaign_blueprint, url_prefix='/api/campaign')
    app.register_blueprint(led_blueprint, url_prefix='/api/led')
    app.register_blueprint(profile_blueprint, url_prefix='/api/profile')
    app.register_blueprint(walker_blueprint, url_prefix='/api/walker')
    app.register_blueprint(config_blueprint, url_prefix='/api/config')

    @app.route('/')
    def index():
        return 'TUNTUNG API'


    return app
