from uuid import UUID

import sqlalchemy
from yatodowa_api.components.collections.exceptions import CollectionNotFoundError
from yatodowa_api.components.collections.service import get_collection
from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import TaskTable

from .exceptions import TaskNotFoundError
from .schemas import (
    MultiTasksRespModel,
    TaskGetQueryArgsModel,
    TaskPostQueryBodyModel,
    TaskRespModel,
)


def add_task(task_query: TaskPostQueryBodyModel) -> TaskRespModel:
    try:
        with get_session() as session:
            task = TaskTable(
                text=task_query.text, collection_id=task_query.collection_id
            )
            session.add(task)

        task_response = TaskRespModel(**task.to_dict())
        return task_response
    except sqlalchemy.exc.IntegrityError:
        raise CollectionNotFoundError(
            "Foreign key violation: There is no collection with the id "
            + str(task_query.collection_id)
        )


def get_tasks(request_args: TaskGetQueryArgsModel) -> MultiTasksRespModel:
    with get_session() as session:
        query: sqlalchemy.sql.Select = sqlalchemy.select(TaskTable)

        if request_args.collection_id is not None:
            query = query.where(TaskTable.collection_id == request_args.collection_id)

        total_count = session.execute(
            sqlalchemy.select(sqlalchemy.func.count()).select_from(query)
        ).scalar_one()

        if total_count == 0:
            get_collection(request_args.collection_id)
            tasks: list[TaskTable] = list()
        else:
            query = query.limit(request_args.page_size).offset(request_args.skip)

            tasks = session.execute(query).scalars().all()

    tasks_response = MultiTasksRespModel(
        tasks=[TaskRespModel.from_orm(task) for task in tasks],
        total_count=total_count,
        skip=request_args.skip,
        page_size=request_args.page_size,
    )
    return tasks_response


def delete_task(task_id: UUID) -> TaskRespModel:
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

        return TaskRespModel(**query_results[0].to_dict())
