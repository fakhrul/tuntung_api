#/src/views/ProfileView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.ProfileModel import ProfileModel, ProfileSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
profile_api = Blueprint('profile_api', __name__)
profile_schema = ProfileSchema()


@profile_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Profiles
    """
    posts = ProfileModel.get_all()
    data = profile_schema.dump(posts, many=True)
    return custom_response(data, 200)

@profile_api.route('/<int:profile_id>', methods=['GET'])
def get_one(profile_id):
    """
    Get A Profile
    """
    post = ProfileModel.get_one(profile_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = profile_schema.dump(post)
    return custom_response(data, 200)
    
@profile_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Profile Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = profile_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = ProfileModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = profile_schema.dump(post)
    return custom_response(data, 201)    

@profile_api.route('/<int:profile_id>', methods=['PUT'])
@Auth.auth_required
def update(profile_id):
    """
    Update A Profile
    """
    req_data = request.get_json()
    post = ProfileModel.get_one(profile_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = profile_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = profile_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = profile_schema.dump(post)
    return custom_response(data, 200)

@profile_api.route('/<int:profile_id>', methods=['DELETE'])
@Auth.auth_required
def delete(profile_id):
    """
    Delete A Profile
    """
    post = ProfileModel.get_one(profile_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = profile_schema.dump(post)
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