from flask_sqlalchemy import SQLAlchemy

from yatodowa_api.sqldb import get_db

db: SQLAlchemy = get_db()


class ListsGroups(db.Model):
    __tablename__ = "lists_groups"

    name = db.Column(db.String(20), primary_key=True)


class TasksLists(db.Model):
    __tablename__ = "tasks_lists"

    name = db.Column(db.String(20), primary_key=True)
    group_name = db.Column(db.String(20), db.ForeignKey("lists_groups.name"))

    def to_dict(self):
        return {"name": self.name, "group_name": self.group_name}


class Tasks(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    list_name = db.Column(
        db.String(20), db.ForeignKey("tasks_lists.name"), nullable=False
    )

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "text": self.text,
            "completed": self.completed,
            "list_name": self.list_name,
        }
