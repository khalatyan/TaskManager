from datetime import datetime

import pytest
from httpx import AsyncClient

from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskCreate, TaskUpdate
from task_manager.core.schemas import UserRead

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient, mocker):
    mock_create_task = {"name": "Test Task", "description": "desc"}

    # Мокаем Depends(get_current_user)
    mocker.patch("task_manager.tasks.routers.get_task_controller").return_value.create = mocker.AsyncMock(return_value={
        "id": 1, "name": "Test Task", "description": "desc", "created_by_id": 1
    })

    response = await async_client.post("/tasks/", json=mock_create_task)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Task"


@pytest.mark.asyncio
async def test_get_tasks(async_client: AsyncClient, mocker):
    mock_controller = mocker.Mock()
    mock_controller.filter = mocker.AsyncMock(return_value=[{"id": 1, "name": "Task", "created_by_id": 2}])
    mocker.patch("task_manager.tasks.routers.get_task_controller", return_value=mock_controller)

    response = await async_client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_task_by_id(async_client: AsyncClient, mocker, task: Task):
    # mock_task = {"id": 42, "name": "My Task", "created_by_id": 3, "created_at": datetime.now()}

    mock_controller = mocker.Mock()
    mocker.patch("task_manager.tasks.routers.get_task_controller", return_value=mock_controller)

    response = await async_client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    assert response.json()["id"] == task.id


@pytest.mark.asyncio
async def test_update_task(async_client: AsyncClient, mocker):
    mock_user = UserRead(id=4, email="update@test.com", is_active=True)
    update_data = {"name": "Updated Task"}
    updated_task = {"id": 99, "name": "Updated Task", "created_by_id": 4}

    mocker.patch("task_manager.tasks.routers.get_current_user", return_value=mock_user)
    mock_controller = mocker.Mock()
    mock_controller.update = mocker.AsyncMock(return_value=updated_task)
    mocker.patch("task_manager.tasks.routers.get_task_controller", return_value=mock_controller)

    response = await async_client.patch("/tasks/99", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Task"
