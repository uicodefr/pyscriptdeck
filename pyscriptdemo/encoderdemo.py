import base64
import bcrypt
from pyscriptdeck.common import ScriptDeck, ScriptDescription, ScriptResult


class Base64Encoder(ScriptDeck):
    def __init__(self):
        super(Base64Encoder, self).__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Base64 Encoder",
            description="Encode or decode content in Base64",
            params=[{
                "id": "type",
                "type": "radio",
                "label": "Encode or Decode",
                "values": [{
                    "value": "encode", "label": "Encode"
                }, {
                    "value": "decode", "label": "Decode"
                }],
                "default": "encode"
            }, {
                "id": "value",
                "type": "textarea",
                "label": "Input",
                "default": ""
            }]
        )

    def run(self, data_input):
        type_action = data_input["type"]
        value = data_input["value"]

        if type_action == "encode":
            encoded_value = base64.b64encode(value.encode())
            data = {"value": value, "encodedValue": encoded_value.decode()}
            return ScriptResult(success=True, message="Encode Base64 success", dataOutput=data)

        if type_action == "decode":
            try:
                decoded_value = base64.b64decode(value.encode())
                data = {"value": value, "decodedValue": decoded_value.decode()}
                return ScriptResult(success=True, message="Decode Base64 success", dataOutput=data)
            except ValueError:
                return ScriptResult(success=False, message="Error decoding in Base64")

        return ScriptResult(success=False, message="Unknown type : {}".format(type))


class BCryptGenerateHash(ScriptDeck):
    def __init__(self):
        super(BCryptGenerateHash, self).__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="BCrypt generate hash",
            description="Generate a hash with Bcrypt",
            params=[{
                "id": "value",
                "type": "text",
                "label": "Text to hash",
                "default": ""
            }]
        )

    def run(self, data_input):
        value = data_input["value"]
        value_hashed = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        data = {"value": value, "hash": value_hashed.decode()}
        return ScriptResult(success=True, message="BCrypt hash success", dataOutput=data)
