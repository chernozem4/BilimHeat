

import pytest
from typing import AsyncGenerator

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db
from models import Base
from models.user import User
from core.security import hash_password

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/test_db"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionTest = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Переопределённая зависимость get_db для использования тестовой базы.
    """
    async with AsyncSessionTest() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Создаёт и удаляет таблицы в тестовой базе, предоставляет клиент для тестов.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
async def test_user() -> AsyncGenerator[User, None]:
    """
    Создаёт тестового пользователя в базе.
    """
    async with AsyncSessionTest() as session:
        hashed_pwd = hash_password("testpassword")
        user = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password=hashed_pwd,
            is_active=True,
            role="user"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        yield user
        await session.delete(user)
        await session.commit()


@pytest.mark.asyncio
async def test_login_and_access(async_client: AsyncClient, test_user: User) -> None:
    """
    Тест логина и доступа к защищённому эндпоинту.
    """
    response = await async_client.post(
        "/api/auth/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data

    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get("/api/schools/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_access_without_token(async_client: AsyncClient) -> None:
    """
    Тест доступа к защищённому эндпоинту без токена (должен быть отказ).
    """
    response = await async_client.get("/api/schools/")
    assert response.status_code == 401
