import os
import pytest
import pyscriptdeck
from tests.assertutil import assert_unauthorized, assert_redirect_login

@pytest.fixture
def app():
    os.environ["FLASK_SECRET_KEY"] = "test"
    test_app = pyscriptdeck.create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    return test_app

@pytest.fixture
def client(app):
    return app.test_client()

def login(client, username="admin", password="admin1234"):
    return client.post('/login', data={
        "login": username,
        "password": password
    }, follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_base(client):
    response = client.get("/")
    assert response.status_code == 302
    response = client.get("/login")
    assert response.status_code == 200

def test_login_logout(client):
    response = login(client, "admin", "incorrect")
    assert b"Invalid credentials" in response.data

    response = login(client, "user", "admin1234")
    assert b"Invalid credentials" in response.data

    response = login(client)
    assert b"You have successfully logged in" in response.data

    response = client.get("/")
    assert response.status_code == 200
    response = client.get("/api/scripts")
    assert response.status_code == 200

    response = logout(client)
    assert b"You have been successfully logged out" in response.data

    response = client.get("/")
    assert_redirect_login(response)
    response = client.get("/api/scripts")
    assert_unauthorized(response)
