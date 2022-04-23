from typing import List
from uuid import UUID

from yatodowa_api.models import Tasks
from yatodowa_api.sqldb import get_session


def add_task(text: str, list_name: str) -> Tasks:
    # TODO: handle the case where list_name foreign key constraint is violated
    with get_session() as session:
        task = Tasks(text=text, list_name=list_name)
        session.add(task)
        return task


def get_tasks() -> List[Tasks]:
    with get_session():
        tasks = Tasks.query.all()
        return tasks


def delete_task(task_id: UUID):
    with get_session():
        results = Tasks.query.filter(Tasks.task_id == task_id)
        if len(results.all()) == 0:
            raise ValueError(
                f"No task with task_id={task_id} exists in the database. "
                "Nothing to delete."
            )
        results.delete()
