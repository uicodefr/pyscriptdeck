from tests.test_base import app, client, login
from tests.assertutil import assert_unauthorized, assert_redirect_login


_SCRIPT_ID = "pyscriptdemo.helloworld.HelloWorld"


def test_script(client):
    response = client.get("/script/" + _SCRIPT_ID)
    assert_redirect_login(response)

    login(client)
    response = client.get("/script/" + _SCRIPT_ID)
    assert response.status_code == 200
    assert b"Execution history for the script" in response.data


def test_api_script(client):
    response = client.get("/api/scripts/" + _SCRIPT_ID)
    assert_unauthorized(response)

    login(client)
    response = client.get("/api/scripts/" + _SCRIPT_ID)
    assert response.status_code == 200
    assert response.json == {
        "description": "Hello world for test",
        "executions": [],
        "group": "demo",
        "id": "pyscriptdemo.helloworld.HelloWorld",
        "name": "Hello world",
        "params": []
    }

    response = client.post("/api/scripts/" + _SCRIPT_ID + "/_run")
    assert response.status_code == 200
    test_output = "Hello Mister, Hello Mister, Hello Mister, Hello Mister, Hello Mister, Hello Mister, Hello Mister"
    assert response.json["dataOutput"] == test_output
    assert response.json["message"] == "Hello World !"
    assert response.json["runAt"] > 1597672257
    assert response.json["success"]

    response = client.get("/api/scripts/" + _SCRIPT_ID)
    assert response.status_code == 200
    assert len(response.json["executions"]) == 1
