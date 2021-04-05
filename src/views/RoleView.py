#/src/views/RoleView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.RoleModel import RoleModel, RoleSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
role_api = Blueprint('role_api', __name__)
role_schema = RoleSchema()


@role_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Roles
    """
    posts = RoleModel.get_all()
    data = role_schema.dump(posts, many=True)
    return custom_response(data, 200)

@role_api.route('/<int:role_id>', methods=['GET'])
def get_one(role_id):
    """
    Get A Role
    """
    post = RoleModel.get_one(role_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = role_schema.dump(post)
    return custom_response(data, 200)
    
@role_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Role Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = role_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = RoleModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = role_schema.dump(post)
    return custom_response(data, 201)    

@role_api.route('/<int:role_id>', methods=['PUT'])
@Auth.auth_required
def update(role_id):
    """
    Update A Role
    """
    req_data = request.get_json()
    post = RoleModel.get_one(role_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = role_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = role_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = role_schema.dump(post)
    return custom_response(data, 200)

@role_api.route('/<int:role_id>', methods=['DELETE'])
@Auth.auth_required
def delete(role_id):
    """
    Delete A Role
    """
    post = RoleModel.get_one(role_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = role_schema.dump(post)
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