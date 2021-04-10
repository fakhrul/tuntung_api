#/src/views/AdsImageView.py
from flask import Flask, request, g, Blueprint, json, Response, send_file
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.AdsImageModel import AdsImageModel, AdsImageSchema
from ..models.UserModel import UserModel
from ..shared.Utility import custom_response_data, custom_response_error, custom_response, custom_response_success
import base64
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
ads_image_api = Blueprint('ads_image_api', __name__)
ads_image_schema = AdsImageSchema(unknown=EXCLUDE)
image_folder = os.getenv('IMAGE_FOLDER')


@ads_image_api.route('/', methods=['GET'])
def get_all():
    posts = AdsImageModel.get_all()
    data = ads_image_schema.dump(posts, many=True)
    return custom_response_data(data, 200)

@ads_image_api.route('/byAdvertiser/<int:advertiser_id>', methods=['GET'])
def get_all_by_advertiser(advertiser_id):
    print('a')
    posts = AdsImageModel.get_by_advertiser_id(advertiser_id)
    data = ads_image_schema.dump(posts, many=True)
    return custom_response_data(data, 200)


@ads_image_api.route('/<int:ads_image_id>', methods=['GET'])
def get_one(ads_image_id):
    post = AdsImageModel.get_one(ads_image_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = ads_image_schema.dump(post)
    return custom_response(data, 200)

@ads_image_api.route('/image/<int:ads_image_id>', methods=['GET'])
def get_image(ads_image_id):
    try:
        image = AdsImageModel.get_one(ads_image_id)
        if not image:
            return custom_response_error("image not found", 404)
        
        advertiser_folder = os.path.join(image_folder, str(image.advertiser_id))
        file_name = str(image.id) + ".png"
        image_path = os.path.join(advertiser_folder,  file_name)
        return send_file(image_path, mimetype='image/png')
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)
       

@ads_image_api.route('', methods=['POST'])
@Auth.auth_required
def create():
    try:
        req_data = request.get_json()
        base64_png =  req_data['image']
        code = base64.b64decode(base64_png.split(',')[1]) 
        image_decoded = Image.open(BytesIO(code))
        # image_decoded.save(Path(app.config['UPLOAD_FOLDER']) / 'image.png')
        # image_decoded.verify()

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        schema = AdsImageSchema(exclude=['advertiser'], unknown=EXCLUDE)
        data = schema.load(req_data, partial=True)
        image = AdsImageModel(data)
        image.save()

        advertiser_folder = os.path.join(image_folder, str(image.advertiser_id))

        if not os.path.exists(advertiser_folder):
            os.makedirs(advertiser_folder)

        file_name = str(image.id) + ".png"
        image_path = os.path.join(advertiser_folder,  file_name)

        image_decoded.save(image_path)
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)

    data = ads_image_schema.dump(image)
    return custom_response_data(data, 201)    

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
    try:
        image = AdsImageModel.get_one(ads_image_id)
        image.delete()

        advertiser_folder = os.path.join(image_folder, str(image.advertiser_id))
        file_name = str(image.id) + ".png"
        image_path = os.path.join(advertiser_folder,  file_name)
        if os.path.exists(image_path):
            os.remove(image_path)

        return custom_response_success()
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)



# def custom_response(res, status_code):
#     """
#     Custom Response Function
#     """
#     return Response(
#         mimetype="application/json",
#         response=json.dumps(res),
#         status=status_code
#     )