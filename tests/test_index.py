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
            "description": "Clean by number OR by date",
            "group": "base",
            "id": "pyscriptdeck.base.execution.CleanHistory",
            "name": "Clean execution history",
            "params": [
                {
                    "default": "by_number",
                    "id": "clean_type",
                    "label": "Clean by number or by date",
                    "type": "radio",
                    "values": [
                        {
                            "label": "By number",
                            "value": "by_number"
                        },
                        {
                            "label": "By date",
                            "value": "by_date"
                        }
                    ]
                },
                {},
                {
                    "default": "20",
                    "id": "clean_number",
                    "label": "Execution history to keep by script (older are deleted)",
                    "type": "number"
                },
                {
                    "default": (date.today() - timedelta(days=30)).isoformat(),
                    "id": "clean_date",
                    "label": "Execution history to delete older than a date",
                    "type": "date"
                }
            ]
        },
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
            "description": "Yes or No Api from yesno.wtf",
            "group": "demo",
            "id": "pyscriptdemo.apidemo.SimpleApi",
            "name": "Simple API",
            "params": []
        },
        {
            "description": "Weather API from rapidapi.com",
            "group": "demo",
            "id": "pyscriptdemo.apidemo.WeatherApi",
            "name": "Weather API",
            "params": [
                {
                    "default": "Paris,fr",
                    "id": "q",
                    "label": "Search",
                    "type": "text"
                }
            ]
        },
        {
            "description": "Calculate a Fibonacci number at a position",
            "group": "demo",
            "id": "pyscriptdemo.calculatedemo.CalculateFibonacci",
            "name": "Calculate Fibonacci numbers",
            "params": [
                {
                    "default": 10,
                    "id": "position",
                    "label": "Position in the Fibonacci sequence",
                    "type": "number"
                }
            ]
        },
        {
            "description": "Estimate Pi with the Monte Carlo method",
            "group": "demo",
            "id": "pyscriptdemo.calculatedemo.CalculatePi",
            "name": "Calculate Pi",
            "params": [
                {
                    "default": 50,
                    "id": "iterations",
                    "label": "Number of iterations",
                    "type": "number"
                }
            ]
        },
        {
            "description": "Generate a hash with Bcrypt",
            "group": "demo",
            "id": "pyscriptdemo.encoderdemo.BCryptGenerateHash",
            "name": "BCrypt generate hash",
            "params": [
                {
                    "default": "",
                    "id": "value",
                    "label": "Text to hash",
                    "type": "text"
                }
            ]
        },
        {
            "description": "Encode or decode content in Base64",
            "group": "demo",
            "id": "pyscriptdemo.encoderdemo.Base64Encoder",
            "name": "Base64 Encoder",
            "params": [
                {
                    "default": "encode",
                    "id": "type",
                    "label": "Encode or Decode",
                    "type": "radio",
                    "values": [
                        {
                            "label": "Encode",
                            "value": "encode"
                        },
                        {
                            "label": "Decode",
                            "value": "decode"
                        }
                    ]
                },
                {
                    "default": "",
                    "id": "value",
                    "label": "Input",
                    "type": "textarea"
                }
            ]
        },
        {
            "description": "Hello world for test",
            "group": "demo",
            "id": "pyscriptdemo.helloworld.HelloWorld",
            "name": "Hello world",
            "params": []
        },
        {
            "description": "Hello world with all types params for test",
            "group": "demo",
            "id": "pyscriptdemo.helloworld.HelloWorldWithParams",
            "name": "Hello with params",
            "params": [
                {
                    "default": "default value",
                    "id": "a",
                    "label": "Type text",
                    "type": "text"
                },
                {
                    "default": 10,
                    "id": "b",
                    "label": "Type number",
                    "type": "number"
                },
                {
                    "default": True,
                    "id": "c",
                    "label": "Type checkbox",
                    "type": "checkbox"
                },
                {
                    "default": "My text \n in textarea",
                    "id": "d",
                    "label": "Type textarea",
                    "placeholder": "Placeholder",
                    "type": "textarea"
                },
                {
                    "default": "1",
                    "id": "e",
                    "label": "Type radio",
                    "type": "radio",
                    "values": [
                        {
                            "label": "Radio 1",
                            "value": "1"
                        },
                        {
                            "label": "Radio 2",
                            "value": "2"
                        }
                    ]
                },
                {
                    "default": "b",
                    "id": "f",
                    "label": "Type select",
                    "multiple": False,
                    "type": "select",
                    "values": [
                        {
                            "label": "Option a",
                            "value": "a"
                        },
                        {
                            "label": "Option b",
                            "value": "b"
                        },
                        {
                            "label": "Option c",
                            "value": "c"
                        }
                    ]
                }
            ]
        }
    ]
    assert response.json == attended_response
