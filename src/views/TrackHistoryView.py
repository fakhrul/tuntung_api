#/src/views/TrackHistoryView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.TrackHistoryModel import TrackHistoryModel, TrackHistorySchema
from ..models.UserModel import UserModel

app = Flask(__name__)
track_history_api = Blueprint('track_history_api', __name__)
track_history_schema = TrackHistorySchema()


@track_history_api.route('/', methods=['GET'])
def get_all():
    """
    Get All TrackHistorys
    """
    posts = TrackHistoryModel.get_all()
    data = track_history_schema.dump(posts, many=True)
    return custom_response(data, 200)

@track_history_api.route('/<int:track_history_id>', methods=['GET'])
def get_one(track_history_id):
    """
    Get A TrackHistory
    """
    post = TrackHistoryModel.get_one(track_history_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = track_history_schema.dump(post)
    return custom_response(data, 200)
    
@track_history_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create TrackHistory Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = track_history_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = TrackHistoryModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = track_history_schema.dump(post)
    return custom_response(data, 201)    

@track_history_api.route('/<int:track_history_id>', methods=['PUT'])
@Auth.auth_required
def update(track_history_id):
    """
    Update A TrackHistory
    """
    req_data = request.get_json()
    post = TrackHistoryModel.get_one(track_history_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = track_history_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = track_history_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = track_history_schema.dump(post)
    return custom_response(data, 200)

@track_history_api.route('/<int:track_history_id>', methods=['DELETE'])
@Auth.auth_required
def delete(track_history_id):
    """
    Delete A TrackHistory
    """
    post = TrackHistoryModel.get_one(track_history_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = track_history_schema.dump(post)
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