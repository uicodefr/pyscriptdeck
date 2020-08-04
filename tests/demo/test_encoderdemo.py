import bcrypt
from tests.test_base import app, client, login

_SCRIPT_ID_BASE64 = "pyscriptdemo.encoderdemo.Base64Encoder"
_SCRIPT_ID_BCRYPT = "pyscriptdemo.encoderdemo.BCryptGenerateHash"


def test_base64_encoder(app, client):
    login(client)

    params = {"type":"encode", "value":"test"}
    response = client.post("/api/scripts/" + _SCRIPT_ID_BASE64 + "/_run", json=params)
    assert response.json["success"]
    assert response.json["message"] == "Encode Base64 success"
    assert response.json["dataOutput"]["value"] == "test"
    assert response.json["dataOutput"]["encodedValue"] == "dGVzdA=="

    params = {"type":"decode", "value":"dGVzdA=="}
    response = client.post("/api/scripts/" + _SCRIPT_ID_BASE64 + "/_run", json=params)
    assert response.json["success"]
    assert response.json["message"] == "Decode Base64 success"
    assert response.json["dataOutput"]["value"] == "dGVzdA=="
    assert response.json["dataOutput"]["decodedValue"] == "test"

    params = {"type":"decode", "value":"error"}
    response = client.post("/api/scripts/" + _SCRIPT_ID_BASE64 + "/_run", json=params)
    assert not response.json["success"]
    assert response.json["message"] == "Error decoding in Base64"

def test_bcrypt_hash(app, client):
    login(client)

    params = {"value":"motdepasse"}
    response = client.post("/api/scripts/" + _SCRIPT_ID_BCRYPT + "/_run", json=params)
    assert response.json["success"]
    assert response.json["message"] == "BCrypt hash success"
    assert response.json["dataOutput"]["value"] == "motdepasse"
    assert bcrypt.checkpw("motdepasse".encode(), response.json["dataOutput"]["hash"].encode())
