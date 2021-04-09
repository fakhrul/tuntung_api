# /src/views/CampaignView.py
from flask import Flask, request, g, Blueprint, json, Response
from marshmallow import ValidationError, EXCLUDE
from ..shared.Authentication import Auth
from ..shared.Mailing import Mailing
from ..models.CampaignModel import CampaignModel, CampaignSchema
from ..models.CampaignScheduleModel import CampaignScheduleModel,CampaignScheduleSchema
from ..models.UserModel import UserModel
from ..shared.Utility import custom_response_data, custom_response_error

app = Flask(__name__)
campaign_api = Blueprint('campaign_api', __name__)
campaign_schema = CampaignSchema(unknown=EXCLUDE)

campaign_schedule_schema = CampaignScheduleSchema(unknown=EXCLUDE)

@campaign_api.route('/', methods=['GET'])
def get_all():
    campaign = CampaignModel.get_all()
    data = campaign_schema.dump(campaign, many=True)
    retObj = {
        'data' : data,
    }

    response = custom_response(retObj, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print('cors-debug')
    return response


@campaign_api.route('/<int:campaign_id>', methods=['GET'])
def get_one(campaign_id):
    post = CampaignModel.get_one(campaign_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = campaign_schema.dump(post)
    return custom_response_data(data, 200)


@campaign_api.route('', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    print(req_data)
    try:
        schema = CampaignSchema(exclude=['campaign_schedule_list', 'advertiser', 'audience', ], unknown=EXCLUDE)
        data = schema.load(req_data)
        campaign = CampaignModel(data)
        campaign.save()

        scheduleList = req_data['campaign_schedule_list']
        for scheduleJson in scheduleList:
            scheduleJson['campaign_id'] = campaign.id
            data = campaign_schedule_schema.load(scheduleJson)
            schedule = CampaignScheduleModel(data)
            schedule.save()
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)
    # except ValidationError as err:
    #     return custom_response(err, 400)

    # try:
    #     app.logger.info('llego al correo ?------ ')
    #     Mailing.send_mail(user)
    # except Exception as e:
    #     app.logger.error(e)
    data = campaign_schema.dump(campaign)
    return custom_response_data(data, 201)


@campaign_api.route('/<int:campaign_id>', methods=['PUT'])
@Auth.auth_required
def update(campaign_id):
    req_data = request.get_json()
    campaign = CampaignModel.get_one(campaign_id)
    if not campaign:
        return custom_response_error('Data not found', 404)

    try:
        schema = CampaignSchema(exclude=['campaign_schedule_list', 'advertiser', 'audience', ], unknown=EXCLUDE)
        data = schema.load(req_data, partial=True)
        campaign.update(data)
    except Exception as err:
        app.logger.info(err)
        return custom_response_error(str(err), 400)

    data = campaign_schema.dump(campaign)
    return custom_response(data, 200)


@campaign_api.route('/<int:campaign_id>', methods=['DELETE'])
@Auth.auth_required
def delete(campaign_id):
    campaign = CampaignModel.get_one(campaign_id)
    if not campaign:
        return custom_response({'error': 'Data not found'}, 404)
    data = campaign_schema.dump(campaign)
    campaign.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
