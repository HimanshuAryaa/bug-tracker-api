from datetime import datetime, timezone
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }


class Project(db.Model):
    __tablename__ = "project"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tester_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "manager_id": self.manager_id,
            "tester_id": self.tester_id,
            "developer_id": self.developer_id
            }


class Bug(db.Model):
    __tablename__ = "bug"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "priority": self.priority,
            "status": self.status,
            "project_id": self.project_id,
            "reporter_id": self.reporter_id,
            "assignee_id": self.assignee_id,
            "created_at": self.created_at.isoformat()
        }