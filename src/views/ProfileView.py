#/src/views/ProfileView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.ProfileModel import ProfileModel, ProfileSchema
from ..models.UserModel import UserModel, UserSchema

app = Flask(__name__)
profile_api = Blueprint('profile_api', __name__)
profile_schema = ProfileSchema(unknown=EXCLUDE)
user_schema = UserSchema(unknown=EXCLUDE)

@profile_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Profiles
    """
    posts = ProfileModel.get_all()
    data = profile_schema.dump(posts, many=True)

    ret_data = {
        'data': data,
        'status': 'success'
    }

    return custom_response(ret_data, 200)

@profile_api.route('/<int:profile_id>', methods=['GET'])
def get_one(profile_id):
    """
    Get A Profile
    """
    post = ProfileModel.get_one(profile_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = profile_schema.dump(post)

    ret_data = {
        'data': data,
        'status': 'success'
    }


    return custom_response(ret_data, 200)
    
@profile_api.route('', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()


    # app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    # user = ProfileModel.get_one_user(g.user.get('id'))
    # req_data['owner_id'] = user.id
    try:
        data = user_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    user_in_db = UserModel.get_user_by_email(data.get("email"))
    if user_in_db:
        return custom_response_error('User already exist, please supply another email address')

    user = UserModel(data)
    user.save()

    try:
        req_data['user_id'] = user.id
        if req_data.get('role'):
            req_data['role'] = req_data.get('role')
        else:
            req_data['role'] = 'normal'

        data = profile_schema.load(req_data)
        post = ProfileModel(data)
        post.save()
    except Exception as err:
        user.delete()
        return custom_response(err, 400)
    
    try:
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

    print(req_data)
    post = ProfileModel.get_one(profile_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    # data = profile_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = profile_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response({'error': err}, 400)

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
    post.delete()

    user = UserModel.get_one(post.user_id)
    user.delete()

    return custom_response({'message': 'deleted'}, 204)


def custom_response_error(message):
    msg = {
        "status": "error",
        "message" : message
    }

    return Response(
        mimetype="application/json",
        response=json.dumps(msg),
        status=400
    )

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )