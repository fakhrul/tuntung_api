# /src/views/LedView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.LedModel import LedModel, LedSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
led_api = Blueprint('led_api', __name__)
led_schema = LedSchema()

@led_api.route('/', methods=['GET'])
def get_all():
    posts = LedModel.get_all()
    data = led_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@led_api.route('/<int:led_id>', methods=['GET'])
def get_one(led_id):
    post = LedModel.get_one(led_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = led_schema.dump(post)
    return custom_response(data, 200)


@led_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = led_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    post = LedModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = led_schema.dump(post)
    return custom_response(data, 201)


@led_api.route('/<int:led_id>', methods=['PUT'])
# @Auth.auth_required
def update(led_id):
    req_data = request.get_json()
    post = LedModel.get_one(led_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = led_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = led_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = led_schema.dump(post)
    return custom_response(data, 200)


@led_api.route('/<int:led_id>', methods=['DELETE'])
@Auth.auth_required
def delete(led_id):
    post = LedModel.get_one(led_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = led_schema.dump(post)
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
