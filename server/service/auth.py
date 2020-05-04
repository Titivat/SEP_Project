from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token
)
from .. import app, db
from server.model import user
from server.controller import auth as controller

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
