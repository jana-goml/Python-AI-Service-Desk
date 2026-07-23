from unittest.mock import AsyncMock
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.deps import get_db

@pytest_asyncio.fixture
async def db_session():
    session = AsyncMock()
    yield session

@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()