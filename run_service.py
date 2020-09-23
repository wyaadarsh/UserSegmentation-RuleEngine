#!/usr/bin/env python
# encoding: utf-8

"""
Service interface for User Segmentation - Licious
"""
import os
import settings

from flask import (abort, Flask, Response, request, jsonify, json as fjson, make_response)
from service.rest_util import *

app = Flask(__name__)
ALLOWED_IPS = ['127.0.0.1']


@app.route('/validate/<user_id>/<segment_id>', methods=['GET,POST'])
def get_user_segment(user_id,segment_id):
    try:
        res=evaluate_user_segment(user_id,segment_id)

    except:
        make_response({"success": False, "error_code": 400})
    return make_response({"success": True,"message":res})

@app.route('/validate/', methods=['GET,POST'])
def get_user_segment():
    res = dict()
    query=request.json
    try:

        # for query in request.json:
        #     res[query[0]]=evaluate_user_segment(query[0],query[1])
        res=bulk_identify_segment(query[0],query[1])
    except:
        make_response({"success": False, "error_code": 400})
    return make_response(jsonify(res))



@app.route('/user/', methods=['POST'])
def insert_user():
    user_data = request.json
    try:
        if isinstance(user_data,list):
            bulk_insert_users(user_data)
        else:
            insert_new_user(user_data)
    except:
        make_response({"success": False, "error_code": 400})
    return make_response({"success": True})


@app.route('/segment/', methods=['POST'])
def insert_segment():
    segment_data = request.json
    try:
        if isinstance(segment_data,list):
            bulk_insert_segments(segment_data)
        else:
            insert_segment(segment_data)
    except:
        make_response({"success": False, "error_code": 400})
    return make_response({"success": True})


# @app.route('/experiment', methods=['POST'])
# def assign_experiment_group():
#     query_parameters = request.args
#     session_id = query_parameters.get('session_id')
#     user_id = query_parameters.get('user_id')
#     if not session_id or not user_id:
#         return make_response({"success": False, "message": "Insufficient payload"}, 400)
#     try:
#         pass
#     except Exception as e:
#         return make_response({"exception": e}, 500)
#     return make_response({"success": True}, 200)
#
#
# @app.route('/experiment', methods=['GET'])
# def get_group_by_experiment():
#     query_parameters = request.args
#     session_id = query_parameters.get('session_id')
#     user_id = query_parameters.get('user_id')
#     experiment_name = query_parameters.get('experiment_name')
#     if not session_id or not user_id or not experiment_name:
#         return make_response({"success": False, "message": "Insufficient payload"}, 400)
#     try:
#         group = None
#     except Exception as e:
#         return make_response({"exception": e, "group": None}, 500)
#     return make_response({"success": True, "group": group}, 200)
#
#
if __name__ == '__main__':
    app.run(
        host=settings.SERVICE_IP,
        port=settings.SERVICE_PORT,
        debug=os.environ.get('NIKI_ENV', 'production') in ('dev', 'beta'),
        threaded=True
    )
