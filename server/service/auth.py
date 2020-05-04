from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_raw_jwt
)
from .. import app, db, jwt
from server.model import user
from server.controller import auth as controller

blacklist = set()

@jwt.token_in_blacklist_loader
def token_in_blacklist(token):
    jti = token['jti']
    return jti in blacklist

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return jsonify({"msg": "missing username",
                "success": False}), 400
        if not password:
            return jsonify({"msg": "missing password",
                "success": False}), 400
        if not controller.validate_credentials(username, password):
            return jsonify({"msg": "incorrect username or password",
                "success": False}), 400
        access_token = create_access_token(username)
        return jsonify({"token": access_token, "success": True})
    except Exception as e:
        return jsonify({"msg": str(e),
            "success": False}), 400

@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"success": True})
