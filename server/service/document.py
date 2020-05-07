from flask import Flask, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from .. import app, db
from server.controller.document import DocumentController
from server.model import user, document
from sqlalchemy.exc import IntegrityError

controller = DocumentController(db)

@app.route('/document', methods=['POST'])
@jwt_required
def createDocument():
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

@app.route('/document/<id>', methods=['DELETE', 'PUT'])
@jwt_required
def modifyDocument(id):
    if not id:
        return jsonify({"msg": "missing id",
            "success": False}), 400
    if request.method == 'DELETE':
        try:
            user = get_jwt_identity()
            controller.remove_document(id, user)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"msg": str(e),
                "success": False}), 400
    else:
        try:
            name = request.json.get('name', None)
            user = get_jwt_identity()
            if not name:
                return jsonify({"msg": "missing name",
                    "success": False}), 400
            controller.rename_document(id, user, name)
            return jsonify({"success": True})
        except IntegrityError as e:
            return jsonify({"msg": "Integrity constraint failed",
                "success": False}), 400
        except Exception as e:
            return jsonify({"msg": str(e),
                "success": False}), 400

@app.route('/documents', methods=['GET'])
@jwt_required
def retrieveDocuments():
    try:
        owner = get_jwt_identity()
        docs = controller.get_documents(owner)
        return jsonify({"documents": docs, "success": True})
    except Exception as e:
        return jsonify({"msg": str(e),
            "success": False}), 400
