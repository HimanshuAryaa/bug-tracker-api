from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Project, Bug

bug = Blueprint("bug", __name__)

report_roles = ["admin", "tester"]
update_roles = ["admin", "tester", "developer"]

@bug.route("/bugs", methods=["POST"])
@jwt_required()
def add_bug():
    user_id= get_jwt_identity()
    user= User.query.get(user_id)
    if user.role not in report_roles:
      return jsonify({"Error": "Permission Denied"}), 403
    data= request.json
    project = Project.query.get(data["project_id"])
    if not project:
      return jsonify({"Error": "Project not found"}), 404
    if user.role != "admin":
      if user.role == "tester" and project.tester_id != int(user_id):
        return jsonify({"error": "You are not assigned to this project"}), 403
    
    bug = Bug(title=data["title"], 
              description=data["description"],
              severity=data["severity"], 
              priority=data["priority"],
              status="Open", 
              project_id=project.id, 
              reporter_id=user_id,
              assignee_id=project.developer_id)
    db.session.add(bug)
    db.session.commit()
    return jsonify(bug.to_dict()), 201

@bug.route("/bugs", methods=["GET"])
@jwt_required()
def get_bugs():
  bugs = Bug.query.all()
  bug = [bug.to_dict() for bug in bugs]
  return jsonify(bug)

@bug.route("/bugs/<int:id>", methods=["GET"])
@jwt_required()
def get_bugs_specific(id):
  bug = Bug.query.get(id)
  if not bug:
    return jsonify({"Error": "Bug not found"}), 404
  return jsonify(bug.to_dict())

@bug.route("/bugs/<int:id>", methods=["PUT"])
@jwt_required()
def update_bug(id):
  user_id=get_jwt_identity()
  user = User.query.get(user_id)
  if user.role not in update_roles:
    return jsonify({"Error": "Permission Denied"}), 403
  data = request.json
  bug= Bug.query.get(id)
  if not bug:
    return jsonify({"Error": "Bug not found"}), 404
  project = Project.query.get(bug.project_id)
  if user.role != "admin":
    if user.role == "developer" and project.developer_id != int(user_id):
      return jsonify({"error": "You are not assigned to this project"}), 403
    if user.role == "tester" and project.tester_id != int(user_id):
      return jsonify({"error": "You are not assigned to this project"}), 403
  bug.status = data.get("status", bug.status)
  db.session.commit()
  return jsonify(bug.to_dict()), 200

@bug.route("/bugs/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_bug(id):
  user_id=get_jwt_identity()
  user=User.query.get(user_id)
  if user.role != "admin":
    return jsonify({"Error": "Permission Denied"}), 403
  bug=Bug.query.get(id)
  if not bug:
    return jsonify({"Error": "Bug not found"}), 404
  db.session.delete(bug)
  db.session.commit()
  return jsonify({"Success": "Bug Deleted Successfully"}), 200