import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from yatodowa_api.sqldb import get_db

db: SQLAlchemy = get_db()


class Group(db.Model):
    __tablename__ = "groups"
    group_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(20), unique=True)


class Collection(db.Model):
    __tablename__ = "collections"
    collection_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(20), unique=True)
    group_name = db.Column(db.String(20), db.ForeignKey("groups.name"), nullable=True)

    def to_dict(self):
        return {
            "collection_id": self.collection_id,
            "name": self.name,
            "group_name": self.group_name,
        }


class Task(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    collection_name = db.Column(
        db.String(20), db.ForeignKey("collections.name"), nullable=False
    )

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "text": self.text,
            "completed": self.completed,
            "collection_name": self.collection_name,
        }
