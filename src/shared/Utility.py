
from flask import  json, Response

def custom_response_data(data, status_code):
    msg = {
        "status": "success",
        "data" : data,
        "message" : ""
    }

    return Response(
        mimetype="application/json",
        response=json.dumps(msg),
        status=status_code
    )

def custom_response_success():
    msg = {
        "status": "success",
        "message" : ""
    }

    return Response(
        mimetype="application/json",
        response=json.dumps(msg),
        status=200
    )

def custom_response_error(message, status_code):
    msg = {
        "status": "error",
        "message" : message
    }

    return Response(
        mimetype="application/json",
        response=json.dumps(msg),
        status=status_code
    )


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
