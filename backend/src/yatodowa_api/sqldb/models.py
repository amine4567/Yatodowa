import uuid

import yatodowa_api.sqldb.consts as sqldb_consts
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from yatodowa_api.sqldb.core import get_db

db: SQLAlchemy = get_db()


class GroupTable(db.Model):
    __tablename__ = "groups"
    group_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(sqldb_consts.GROUP_NAME_MAX_LEN), unique=True)


class CollectionTable(db.Model):
    __tablename__ = "collections"
    collection_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(sqldb_consts.COLLECTION_NAME_MAX_LEN), unique=True)
    group_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("groups.group_id"), nullable=True
    )

    def to_dict(self):
        return {
            "collection_id": self.collection_id,
            "name": self.name,
            "group_id": self.group_id,
        }


class TaskTable(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.String(sqldb_consts.TASK_TEXT_MAX_LEN))
    completed = db.Column(db.Boolean, default=False)
    collection_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("collections.collection_id"), nullable=False
    )

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "text": self.text,
            "completed": self.completed,
            "collection_id": self.collection_id,
        }
