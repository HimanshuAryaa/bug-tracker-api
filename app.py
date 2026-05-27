from flask import Flask
from flask_jwt_extended import JWTManager
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

@app.route("/")
def home():
    return "Bug Tracker API is running!"

with app.app_context():
    db.create_all()
    print("Tables created!")

if __name__ == "__main__":
    app.run(debug=True)