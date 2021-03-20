from datetime import date, timedelta
from tests.test_base import app, client, login
from tests.assertutil import assert_unauthorized, assert_redirect_login


def test_index(client):
    response = client.get("/")
    assert_redirect_login(response)

    login(client)
    response = client.get("/")
    assert response.status_code == 200
    assert b"Search" in response.data


def test_api_groups(client):
    response = client.get("/api/groups")
    assert_unauthorized(response)

    login(client)
    response = client.get("/api/groups")
    assert response.json == ["base", "demo"]


def test_api_scripts(client):
    response = client.get("/api/scripts")
    assert_unauthorized(response)

    login(client)
    response = client.get("/api/scripts")
    attended_response = [
        {
            "description": "Change the password for the main user",
            "group": "base",
            "id": "pyscriptdeck.base.user.ChangePassword",
            "name": "Change main password",
            "params": [
                {
                    "default": "",
                    "id": "password",
                    "label": "New password",
                    "type": "password"
                },
                {
                    "default": "",
                    "id": "password_confirm",
                    "label": "Confirm password",
                    "type": "password"
                }
            ]
        },
        {
            "description": "Hello world for test",
            "group": "demo",
            "id": "pyscriptdemo.helloworld.HelloWorld",
            "name": "Hello world",
            "params": []
        }
    ]
    assert attended_response[0] in response.json
    assert attended_response[1] in response.json
