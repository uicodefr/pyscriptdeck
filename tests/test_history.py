from tests.test_base import app, client, login
from tests.assertutil import assert_unauthorized, assert_redirect_login


def test_history(client):
    response = client.get("/history")
    assert_redirect_login(response)

    login(client)
    response = client.get("/history")
    assert response.status_code == 200
    assert b"Execution History" in response.data


def test_api_executions(client):
    response = client.get("/api/executions")
    assert_unauthorized(response)

    login(client)
    response = client.get("/api/executions")
    assert response.status_code == 200
    assert len(response.json) == 0

    # Run a HelloWorld 2 times
    for i in range(2):
        response = client.post("/api/scripts/pyscriptdemo.helloworld.HelloWorld/_run")
        assert response.status_code == 200

        response = client.get("/api/executions")
        assert response.status_code == 200
        assert len(response.json) == i+1
        assert response.json[i]["executedBy"] == "admin"
        assert response.json[i]["id"] == 1
        assert response.json[i]["message"] == "Hello World !"
        assert isinstance(response.json[i]["runAt"], float)
        assert response.json[i]["runAt"] > 1597672257
        assert response.json[i]["scriptId"] == "pyscriptdemo.helloworld.HelloWorld"
        assert response.json[i]["success"]
