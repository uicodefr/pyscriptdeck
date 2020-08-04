from tests.test_base import app, client, login

_SCRIPT_ID_HELLO = "pyscriptdemo.helloworld.HelloWorld"
_SCRIPT_ID_HELLO_WITH_PARAMS = "pyscriptdemo.helloworld.HelloWorldWithParams"


def test_hello(app, client):
    login(client)

    response = client.post("/api/scripts/" + _SCRIPT_ID_HELLO + "/_run")
    assert response.json["success"]
    assert response.json["message"] == "Hello World !"
    assert response.json["dataOutput"]["config_hello"] == "Mister"
    assert response.json["dataOutput"]["config_number"] == 7


def test_hello_with_params(app, client):
    login(client)

    response = client.post("/api/scripts/" + _SCRIPT_ID_HELLO_WITH_PARAMS + "/_run")
    assert response.json["success"]
    assert response.json["dataOutput"]["values"] is None

    params = {"a":"default value", "b":10, "c":True, "d":"My text \n in textarea", "e":"1", "f":"b"}
    response = client.post("/api/scripts/" + _SCRIPT_ID_HELLO_WITH_PARAMS + "/_run", json=params)
    assert response.json["success"]
    assert response.json["dataOutput"]["values"] == params
    assert response.json["dataOutput"]["params"] == [
        {
            "id": "a",
            "type": "text",
            "label": "Type text",
            "default": "default value"
        }, {
            "id": "b",
            "type": "number",
            "label": "Type number",
            "default": 10
        }, {
            "id": "c",
            "type": "checkbox",
            "label": "Type checkbox",
            "default": True
        }, {
            "id": "d",
            "type": "textarea",
            "label": "Type textarea",
            "placeholder": "Placeholder",
            "default": "My text \n in textarea"
        }, {
            "id": "e",
            "type": "radio",
            "label": "Type radio",
            "values": [
                {"value": "1", "label": "Radio 1"},
                {"value": "2", "label": "Radio 2"}
            ],
            "default": "1"
        }, {
            "id": "f",
            "type": "select",
            "multiple": False,
            "label": "Type select",
            "values": [
                {"value": "a", "label": "Option a"},
                {"value": "b", "label": "Option b"},
                {"value": "c", "label": "Option c"}
            ],
            "default": "b"
        }]
