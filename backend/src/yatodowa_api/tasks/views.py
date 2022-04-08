from flask import Blueprint, jsonify
from yatodowa_api.models import ListsGroups, Tasks, TasksLists
from yatodowa_api.sqldb import get_db

db = get_db()

tasks_api = Blueprint("tasks_api", __name__)

COMMON_ENDPOINT = "/api/v1"


# groups
@tasks_api.route(COMMON_ENDPOINT + "/groups", methods=["GET"])
def get_groups():
    groups = ListsGroups.query.all()
    return jsonify([group.name for group in groups]), 200


@tasks_api.route(COMMON_ENDPOINT + "/addgroup")
def add_group():
    group = ListsGroups(name="group2")
    db.session.add(group)
    db.session.commit()
    return jsonify(group.name), 201


# Lists
@tasks_api.route(COMMON_ENDPOINT + "/lists", methods=["GET"])
def get_lists():
    tasks_lists = TasksLists.query.all()
    return jsonify([elt.to_dict() for elt in tasks_lists]), 200


@tasks_api.route(COMMON_ENDPOINT + "/add_list")
def add_list():
    tasks_list = TasksLists(name="list2")
    db.session.add(tasks_list)
    db.session.commit()
    return jsonify(tasks_list.name), 201


# Tasks
@tasks_api.route(COMMON_ENDPOINT + "/tasks", methods=["GET"])
def get_tasks():
    tasks = Tasks.query.all()
    return jsonify([elt.to_dict() for elt in tasks]), 200


@tasks_api.route(COMMON_ENDPOINT + "/add_task")
def add_task():
    task = Tasks(
        text="lorem ipsum somthing somewhere haha", completed=False, list_name="list5"
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.text), 201
