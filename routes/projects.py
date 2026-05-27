from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Project

role = ["admin", "manager"]

project = Blueprint("project", __name__)

@project.route("/projects", methods=["POST"])
@jwt_required()
def add_project():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role not in role:
        return jsonify({"error": "Permission Denied"}), 403
    
    data = request.json

    existing = Project.query.filter_by(name=data["name"]).first()
    if existing:
        return jsonify({"error": "Project name already exists"}), 409

    project = Project(name=data["name"], description=data["description"], 
                      manager_id=user_id, tester_id=data["tester_id"], developer_id=data["developer_id"])
    
    db.session.add(project)
    db.session.commit()

    return jsonify(project.to_dict()), 201

@project.route("/projects", methods=["GET"])
@jwt_required()
def get_project():
    projects = Project.query.all()
    project = [project.to_dict() for project in projects]
    return jsonify(project)

@project.route("/projects/<int:id>", methods=["GET"])
@jwt_required()
def specific_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"Error": "No Project Found"}), 404
    return jsonify(project.to_dict()), 201

@project.route("/projects/<int:id>", methods=["PUT"])
@jwt_required()
def update_project(id):
    user_id = get_jwt_identity()
    user= User.query.get(user_id)
    if user.role not in role:
        return jsonify({"Error": "Permission Denied"}), 403
    data = request.json
    project = Project.query.get(id)
    if not project:
        return jsonify({"Error": "Project not found"}), 404

    project.name = data.get("name", project.name)
    project.description = data.get("description", project.description)
    project.tester_id = data.get("tester_id", project.tester_id)
    project.developer_id = data.get("developer_id", project.developer_id)
    db.session.commit()
    return jsonify(project.to_dict()), 200

@project.route("/projects/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_project(id):
    user_id=get_jwt_identity()
    user= User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"Error": "Permission Denied"}), 403
    project = Project.query.get(id)
    if not project:
        return jsonify({"Error": "Project not found"}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({"Success": "Project deleted successfully"}), 200