import random
import string

from factory.declarations import LazyFunction
from fastapi.testclient import TestClient

from app.core.config import settings
from app import schemas 



def get_random_email() -> str:
    """Generate a random email address with a random 12-character local part."""
    _ = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{_}@test.com"

def get_random_str() -> str:
    """Generate a random email address with a random 12-character local part."""
    _ = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return _

def get_test_token_by_user(client: TestClient, user_email:str, user_password:str) -> dict[str, str]:
    login_data = {
        "username": user_email,
        "password": user_password,
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

def get_admin_token(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER_USERNAME,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

random_serial_number = LazyFunction(get_random_str)
random_email = LazyFunction(get_random_email)

