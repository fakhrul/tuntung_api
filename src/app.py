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
from .views.LocationView import location_api as location_blueprint
from .views.NotificationView import notification_api as notification_blueprint
from .views.OrganizationView import organization_api as organization_blueprint
from .views.ProductView import product_api as product_blueprint
from .views.RoleView import role_api as role_blueprint
from .views.ProfileView import profile_api as profile_blueprint
from .views.SpeciesView import species_api as species_blueprint
from .views.TrackHistoryView import track_history_api as track_history_blueprint
from .views.ConfigView import config_api as config_blueprint


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
    app.register_blueprint(location_blueprint, url_prefix='/api/location')
    app.register_blueprint(notification_blueprint,
                           url_prefix='/api/notification')
    app.register_blueprint(organization_blueprint,
                           url_prefix='/api/organization')
    app.register_blueprint(product_blueprint, url_prefix='/api/product')
    app.register_blueprint(role_blueprint, url_prefix='/api/role')
    app.register_blueprint(profile_blueprint, url_prefix='/api/profile')
    app.register_blueprint(species_blueprint, url_prefix='/api/species')
    app.register_blueprint(track_history_blueprint, url_prefix='/api/trackhistory')
    app.register_blueprint(config_blueprint, url_prefix='/api/config')

    @app.route('/')
    def index():
        """
        example endpoint
        """
        app.logger.info('Mostrando los posts del blog')
        return 'TUNTUNG API'

    # @app.after_request
    # def after_request(response):
    #     # response.headers.add('Access-Control-Allow-Origin', '*')
    #     # response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    #     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #     response.headers.add('Access-Control-Allow-Credentials', 'true')
    #     print("123123123213213333333333333333333333333333333333333")
    #     return response

    return app
