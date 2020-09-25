#!/usr/bin/env python
# encoding: utf-8

"""
Service interface for User Segmentation - Licious
"""
import os
import settings

from flask import (abort, Flask, Response, request, jsonify, make_response)
from service.rest_util import *

app = Flask(__name__)
ALLOWED_IPS = ['127.0.0.1']


# @app.route('/validatesingle/', methods=['GET'])
# def get_user_segment():
#     try:
#         user_id, segment_id = request.args['user_id'], request.args['segment_id']
#         res = evaluate_user_segment(user_id, segment_id)
#     except:
#         return make_response({"success": False, "error_code": 400})
#     return make_response({"success": True, "message": res})
#

@app.route('/validate/', methods=['POST'])
def get_user_segments():
    res = dict()
    query = request.json
    try:
        res = bulk_identify_segment(query.get('user_id'), query.get('segments'))
    except:
        return make_response({"success": False, "error_code": 400})
    return make_response(jsonify(res))


@app.route('/user/', methods=['POST'])
def insert_user():
    user_data = request.json
    try:
        if isinstance(user_data, list):
            bulk_insert_users(user_data)
        else:
            insert_new_user(user_data)
    except:
        return make_response({"success": False, "error_code": 400})
    return make_response({"success": True})


@app.route('/user/<id>/', methods=['GET'])
def user_detail(id):
    try:
        res = get_user(id)
    except:
        return make_response({"success": False, "error_code": 400})
    return make_response(jsonify(res))


@app.route('/segment/', methods=['POST'])
def insert_segment():
    segment_data = request.json
    try:
        if isinstance(segment_data, list):
            bulk_insert_segments(segment_data)
        else:
            insert_new_segment(segment_data)
    except:
        return make_response({"success": False, "error_code": 400})
    return make_response({"success": True})


@app.route('/segment/<id>/', methods=['GET'])
def segment_detail(id):
    try:
        res = get_segment(id)
    except:
        return make_response({"success": False, "error_code": 400})
    return make_response(jsonify(res))


if __name__ == '__main__':
    app.run(
        host=settings.SERVICE_IP,
        port=settings.SERVICE_PORT
    )
