#!/usr/bin/env python
# encoding: utf-8

"""
Service interface for User Segmentation - Licious
"""
import os
import settings

from flask import (abort, Flask, Response, request, jsonify, json as fjson, make_response)

app = Flask(__name__)
ALLOWED_IPS = ['127.0.0.1']


@app.route('/experiment', methods=['POST'])
def assign_experiment_group():
    query_parameters = request.args
    session_id = query_parameters.get('session_id')
    user_id = query_parameters.get('user_id')
    if not session_id or not user_id:
        return make_response({"success": False, "message": "Insufficient payload"}, 400)
    try:
        pass
    except Exception as e:
        return make_response({"exception": e}, 500)
    return make_response({"success": True}, 200)


@app.route('/experiment', methods=['GET'])
def get_group_by_experiment():
    query_parameters = request.args
    session_id = query_parameters.get('session_id')
    user_id = query_parameters.get('user_id')
    experiment_name = query_parameters.get('experiment_name')
    if not session_id or not user_id or not experiment_name:
        return make_response({"success": False, "message": "Insufficient payload"}, 400)
    try:
        group = None
    except Exception as e:
        return make_response({"exception": e, "group": None}, 500)
    return make_response({"success": True, "group": group}, 200)


if __name__ == '__main__':
    app.run(
        host=settings.SERVICE_IP,
        port=settings.SERVICE_PORT,
        debug=os.environ.get('NIKI_ENV', 'production') in ('dev', 'beta'),
        threaded=True
    )
