import pytest
from fastapi import HTTPException

from task_manager.tasks.application.controller import TaskController
from task_manager.tasks.schemas import TaskUpdate
from task_manager.tasks.models import Task


@pytest.mark.asyncio
async def test_update_task_success(interactor_mock, current_user, task):
    controller = TaskController(crud_interactor=interactor_mock)
    update_schema = TaskUpdate(name="Updated Title")

    result = await controller.update(task_id=1, schema=update_schema, current_user=current_user)

    assert result == task
    interactor_mock.get_by_id.assert_called_once_with(1)
    interactor_mock.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_task_forbidden(interactor_mock, current_user):
    interactor_mock.get_by_id.return_value = Task(id=1, name="Test Task", user_id=999, created_by_id=999)

    controller = TaskController(crud_interactor=interactor_mock)
    update_schema = TaskUpdate(name="Updated Title")

    with pytest.raises(HTTPException) as exc_info:
        await controller.update(task_id=1, schema=update_schema, current_user=current_user)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_by_id_success(interactor_mock, current_user, task):
    controller = TaskController(crud_interactor=interactor_mock)

    result = await controller.get_by_id(task_id=1, current_user=current_user)

    assert result == task
    interactor_mock.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_by_id_forbidden(interactor_mock, current_user):
    interactor_mock.get_by_id.return_value = Task(id=1, name="Test Task", user_id=2, created_by_id=2)

    controller = TaskController(crud_interactor=interactor_mock)

    with pytest.raises(HTTPException) as exc_info:
        await controller.get_by_id(task_id=1, current_user=current_user)

    assert exc_info.value.status_code == 404
