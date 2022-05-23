import logging
from uuid import UUID

import sqlalchemy
from yatodowa_api.components.collections.service import check_if_collection_exists
from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import TaskTable

from .exceptions import TaskNotFoundError
from .schemas import (
    MultiTasksRespModel,
    TaskPostQueryBodyModel,
    TaskPutQueryBodyModel,
    TaskRespModel,
)

logger = logging.getLogger(__name__)


def add_task(request_body: TaskPostQueryBodyModel) -> TaskRespModel:
    try:
        with get_session() as session:
            task = TaskTable(
                text=request_body.text, collection_id=request_body.collection_id
            )
            session.add(task)

        task_response = TaskRespModel.from_orm(task)
        return task_response
    except sqlalchemy.exc.IntegrityError as integrity_error:
        check_if_collection_exists(request_body.collection_id)

        # If no other exception is thrown
        logger.error("Unhandled exception")
        raise integrity_error


def get_tasks(
    page_size: int, skip: int, collection_id: UUID = None
) -> MultiTasksRespModel:
    with get_session() as session:
        stmt: sqlalchemy.sql.Select = sqlalchemy.select(TaskTable)

        if collection_id is not None:
            stmt = stmt.where(TaskTable.collection_id == collection_id)

        total_count = session.execute(
            sqlalchemy.select(sqlalchemy.func.count()).select_from(stmt)
        ).scalar_one()

        if total_count == 0:
            if collection_id is not None:
                check_if_collection_exists(collection_id)
            tasks: list[TaskTable] = list()
        else:
            stmt = stmt.limit(page_size).offset(skip)

            tasks = session.execute(stmt).scalars().all()

    tasks_response = MultiTasksRespModel(
        tasks=[TaskRespModel.from_orm(task) for task in tasks],
        total_count=total_count,
        skip=skip,
        page_size=page_size,
    )
    return tasks_response


def delete_task(task_id: UUID) -> TaskRespModel:
    with get_session() as session:
        task_to_delete: TaskTable = session.get(TaskTable, task_id)
        if task_to_delete is None:
            raise TaskNotFoundError(
                f"No task with task_id={task_id} exists in the database. "
                "Nothing to delete."
            )

        session.delete(task_to_delete)

    return TaskRespModel.from_orm(task_to_delete)


def update_task(task_id: UUID, request_body: TaskPutQueryBodyModel):
    try:
        with get_session() as session:
            task_to_update: TaskTable = session.get(TaskTable, task_id)
            if task_to_update is None:
                raise TaskNotFoundError(
                    f"No task with task_id={task_id} exists in the database. "
                    "Nothing to update."
                )

            if request_body.text is not None:
                task_to_update.text = request_body.text

            if request_body.completed is not None:
                task_to_update.completed = request_body.completed

            if request_body.collection_id is not None:
                task_to_update.collection_id = request_body.collection_id
    except sqlalchemy.exc.IntegrityError as integrity_error:
        check_if_collection_exists(request_body.collection_id)

        # If no other exception is thrown
        logger.error("Unhandled exception")
        raise integrity_error

    return TaskRespModel.from_orm(task_to_update)
