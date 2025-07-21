from unittest.mock import MagicMock, AsyncMock

import pytest

from task_manager.tasks.models import Task
from task_manager.tasks.schemas import TaskRead
from task_manager.core.tests.conftest import current_user, async_client
from task_manager.tasks.tests.factories import TaskFactory


@pytest.fixture
def task():
    return TaskFactory()


@pytest.fixture
def task_read():
    return TaskRead(id=1, name="Test Task")

@pytest.fixture
def interactor_mock(task):
    interactor = MagicMock()
    interactor.get_by_id = AsyncMock(return_value=task)
    interactor.update = AsyncMock(return_value=task)
    interactor.get_one = AsyncMock(return_value=task)
    return interactor