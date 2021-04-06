# /src/views/WalkerView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.WalkerModel import WalkerModel, WalkerSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
walker_api = Blueprint('walker_api', __name__)
walker_schema = WalkerSchema()

@walker_api.route('/', methods=['GET'])
def get_all():
    posts = WalkerModel.get_all()
    data = walker_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@walker_api.route('/<int:walker_id>', methods=['GET'])
def get_one(walker_id):
    post = WalkerModel.get_one(walker_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = walker_schema.dump(post)
    return custom_response(data, 200)


@walker_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = walker_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    post = WalkerModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = walker_schema.dump(post)
    return custom_response(data, 201)


@walker_api.route('/<int:walker_id>', methods=['PUT'])
# @Auth.auth_required
def update(walker_id):
    req_data = request.get_json()
    post = WalkerModel.get_one(walker_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = walker_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = walker_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = walker_schema.dump(post)
    return custom_response(data, 200)


@walker_api.route('/<int:walker_id>', methods=['DELETE'])
@Auth.auth_required
def delete(walker_id):
    post = WalkerModel.get_one(walker_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = walker_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
