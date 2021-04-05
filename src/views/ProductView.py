#/src/views/ProductView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.ProductModel import ProductModel, ProductSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
product_api = Blueprint('product_api', __name__)
product_schema = ProductSchema()


@product_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Products
    """
    posts = ProductModel.get_all()
    data = product_schema.dump(posts, many=True)
    return custom_response(data, 200)

@product_api.route('/<int:product_id>', methods=['GET'])
def get_one(product_id):
    """
    Get A Product
    """
    post = ProductModel.get_one(product_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = product_schema.dump(post)
    return custom_response(data, 200)
    
@product_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Product Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = product_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = ProductModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = product_schema.dump(post)
    return custom_response(data, 201)    

@product_api.route('/<int:product_id>', methods=['PUT'])
@Auth.auth_required
def update(product_id):
    """
    Update A Product
    """
    req_data = request.get_json()
    post = ProductModel.get_one(product_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = product_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = product_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = product_schema.dump(post)
    return custom_response(data, 200)

@product_api.route('/<int:product_id>', methods=['DELETE'])
@Auth.auth_required
def delete(product_id):
    """
    Delete A Product
    """
    post = ProductModel.get_one(product_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = product_schema.dump(post)
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