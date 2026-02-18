#backend/app/test/fixtures/factory.py

import pytest
from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import Sequence, SubFactory, SelfAttribute
import factory

from app.core.security import get_password_hash

from app.test.utils.utils import random_email, random_serial_number
from app import models

@pytest.fixture
def user_factory(db_session):
    class _UserFactory(SQLAlchemyModelFactory):
        class Meta:
            model = models.sql.User
            sqlalchemy_session = db_session
            sqlalchemy_session_persistence = "commit"

        email = random_email
        full_name = Sequence(lambda n: f"Test User {n}")
        hashed_password = get_password_hash("testuser")
        is_active = True
        is_superuser = False

    return _UserFactory


@pytest.fixture
def device_factory(db_session):
    class _DeviceFactory(SQLAlchemyModelFactory):
        class Meta:
            model = models.sql.Device
            sqlalchemy_session = db_session
            sqlalchemy_session_persistence = "commit"

        name = Sequence(lambda n: f"device{n}")
        model = "Test-model"
        serial_number = random_serial_number  

    return _DeviceFactory

