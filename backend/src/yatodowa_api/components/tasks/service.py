from typing import List
from uuid import UUID

import sqlalchemy
from yatodowa_api.components.collections.exceptions import CollectionNotFoundError
from yatodowa_api.components.tasks.exceptions import TaskNotFoundError
from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import Task

from .schemas import TaskQuery


def add_task(task_query: TaskQuery) -> Task:
    try:
        with get_session() as session:
            task = Task(text=task_query.text, collection_id=task_query.collection_id)
            session.add(task)
            return task
    except sqlalchemy.exc.IntegrityError:
        raise CollectionNotFoundError(
            "Foreign key violation: There is no collection with the id "
            + str(task_query.collection_id)
        )


def get_tasks() -> List[Task]:
    with get_session():
        tasks = Task.query.all()
        return tasks


def delete_task(task_id: UUID) -> Task:
    with get_session():
        query = Task.query.filter(Task.task_id == task_id)

        query_results = query.all()
        if len(query_results) == 0:
            raise TaskNotFoundError(
                f"No task with task_id={task_id} exists in the database. "
                "Nothing to delete."
            )

        delete_results = query.delete()
        assert delete_results == 1

        return query_results[0]
