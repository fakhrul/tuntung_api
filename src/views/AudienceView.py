# /src/views/AudienceView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.AudienceModel import AudienceModel, AudienceSchema
from ..models.UserModel import UserModel
from ..shared.Utility import custom_response_data, custom_response_error, custom_response

app = Flask(__name__)
audience_api = Blueprint('audience_api', __name__)
audience_schema = AudienceSchema(unknown=EXCLUDE)

@audience_api.route('/', methods=['GET'])
def get_all():
    posts = AudienceModel.get_all()
    data = audience_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@audience_api.route('/<int:audience_id>', methods=['GET'])
def get_one(audience_id):
    post = AudienceModel.get_one(audience_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = audience_schema.dump(post)
    retObj = {
        'data' : data,
    }

    return custom_response(retObj, 200)


@audience_api.route('', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    try:
        data = audience_schema.load(req_data)
        post = AudienceModel(data)
        post.save()
    except Exception as err:
        return custom_response_error(str(err), 400)

    data = audience_schema.dump(post)
    return custom_response(data, 201)


@audience_api.route('/<int:audience_id>', methods=['PUT'])
# @Auth.auth_required
def update(audience_id):
    req_data = request.get_json()
    post = AudienceModel.get_one(audience_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = audience_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = audience_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = audience_schema.dump(post)
    return custom_response(data, 200)


@audience_api.route('/<int:audience_id>', methods=['DELETE'])
@Auth.auth_required
def delete(audience_id):
    post = AudienceModel.get_one(audience_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = audience_schema.dump(post)

    post.delete()
    return custom_response({'message': 'deleted'}, 204)


# def custom_response(res, status_code):
#     return Response(
#         mimetype="application/json",
#         response=json.dumps(res),
#         status=status_code
#     )
