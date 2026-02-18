import pytest
from app.core.config import settings
from app.test.utils.utils import get_test_token_by_user, get_admin_token,get_random_str
from app import schemas


"""Test api/v1/devices/"""


@pytest.mark.parametrize("mock_devices", [1, 3, 5], indirect=True)
def test_get_devices(client, mock_devices):
    devices = mock_devices
    headers = get_admin_token(client=client)
    response = client.get(f"{settings.API_V1_STR}/devices/", headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == len(devices)

@pytest.mark.parametrize("mock_multiple_users", [1, 3, 5], indirect=True)
def test_create_devices(client, mock_multiple_users):
    """Each user should be able to create one device via POST /devices/"""
    for user in mock_multiple_users:
        headers = get_test_token_by_user(client, user.email, "testuser")

        data = schemas.sql.DeviceCreate(
            name="test-device",
            serial_number=get_random_str(),
            model=get_random_str()
        )

        response = client.post(
            f"{settings.API_V1_STR}/devices/",
            headers=headers,
            json=data.model_dump() 
        )

        assert response.status_code == 201, response.text
        response_data = response.json()

        assert isinstance(response_data, dict)

        assert response_data["serial_number"] == data.serial_number
        assert response_data["name"] == data.name
        assert response_data["model"] == data.model
