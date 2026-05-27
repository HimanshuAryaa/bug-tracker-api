from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from extensions import db, bcrypt
from models import User, Project, Bug
from routes.auth import auth
from routes.projects import project
from routes.bugs import bug

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bugtracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(project)
app.register_blueprint(bug)
bcrypt.init_app(app)

@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    from models import User
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())

with app.app_context():
    db.create_all()
    print("Tables created!")

if __name__ == "__main__":
    app.run(debug=True)