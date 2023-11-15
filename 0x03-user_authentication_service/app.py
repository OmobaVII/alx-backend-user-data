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


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """ responds to get /profile route """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """ generate token and respond with the reset_token """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    msg = {"email": email, "reset_token": reset_token}
    return jsonify(msg), 200


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """ updates the users password """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    msg = {"email": email, "message": "Password updated"}
    return jsonify(msg), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
