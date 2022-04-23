from typing import List
from uuid import UUID

from yatodowa_api.models import Task
from yatodowa_api.sqldb import get_session


def add_task(text: str, collection_name: str) -> Task:
    # TODO: handle the case where collection_name foreign key constraint is violated
    with get_session() as session:
        task = Task(text=text, collection_name=collection_name)
        session.add(task)
        return task


def get_tasks() -> List[Task]:
    with get_session():
        tasks = Task.query.all()
        return tasks


def delete_task(task_id: UUID):
    with get_session():
        results = Task.query.filter(Task.task_id == task_id)
        if len(results.all()) == 0:
            raise ValueError(
                f"No task with task_id={task_id} exists in the database. "
                "Nothing to delete."
            )
        results.delete()
