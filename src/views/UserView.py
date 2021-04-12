#/src/views/UserView

from flask import Flask, request, json, Response, Blueprint, g, jsonify
from marshmallow import ValidationError
from ..models.UserModel import UserModel, UserSchema
from ..models.ProfileModel import ProfileModel, ProfileSchema
from ..shared.Authentication import Auth
from ..shared.Utility import custom_response_data, custom_response_error, custom_response_success, custom_response

app = Flask(__name__)
user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()
profile_schema = ProfileSchema()

@user_api.route('/register', methods=['POST'])
def create():
    req_data = request.get_json()
    
    try:
        # data = user_schema.load(req_data)
        data = user_schema.load({
            "email": req_data["email"],
            "password": req_data["password"]
        })
        # check if user already exist in the db
        user_in_db = UserModel.get_user_by_email(data.get('email'))
        if user_in_db:
            message = {'error': 'User already exist, please supply another email address'}
            return custom_response(message, 400)

        user = UserModel(data)
        user.save()
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)

    try:
        role = 'normal'
        if req_data.get('role'):
            role = req_data.get('role')
        profile_data = profile_schema.load({
            "email": user.email,
            "user_id": user.id,
            "role": role
        })
        profile = ProfileModel(profile_data)
        profile.save()

        ser_user = user_schema.dump(user)
        ser_profile = profile_schema.dump(profile)
        token = Auth.generate_token(ser_user.get('id'))
        data = {
            'token': token,
            'user': ser_user,
            'profile': ser_profile,
            'status': 'success'
        }
        return custom_response(data, 201)
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)



@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    return custom_response(ser_users, 200)

@user_api.route('/loginAdmin', methods=['POST'])
def loginAdmin():
    req_data = request.get_json()
    
    try:
        data = user_schema.load({
            "email": req_data.get("email"),
            "password": req_data.get("password")
            }, partial=True)

        if not data.get('email') or not data.get('password'):
            return custom_response_error('you need email and password to sign in', 400)

        user = UserModel.get_user_by_email(data.get('email'))
        if not user:
            return custom_response_error('no user found', 400)
        if not user.check_hash(data.get('password')):
            return custom_response_error('invalid credentials', 400)

        profile = ProfileModel.get_profile_by_email(data.get('email'))
        if not profile:
            return custom_response_error('no profile found', 400)
        if profile.role != 'admin':
            return custom_response_error('invalid role', 400)

        ser_user = user_schema.dump(user)
        ser_profile = profile_schema.dump(profile)
        token = Auth.generate_token(ser_user.get('id'))
        data = {
            'token': token,
            'user': ser_user,
            'profile': ser_profile,
            'status': 'success'
        }
        return custom_response(data, 200)

    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)

@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    
    try:
        data = user_schema.load({
            "email": req_data.get("email"),
            "password": req_data.get("password")
            }, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)
    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    user = UserModel.get_user_by_email(data.get('email'))
    if not user:
        return custom_response({'error': 'no user found'}, 400)
    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)

    profile = ProfileModel.get_profile_by_email(data.get('email'))
    if not profile:
        return custom_response({'error': 'no profile found'}, 400)

    ser_user = user_schema.dump(user)
    ser_profile = profile_schema.dump(profile)
    token = Auth.generate_token(ser_user.get('id'))
    data = {
        'token': token,
        'user': ser_user,
        'profile': ser_profile,
        'status': 'success'
    }
    return custom_response(data, 200)

@user_api.route('/loginfg', methods=['POST'])
def loginfg():
    """
    User Login Function
    """
    req_data = request.get_json()
    app.logger.info('llega siquiera --------------#'+json.dumps(req_data))
    
    try:
        data = user_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    if not data.get('email') or not data.get('tokenfg'):
        return custom_response({'error': 'you need email and token from facebook/gmail to sign in'}, 400)

    user = UserModel.get_user_by_email(data.get('email'))
    if not user:
        return custom_response({'error': 'email does not exist'}, 400)
    # if not user.check_hash(data.get('password')):
    #     return custom_response({'error': 'invalid credentials'}, 400)
    #Aqui en vez de revisar password revisamos contra feis y google q si funcione el token válido

    ser_data = user_schema.dump(user)

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)  

@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    """
    Get a single user
    """
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)

@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    try:
        data = user_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err, 400)

    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)

@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete a user
    """
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, 204)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
    Get me
    """
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


# def custom_response(res, status_code):
#     """
#     Custom Response Function
#     """
#     return Response(
#         mimetype="application/json",
#         response=json.dumps(res),
#         status=status_code
#     )
