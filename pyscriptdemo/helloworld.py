from pyscriptdeck.common import ScriptDeck, ScriptDescription, ScriptResult


class HelloWorld(ScriptDeck):
    """ HelloWorld script just for test """
    def __init__(self):
        super().__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Hello world",
            description="Hello world for test", params=[]
        )

    def run(self, data_input):
        message = "Hello World !"
        data_array = []
        for _ in range(self.get_config("number")):
            data_array.append("Hello " + self.get_config("hello"))
        data = ", ".join(data_array)

        return ScriptResult(success=True, message=message, dataOutput=data, template="text")

class HelloWorldTable(ScriptDeck):
    """ HelloWorld script with table in output """
    def __init__(self):
        super().__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Hello world with table",
            description="Hello world with table in ouput", params=[]
        )

    def run(self, data_input):
        message = "Hello World with table !"
        data = []
        data.append(["String", "Number", "Boolean"])
        data.append(["Hello", 12, True])
        data.append(["OK", 20, False])
        data.append(["Bye", 3.14, True])

        return ScriptResult(success=True, message=message, dataOutput=data, template="table")


class HelloWorldWithParams(ScriptDeck):
    """ HelloWorld script with params """
    def __init__(self):
        super().__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Hello with params",
            description="Hello world with all types params for test",
            params=[{
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
        )

    def run(self, data_input):
        message = "Hello (the output is the input of the script)"
        data_output = {"values": data_input, "params":self.get_description().params}
        return ScriptResult(success=True, message=message, dataOutput=data_output)
