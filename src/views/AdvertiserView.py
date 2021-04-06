# /src/views/AdvertiserView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.AdvertiserModel import AdvertiserModel, AdvertiserSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
advertiser_api = Blueprint('advertiser_api', __name__)
advertiser_schema = AdvertiserSchema()

@advertiser_api.route('/', methods=['GET'])
def get_all():
    posts = AdvertiserModel.get_all()
    data = advertiser_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@advertiser_api.route('/<int:advertiser_id>', methods=['GET'])
def get_one(advertiser_id):
    post = AdvertiserModel.get_one(advertiser_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = advertiser_schema.dump(post)
    return custom_response(data, 200)


@advertiser_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = advertiser_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    post = AdvertiserModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = advertiser_schema.dump(post)
    return custom_response(data, 201)


@advertiser_api.route('/<int:advertiser_id>', methods=['PUT'])
# @Auth.auth_required
def update(advertiser_id):
    req_data = request.get_json()
    post = AdvertiserModel.get_one(advertiser_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = advertiser_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = advertiser_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = advertiser_schema.dump(post)
    return custom_response(data, 200)


@advertiser_api.route('/<int:advertiser_id>', methods=['DELETE'])
@Auth.auth_required
def delete(advertiser_id):
    post = AdvertiserModel.get_one(advertiser_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = advertiser_schema.dump(post)
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
