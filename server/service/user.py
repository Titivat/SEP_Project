from flask import Flask, jsonify, request
from .. import app, db
from server.model import user
from server.controller import user as controller
from sqlalchemy.exc import IntegrityError

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
