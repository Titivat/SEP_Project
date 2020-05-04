from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_raw_jwt
)
from .. import app, db
from server.controller import document as controller
from server.model import user, document
from sqlalchemy.exc import IntegrityError

@app.route('/document', methods=['POST'])
@jwt_required
def create():
    try:
        name = request.json.get('name', None)
        user = get_jwt_identity()
        if not name:
            return jsonify({"msg": "missing name",
                "success": False}), 400
        controller.create_document(name, user)
        return jsonify({"success": True})
    except IntegrityError as e:
        return jsonify({"msg": "Integrity constraint failed",
            "success": False}), 400
    except Exception as e:
        return jsonify({"msg": str(e),
            "success": False}), 400
