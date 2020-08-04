from tests.test_base import app, client, login

_SCRIPT_ID_PI = "pyscriptdemo.calculatedemo.CalculatePi"
_SCRIPT_ID_FIB = "pyscriptdemo.calculatedemo.CalculateFibonacci"

def test_calculate_pi(app, client):
    login(client)

    params = {"iterations": 50}
    response = client.post("/api/scripts/" + _SCRIPT_ID_PI + "/_run", json=params)
    assert response.json["success"]
    assert "Estimate Pi as" in response.json["message"]
    assert response.json["dataOutput"]["iterations"] == 50
    assert response.json["dataOutput"]["pointsInside"] <= 50

    params = {"iterations": 50000000}
    response = client.post("/api/scripts/" + _SCRIPT_ID_PI + "/_run", json=params)
    assert not response.json["success"]
    assert "The maximum number of iterations allowed is" in response.json["message"]

def test_calculate_fib(app, client):
    login(client)

    params = {"position": 50}
    response = client.post("/api/scripts/" + _SCRIPT_ID_FIB + "/_run", json=params)
    assert response.json["success"]
    assert response.json["message"] == "The fibonacci number at the position 50 has the value 1275"
    assert response.json["dataOutput"]["position"] == 50
    assert response.json["dataOutput"]["value"] == 1275

    params = {"position": 5000}
    response = client.post("/api/scripts/" + _SCRIPT_ID_FIB + "/_run", json=params)
    assert not response.json["success"]
    assert "The maximum position allowed is" in response.json["message"]
