from typing import List
from uuid import UUID

import sqlalchemy
from yatodowa_api.collections.exceptions import CollectionNotFoundError
from yatodowa_api.models import Task
from yatodowa_api.sqldb import get_session
from yatodowa_api.tasks.exceptions import TaskNotFoundError


def add_task(text: str, collection_name: str) -> Task:
    try:
        with get_session() as session:
            task = Task(text=text, collection_name=collection_name)
            session.add(task)
            return task
    except sqlalchemy.exc.IntegrityError:
        raise CollectionNotFoundError(
            "Foreign key violation: There is no collection with the name "
            + collection_name
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
