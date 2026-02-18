# backend\app\test\conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.main import app
from app.core.config import settings
from app import dependencies

@pytest.fixture(scope="session")
def engine():
    return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[dependencies.get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

# --- Import and Register Factory Fixtures ---

from app.test.fixtures.factory import (
    user_factory,
    device_factory,
)

# --- Composite Test Data Fixtures ---

from app.test.fixtures.fixtures import (
    mock_multiple_users,
    mock_devices,
)
