from uuid import UUID

import sqlalchemy
from yatodowa_api.components.collections.exceptions import CollectionNotFoundError
from yatodowa_api.components.tasks.exceptions import TaskNotFoundError
from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import TaskTable

from .schemas import TaskQueryBody, TaskResponse


def add_task(task_query: TaskQueryBody) -> TaskResponse:
    try:
        with get_session() as session:
            task = TaskTable(
                text=task_query.text, collection_id=task_query.collection_id
            )
            session.add(task)

        task_response = TaskResponse(**task.to_dict())
        return task_response
    except sqlalchemy.exc.IntegrityError:
        raise CollectionNotFoundError(
            "Foreign key violation: There is no collection with the id "
            + str(task_query.collection_id)
        )


def get_tasks() -> list[TaskResponse]:
    with get_session():
        tasks = TaskTable.query.all()

    tasks_response = [TaskResponse(**task.to_dict()) for task in tasks]
    return tasks_response


def delete_task(task_id: UUID) -> TaskResponse:
    with get_session():
        query = TaskTable.query.filter(TaskTable.task_id == task_id)

        query_results = query.all()
        if len(query_results) == 0:
            raise TaskNotFoundError(
                f"No task with task_id={task_id} exists in the database. "
                "Nothing to delete."
            )

        delete_results = query.delete()
        assert delete_results == 1  # TODO

        return TaskResponse(**query_results[0].to_dict())
