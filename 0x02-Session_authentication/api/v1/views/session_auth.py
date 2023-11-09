#!/usr/bin/env python3
""" Creates a new Flask view that handles all
    routes for the Session authentication
"""
from flask import jsonify, abort, request, make_response
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'])
def auth_session_login():
    """ adds the view """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    for u in user:
        if not u.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    u = user[0]
    ses_id = auth.create_session(u.id)
    user_dict = u.to_json()
    response = make_response(jsonify(user_dict))

    response.set_cookie(getenv("SESSION_NAME"), ses_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'])
def auth_session_logout():
    """ deletes session id contains in the request as cookie """
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if destroy_session is False:
        abort(404)
    return jsonify({}), 200
