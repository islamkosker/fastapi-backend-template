#backend/app/test/fixtures/fixtures.py

import pytest

from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, scoped_session

from app.main import app
from app.core.config import settings

from app.test.fixtures.factory import device_factory ,user_factory


@pytest.fixture
def mock_devices(db_session, request, device_factory):
    device_count = getattr(request, "param", 1)
    devices = device_factory.create_batch(device_count)
    db_session.commit()
    return devices


@pytest.fixture
def mock_multiple_users(db_session, user_factory, request):
    """
    Creates N users and returns the list.
    Use with: @pytest.mark.parametrize("multiple_users", [3], indirect=True)
    """
    user_count = getattr(request, "param", 2)
    users = user_factory.create_batch(user_count)
    db_session.commit()
    return users