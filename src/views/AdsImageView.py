#/src/views/AdsImageView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.AdsImageModel import AdsImageModel, AdsImageSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
ads_image_api = Blueprint('ads_image_api', __name__)
ads_image_schema = AdsImageSchema()


@ads_image_api.route('/', methods=['GET'])
def get_all():
    posts = AdsImageModel.get_all()
    data = ads_image_schema.dump(posts, many=True)
    return custom_response(data, 200)

@ads_image_api.route('/<int:ads_image_id>', methods=['GET'])
def get_one(ads_image_id):
    post = AdsImageModel.get_one(ads_image_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = ads_image_schema.dump(post)
    return custom_response(data, 200)
    
@ads_image_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = ads_image_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = AdsImageModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = ads_image_schema.dump(post)
    return custom_response(data, 201)    

@ads_image_api.route('/<int:ads_image_id>', methods=['PUT'])
@Auth.auth_required
def update(ads_image_id):
    req_data = request.get_json()
    post = AdsImageModel.get_one(ads_image_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = ads_image_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = ads_image_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = ads_image_schema.dump(post)
    return custom_response(data, 200)

@ads_image_api.route('/<int:ads_image_id>', methods=['DELETE'])
@Auth.auth_required
def delete(ads_image_id):
    post = AdsImageModel.get_one(ads_image_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = ads_image_schema.dump(post)
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