from extensions import db, bcrypt
from models import User
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    
    user = User.query.filter_by(email= data["email"]).first()
    if user:
        return jsonify({"error": "Email Already Exist"}), 409
    
    has_password = bcrypt.generate_password_hash(data["password"])

    add_user = User(name=data["name"], email=data["email"], password=has_password, role=data["role"])
    db.session.add(add_user)
    db.session.commit()
    return jsonify({"message": "Successfully Registered User"}), 201


@auth.route("/login", methods=["POST"])
def login():
    
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"Error": "User not found"}), 401
    if bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=str(user.id))
        return jsonify({"Token": token}), 200
    else:
        return jsonify({"Error": "Wrong Password"}), 401
