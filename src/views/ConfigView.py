# /src/views/ActivityView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.ActivityModel import ActivityModel
from ..models.LocationModel import LocationModel
from ..models.NotificationModel import NotificationModel
from ..models.OrganizationModel import OrganizationModel
from ..models.ProductModel import ProductModel
from ..models.ProfileModel import ProfileModel
from ..models.RoleModel import RoleModel
from ..models.SpeciesModel import SpeciesModel
from ..models.TrackHistoryModel import TrackHistoryModel
from ..models.UserModel import UserModel

app = Flask(__name__)
config_api = Blueprint('config_api', __name__)
# activity_schema = ActivitySchema()


@config_api.route('/', methods=['GET'])
def index():
    return custom_response('config', 200)


@config_api.route('/seed', methods=['GET'])
def seed():
    ActivityModel.query.delete()
    ActivityModel({'code': '1', 'name': 'Send to ceramic tank'}).save()
    ActivityModel({'code': '2', 'name': 'Receive at ceramic tank'}).save()
    ActivityModel({'code': '3', 'name': 'Complete moisture process'}).save()
    ActivityModel({'code': '4', 'name': 'Send to retail shop'}).save()
    ActivityModel({'code': '5', 'name': 'Receive at retail shop'}).save()
    ActivityModel({'code': '6', 'name': 'Sold to customer'}).save()

    LocationModel({'code': 'CER', 'name': 'Ceramik Tank, Terengganu',
                   'location_type': 'Ceramic Tank', 'organization_code': '1'}).save()
    LocationModel({'code': 'SHP', 'name': 'Retail Shop, Terengganu',
                   'location_type': 'Retail Shop', 'organization_code': '1'}).save()
    LocationModel({'code': 'END', 'name': 'End User Customer',
                   'location_type': 'End User', 'organization_code': '1'}).save()

    NotificationModel({'title': 'Product arrive at ceramic tank',
                       'information': 'Product id = 1'}).save()
    NotificationModel({'title': 'Product arrive at ceramic tank',
                       'information': 'Product id = 2'}).save()
    NotificationModel({'title': 'Product arrive at ceramic tank',
                       'information': 'Product id = 3'}).save()

    OrganizationModel({'code': '1', 'name': 'Persatuan Penternak Kelulut Selangor',
                       'address': 'Selangor, Malaysia'}).save()
    OrganizationModel({'code': '2', 'name': 'Persatuan Penternak Kelulut Negeri Sembilan',
                       'address': 'Negeri Sembilan, Malaysia'}).save()
    OrganizationModel({'code': '3', 'name': 'Persatuan Penternak Kelulut Terengganu',
                       'address': 'Terengganu, Malaysia'}).save()

    ProductModel({
        'code': 'AAA',
        'name': 'Product AAA',
        'species_code': '1'
    }).save()
    ProductModel({
        'code': 'AAB',
        'name': 'Product AAB',
        'species_code': '1'
    }).save()
    ProfileModel({
        'code': 'fakhrulazran@gmail.com',
        'name': 'Fakhrul Azran',
        'email': 'fakhrulazran@gmail.com',
        'password': 'abc123',
        'role_code': 'ADM',
        'organization_code': '1',
    }).save()
    ProfileModel({
        'code': 'ainnur@gmail.com',
        'name': 'Ainnur',
        'email': 'ainnur@gmail.com',
        'password': 'abc123',
        'role_code': 'UPD',
        'organization_code': '1',
    }).save()
    ProfileModel({
        'code': 'ain@gmail.com',
        'name': 'Ain',
        'email': 'ain@gmail.com',
        'password': 'abc123',
        'role_code': 'UPD',
        'organization_code': '1',
    }).save()

    RoleModel({
        'code': 'ADM',
        'name': 'Administrator'
    }).save()
    RoleModel({
        'code': 'UPD',
        'name': 'Updater'
    }).save()

    SpeciesModel({
        'code': '1',
        'name': 'Species A',
        'description': 'Species A Description'
    }).save()
    SpeciesModel({
        'code': '2',
        'name': 'Species B',
        'description': 'Species B Description'
    }).save()

    TrackHistoryModel({
        'info': 'info',
        'remarks': 'info',
        'product_code': 'AAA',
        'activity_code': '1',
        'profile_code': 'ain@gmail.com',
        'location_code': 'SHP',
        'gps': '123,123'
    }).save()
    TrackHistoryModel({
        'info': 'info',
        'remarks': 'info',
        'product_code': 'AAA',
        'activity_code': '1',
        'profile_code': 'fakhrulazran@gmail.com',
        'location_code': 'END',
        'gps': '123,123'
    }).save()

    return custom_response('ok', 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
