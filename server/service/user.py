from flask import Flask, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from .. import app, db
from server.model import user
from server.controller.user import UserController
from sqlalchemy.exc import IntegrityError

controller = UserController(db)

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return jsonify({"msg": "missing username",
                "success": False}), 400
        if not password:
            return jsonify({"msg": "missing password",
                "success": False}), 400
        controller.create_user(username, password)
        return jsonify({"success": True})
    except IntegrityError as e:
        return jsonify({"msg": "Integrity constraint failed",
            "success": False}), 400
    except Exception as e:
        return jsonify({"msg": str(e),
            "success": False}), 400

@app.route('/users', methods=['GET'])
@jwt_required
def retrieveUsers():
    try:
        users = controller.get_users()
        return jsonify({"users": users,"success": True})
    except Exception as e:
        return jsonify({"msg": str(e),
            "success": False}), 400
