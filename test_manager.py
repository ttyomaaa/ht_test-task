import pytest
import json
import os
from random import randrange


from tasks import TaskManager


@pytest.fixture
def task_manager():
    file_path = 'test_tasks.json'
    empty_data = []
    with open(file_path, 'w') as json_file:
        json.dump(empty_data, json_file)
    manager = TaskManager(file_path)
    yield manager
    os.remove(file_path)


def test_create_task(task_manager):
    tasks_number = randrange(1, 10)
    for i in range(tasks_number):
        task_manager.create_task(title="title1",
                                 description="description1",
                                 category="category1",
                                 due_date="2000-01-01",
                                 priority="низкий")
    assert len(task_manager.tasks) == tasks_number
    assert task_manager.max_id == tasks_number


def test_edit_task(task_manager):
    new_title = "edit"
    task = task_manager.create_task(title="title1",
                             description="description1",
                             category="category1",
                             due_date="2000-01-01",
                             priority="низкий")
    target_id = task.id
    task_manager.edit_task(target_id, title=new_title, do_complete=False)
    assert task_manager.tasks[target_id-1].title == new_title

    task_manager.edit_task(target_id, title=new_title, do_complete=True)
    assert task_manager.tasks[target_id - 1].status == "Выполнена"


def test_delete_task(task_manager):
    task = task_manager.create_task(title="title1",
                                    description="description1",
                                    category="category1",
                                    due_date="2000-01-01",
                                    priority="низкий")
    task_manager.delete_task(task.id, category=None)
    assert len(task_manager.tasks) == 0

    task = task_manager.create_task(title="title1",
                                    description="description1",
                                    category="category1",
                                    due_date="2000-01-01",
                                    priority="низкий")
    task_manager.delete_task(task_id=None, category=task.category)
    assert len(task_manager.tasks) == 0

    task = task_manager.create_task(title="title1",
                                    description="description1",
                                    category="category1",
                                    due_date="2000-01-01",
                                    priority="низкий")

    task_manager.delete_task(task_id=999, category="unrelevant")
    assert len(task_manager.tasks) == 1


def test_search_task(task_manager):
    task1 = task_manager.create_task(title="title1",
                                     description="description1",
                                     category="category",
                                     due_date="2000-01-01",
                                     priority="низкий")

    task2 = task_manager.create_task(title="title2",
                                     description="description2",
                                     category="category",
                                     due_date="2000-01-01",
                                     priority="низкий")

    task3 = task_manager.create_task(title="title3",
                                     description="description2",
                                     category="anothercategory",
                                     due_date="2000-01-01",
                                     priority="низкий")

    results = task_manager.search_tasks(category="category")
    assert len(results) == 2
    assert results[0].category == "category"
    assert results[1].category == "category"

    results = task_manager.search_tasks(title="title1", category="category")
    assert len(results) == 1
    assert results[0].title == task1.title

    results = task_manager.search_tasks(title="anothertitle", category="anothercategory")
    assert len(results) == 0

    results = task_manager.search_tasks(status="Не выполнена")
    assert len(results) == 3

    results = task_manager.search_tasks()
    assert len(results) == 0


def test_view_task(task_manager):
    task1 = task_manager.create_task(title="title1",
                                     description="description1",
                                     category="category",
                                     due_date="2000-01-01",
                                     priority="низкий")

    task2 = task_manager.create_task(title="title2",
                                     description="description2",
                                     category="category",
                                     due_date="2000-01-01",
                                     priority="низкий")

    task3 = task_manager.create_task(title="title3",
                                     description="description2",
                                     category="anothercategory",
                                     due_date="2000-01-01",
                                     priority="низкий")

    results = task_manager.view_tasks(category="category")
    assert len(results) == 2

    results = task_manager.view_tasks(category=None)
    assert len(results) == 3


def test_load_task(task_manager):
    task_data = [
        {"id": 1, "title": "title1", "description": "description1", "category": "test1", "due_date": "2001-10-10", "priority": "1", "status": "Выполнена"},
        {"id": 5, "title": "title2", "description": "description2", "category": "test2", "due_date": "2002-10-10", "priority": "2", "status": "Не выполнена"}
    ]
    with open(task_manager.path, 'w') as file:
        json.dump(task_data, file, indent=4)
    task_manager.load_tasks()
    assert len(task_manager.tasks) == 2
    assert task_manager.tasks[0].id == task_data[0]["id"]
    assert task_manager.tasks[1].id == task_data[1]["id"]
    assert task_manager.max_id == task_data[1]["id"]


def test_save_task(task_manager):
    tasks_number = randrange(1, 10)
    for i in range(tasks_number):
        task_manager.create_task(title="title1",
                                 description="description1",
                                 category="category1",
                                 due_date="2000-01-01",
                                 priority="низкий")
    with open(task_manager.path, 'r') as file:
        data = json.load(file)
    assert len(data) == tasks_number
    assert data[0]['id'] == task_manager.tasks[0].id
