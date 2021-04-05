#/src/views/NotificationView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.NotificationModel import NotificationModel, NotificationSchema
from ..models.UserModel import UserModel

app = Flask(__name__)
notification_api = Blueprint('notification_api', __name__)
notification_schema = NotificationSchema()


@notification_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Notifications
    """
    posts = NotificationModel.get_all()
    data = notification_schema.dump(posts, many=True)
    return custom_response(data, 200)

@notification_api.route('/<int:notification_id>', methods=['GET'])
def get_one(notification_id):
    """
    Get A Notification
    """
    post = NotificationModel.get_one(notification_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = notification_schema.dump(post)
    return custom_response(data, 200)
    
@notification_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Notification Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera blog--------------#'+json.dumps(req_data))
    user = UserModel.get_one_user(g.user.get('id'))
    req_data['owner_id'] = user.id

    try:
        data = notification_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err, 400)
        
    post = NotificationModel(data)
    post.save()
    try:
        app.logger.info('llego al correo ?------ ')
        Mailing.send_mail(user)
    except Exception as e:
        app.logger.error(e)
    data = notification_schema.dump(post)
    return custom_response(data, 201)    

@notification_api.route('/<int:notification_id>', methods=['PUT'])
@Auth.auth_required
def update(notification_id):
    """
    Update A Notification
    """
    req_data = request.get_json()
    post = NotificationModel.get_one(notification_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = notification_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = notification_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    post.update(data)
    data = notification_schema.dump(post)
    return custom_response(data, 200)

@notification_api.route('/<int:notification_id>', methods=['DELETE'])
@Auth.auth_required
def delete(notification_id):
    """
    Delete A Notification
    """
    post = NotificationModel.get_one(notification_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = notification_schema.dump(post)
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