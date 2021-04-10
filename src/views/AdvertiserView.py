# /src/views/AdvertiserView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.AdvertiserModel import AdvertiserModel, AdvertiserSchema
from ..models.UserModel import UserModel
from ..shared.Utility import custom_response_data, custom_response_error

app = Flask(__name__)
advertiser_api = Blueprint('advertiser_api', __name__)
advertiser_schema = AdvertiserSchema(unknown=EXCLUDE)

@advertiser_api.route('/', methods=['GET'])
def get_all():
    posts = AdvertiserModel.get_all()
    data = advertiser_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # print('cors-debug')
    return response


@advertiser_api.route('/<int:advertiser_id>', methods=['GET'])
def get_one(advertiser_id):
    post = AdvertiserModel.get_one(advertiser_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = advertiser_schema.dump(post)
    return custom_response_data(data, 200)
    # return custom_response(data, 200)


@advertiser_api.route('', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    try:
        schema = AdvertiserSchema(exclude=['profile', ], unknown=EXCLUDE)
        data = schema.load(req_data)
        post = AdvertiserModel(data)
        post.save()
        data = schema.dump(post)
        return custom_response_data(data, 201)
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)
    # except ValidationError as err:
    #     app.logger.info(err)
    #     return custom_response_error("Validation Exception", 400)
        # return custom_response("Validation Error", 400)

    # try:
    #     app.logger.info('llego al correo ?------ ')
    #     Mailing.send_mail(user)
    # except Exception as e:
    #     app.logger.error(e)


@advertiser_api.route('/<int:advertiser_id>', methods=['PUT'])
# @Auth.auth_required
def update(advertiser_id):
    req_data = request.get_json()
    obj = AdvertiserModel.get_one(advertiser_id)
    if not obj:
        return custom_response_error('Data not found', 404)
    data = advertiser_schema.dump(obj)

    try:
        data = advertiser_schema.load(req_data, partial=True)
        obj.update(data)
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)
    # except ValidationError as err:
    #     return custom_response(err, 400)

    data = advertiser_schema.dump(obj)
    return custom_response_data(data, 200)


@advertiser_api.route('/<int:advertiser_id>', methods=['DELETE'])
@Auth.auth_required
def delete(advertiser_id):
    try:

        post = AdvertiserModel.get_one(advertiser_id)
        if not post:
            return custom_response({'error': 'post not found'}, 404)
        post.delete()
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)

    return custom_response({'message': 'deleted'}, 204)


# def custom_response_error(message, status_code):
#     msg = {
#         "status": "error",
#         "message" : message
#     }

#     return Response(
#         mimetype="application/json",
#         response=json.dumps(msg),
#         status=status_code
#     )


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
