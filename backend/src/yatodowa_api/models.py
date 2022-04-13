import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from yatodowa_api.sqldb import get_db

db: SQLAlchemy = get_db()


class ListsGroups(db.Model):
    __tablename__ = "lists_groups"
    group_name = db.Column(db.String(20), primary_key=True)


class TasksLists(db.Model):
    __tablename__ = "tasks_lists"
    list_name = db.Column(db.String(20), primary_key=True)
    group_name = db.Column(
        db.String(20), db.ForeignKey("lists_groups.group_name"), nullable=True
    )

    def to_dict(self):
        return {
            "list_name": self.list_name,
            "group_name": self.group_name,
        }


class Tasks(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    list_name = db.Column(
        db.String(20), db.ForeignKey("tasks_lists.list_name"), nullable=False
    )

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "text": self.text,
            "completed": self.completed,
            "list_name": self.list_name,
        }
