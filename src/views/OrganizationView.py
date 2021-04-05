# /src/views/OrganizationView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.OrganizationModel import OrganizationModel, OrganizationSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
organization_api = Blueprint('organization_api', __name__)
organization_schema = OrganizationSchema()

@organization_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Organizations
    """
    posts = OrganizationModel.get_all()
    data = organization_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@organization_api.route('/<int:organization_id>', methods=['GET'])
def get_one(organization_id):
    """
    Get A Organization
    """
    post = OrganizationModel.get_one(organization_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = organization_schema.dump(post)
    return custom_response(data, 200)


@organization_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Organization Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = organization_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    post = OrganizationModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = organization_schema.dump(post)
    return custom_response(data, 201)


@organization_api.route('/<int:organization_id>', methods=['PUT'])
# @Auth.auth_required
def update(organization_id):
    """
    Update A Organization
    """
    req_data = request.get_json()
    post = OrganizationModel.get_one(organization_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = organization_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = organization_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = organization_schema.dump(post)
    return custom_response(data, 200)


@organization_api.route('/<int:organization_id>', methods=['DELETE'])
@Auth.auth_required
def delete(organization_id):
    """
    Delete A Organization
    """
    post = OrganizationModel.get_one(organization_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = organization_schema.dump(post)
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
