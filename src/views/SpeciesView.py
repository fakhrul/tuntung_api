#/src/views/SpeciesView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.SpeciesModel import SpeciesModel, SpeciesSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
species_api = Blueprint('species_api', __name__)
species_schema = SpeciesSchema()


@species_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Speciess
    """
    posts = SpeciesModel.get_all()
    data = species_schema.dump(posts, many=True)
    return custom_response(data, 200)

@species_api.route('/<int:species_id>', methods=['GET'])
def get_one(species_id):
    """
    Get A Species
    """
    post = SpeciesModel.get_one(species_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = species_schema.dump(post)
    return custom_response(data, 200)
    
@species_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Species Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = species_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = SpeciesModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = species_schema.dump(post)
    return custom_response(data, 201)    

@species_api.route('/<int:species_id>', methods=['PUT'])
@Auth.auth_required
def update(species_id):
    """
    Update A Species
    """
    req_data = request.get_json()
    post = SpeciesModel.get_one(species_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = species_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = species_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = species_schema.dump(post)
    return custom_response(data, 200)

@species_api.route('/<int:species_id>', methods=['DELETE'])
@Auth.auth_required
def delete(species_id):
    """
    Delete A Species
    """
    post = SpeciesModel.get_one(species_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = species_schema.dump(post)
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