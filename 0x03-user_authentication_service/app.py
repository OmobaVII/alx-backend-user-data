#!/usr/bin/env python3
""" Sets up a basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
from flask import redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def welcome() -> str:
    """ returns a jsonify payload """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """ register a user to database """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        msg = {"email": email, "message": "user created"}
        return jsonify(msg)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """ create a new session for a user """
    email = request.form.get("email")
    password = request.form.get("password")
    login = AUTH.valid_login(email, password)
    if login is False:
        abort(401)
    session_id = AUTH.create_session(email)
    user_dict = {"email": email, "message": "logged in"}
    response = make_response(jsonify(user_dict))
    response.set_cookie("session_id", session_id)

    return response

@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """ logout a session """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
