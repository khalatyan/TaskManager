import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport

from task_manager.core.dependencies import get_current_user
from task_manager.core.schemas import UserRead
from task_manager.main import app


@pytest.fixture
def current_user():
    return UserRead(id=1, username="test_user", email="test@example.com")


def override_get_current_user():
    return UserRead(id=1, email="test@example.com")

@pytest_asyncio.fixture
async def async_client():
    app.dependency_overrides[get_current_user] = override_get_current_user
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client