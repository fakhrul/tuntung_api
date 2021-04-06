# /src/views/CampaignEnrollView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.CampaignEnrollModel import CampaignEnrollModel, CampaignEnrollSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
campaign_enroll_api = Blueprint('campaign_enroll_api', __name__)
campaign_enroll_schema = CampaignEnrollSchema()

@campaign_enroll_api.route('/', methods=['GET'])
def get_all():
    posts = CampaignEnrollModel.get_all()
    data = campaign_enroll_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@campaign_enroll_api.route('/<int:campaign_enroll_id>', methods=['GET'])
def get_one(campaign_enroll_id):
    post = CampaignEnrollModel.get_one(campaign_enroll_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = campaign_enroll_schema.dump(post)
    return custom_response(data, 200)


@campaign_enroll_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = campaign_enroll_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    post = CampaignEnrollModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = campaign_enroll_schema.dump(post)
    return custom_response(data, 201)


@campaign_enroll_api.route('/<int:campaign_enroll_id>', methods=['PUT'])
# @Auth.auth_required
def update(campaign_enroll_id):
    req_data = request.get_json()
    post = CampaignEnrollModel.get_one(campaign_enroll_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = campaign_enroll_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = campaign_enroll_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = campaign_enroll_schema.dump(post)
    return custom_response(data, 200)


@campaign_enroll_api.route('/<int:campaign_enroll_id>', methods=['DELETE'])
@Auth.auth_required
def delete(campaign_enroll_id):
    post = CampaignEnrollModel.get_one(campaign_enroll_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = campaign_enroll_schema.dump(post)
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
