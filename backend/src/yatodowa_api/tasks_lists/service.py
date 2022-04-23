from typing import List

from yatodowa_api.models import TasksLists
from yatodowa_api.sqldb import get_session


def get_lists() -> List[TasksLists]:
    with get_session():
        tasks_lists = TasksLists.query.all()
        return tasks_lists


def add_list(list_name: str, group_name: str = None) -> TasksLists:
    with get_session() as session:
        new_tasks_list = TasksLists(list_name=list_name, group_name=group_name)
        session.add(new_tasks_list)
        return new_tasks_list
