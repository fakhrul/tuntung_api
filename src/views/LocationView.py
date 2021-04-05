#/src/views/LocationView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.LocationModel import LocationModel, LocationSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
location_api = Blueprint('location_api', __name__)
location_schema = LocationSchema()


@location_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Locations
    """
    posts = LocationModel.get_all()
    data = location_schema.dump(posts, many=True)
    return custom_response(data, 200)

@location_api.route('/<int:location_id>', methods=['GET'])
def get_one(location_id):
    """
    Get A Location
    """
    post = LocationModel.get_one(location_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = location_schema.dump(post)
    return custom_response(data, 200)
    
@location_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Location Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = location_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = LocationModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = location_schema.dump(post)
    return custom_response(data, 201)    

@location_api.route('/<int:location_id>', methods=['PUT'])
@Auth.auth_required
def update(location_id):
    """
    Update A Location
    """
    req_data = request.get_json()
    post = LocationModel.get_one(location_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = location_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = location_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = location_schema.dump(post)
    return custom_response(data, 200)

@location_api.route('/<int:location_id>', methods=['DELETE'])
@Auth.auth_required
def delete(location_id):
    """
    Delete A Location
    """
    post = LocationModel.get_one(location_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = location_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )