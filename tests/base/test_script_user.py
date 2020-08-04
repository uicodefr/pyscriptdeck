from tests.test_base import app, client, login, logout

_SCRIPT_ID = "pyscriptdeck.base.user.ChangePassword"

def test_change_password(client):
    login(client)

    data = {
        "password": "1",
        "password_confirm": "1"
    }
    response = client.post("/api/scripts/" + _SCRIPT_ID + "/_run", json=data)
    assert not response.json["success"]
    assert response.json["message"] == "The minimum length is 5"

    data = {
        "password": "azertyuiop",
        "password_confirm": "qsdfghjkl"
    }
    response = client.post("/api/scripts/" + _SCRIPT_ID + "/_run", json=data)
    assert not response.json["success"]
    assert response.json["message"] == "The passwords does not match"

    data = {
        "password": "new password",
        "password_confirm": "new password"
    }
    response = client.post("/api/scripts/" + _SCRIPT_ID + "/_run", json=data)
    assert response.json["success"]
    assert response.json["message"] == "Password Updated"

    logout(client)
    response = login(client, password="new password")
    assert b"You have successfully logged in" in response.data
