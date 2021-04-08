# /src/views/BusinessCategoryView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.BusinessCategoryModel import BusinessCategoryModel, BusinessCategorySchema
from ..models.UserModel import UserModel

app = Flask(__name__)
business_category_api = Blueprint('business_category_api', __name__)
business_category_schema = BusinessCategorySchema(unknown=EXCLUDE)

@business_category_api.route('/', methods=['GET'])
def get_all():
    posts = BusinessCategoryModel.get_all()
    data = business_category_schema.dump(posts, many=True)

    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@business_category_api.route('/<int:business_category_id>', methods=['GET'])
def get_one(business_category_id):
    post = BusinessCategoryModel.get_one(business_category_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = business_category_schema.dump(post)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 200)


@business_category_api.route('', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    # app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    # user = UserModel.get_one_user(g.user.get('id'))
    # req_data['owner_id'] = user.id

    try:
        data = business_category_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)

    post = BusinessCategoryModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = business_category_schema.dump(post)
    return custom_response(data, 201)


@business_category_api.route('/<int:business_category_id>', methods=['PUT'])
# @Auth.auth_required
def update(business_category_id):
    req_data = request.get_json()
    post = BusinessCategoryModel.get_one(business_category_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = business_category_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    try:
        data = business_category_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = business_category_schema.dump(post)
    return custom_response(data, 200)


@business_category_api.route('/<int:business_category_id>', methods=['DELETE'])
@Auth.auth_required
def delete(business_category_id):
    post = BusinessCategoryModel.get_one(business_category_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = business_category_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
