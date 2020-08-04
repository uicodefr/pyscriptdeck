import pytest
import requests
from tests.test_base import app, client, login
from pyscriptdeck.config import getconfig

_SCRIPT_ID_SIMPLE = "pyscriptdemo.apidemo.SimpleApi"
_SCRIPT_ID_WEATHER = "pyscriptdemo.apidemo.WeatherApi"

def test_simple_api(app, client, requests_mock):
    login(client)

    requests_mock.get(getconfig()[_SCRIPT_ID_SIMPLE]["url"], json={
        "answer": "yes",
        "forced": False,
        "image": "image_url"
    })

    response = client.post("/api/scripts/" + _SCRIPT_ID_SIMPLE + "/_run")
    print(response.json)
    assert response.json["success"]
    assert (response.json["message"] == "The answer is 'yes'"
            or response.json["message"] == "The answer is 'no'")
    assert "answer" in response.json["dataOutput"]


def test_weather_api(app, client, requests_mock):
    login(client)

    requests_mock.get(getconfig()[_SCRIPT_ID_WEATHER]["url"], json={
        "weather": [
            {"main": "Sunny"}
        ]
    })

    params = {"q": "Paris,fr"}
    response = client.post("/api/scripts/" + _SCRIPT_ID_WEATHER + "/_run", json=params)
    assert response.json["success"]
    assert "The weather in 'Paris,fr 'is" in response.json["message"]
    assert "weather" in response.json["dataOutput"]
