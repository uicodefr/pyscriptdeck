import requests
from pydantic import BaseModel, ValidationError
from pyscriptdeck.common import ScriptDeck, ScriptDescription, ScriptResult


class YesNoResponse(BaseModel):
    answer: str
    forced: bool
    image: str

class SimpleApi(ScriptDeck):
    def __init__(self):
        super(SimpleApi, self).__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Simple API",
            description="Yes or No Api from yesno.wtf",
            params=[]
        )

    def run(self, data_input):
        url = self.get_config("url")
        response = requests.get(url)

        if response.status_code != 200:
            message = "Incorrect status code : {}".format(response.status_code)
            return ScriptResult(success=False, message=message)
        json_response = response.json()
        if json_response is None:
            return ScriptResult(success=False, message="No json in the response body")

        # Use pydantic for demo purpose
        try:
            yes_no_response = YesNoResponse(**json_response)
        except ValidationError:
            return ScriptResult(success=False, message="Invalid json response")

        message = "The answer is '{}'".format(yes_no_response.answer)
        return ScriptResult(success=True, message=message, dataOutput=yes_no_response.dict())


class WeatherApi(ScriptDeck):
    def __init__(self):
        super(WeatherApi, self).__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Weather API",
            description="Weather API from rapidapi.com",
            params=[{
                "id": "q",
                "type": "text",
                "label": "Search",
                "default": "Paris,fr"
            }]
        )

    def run(self, data_input):
        url = self.get_config("url")
        api_key = self.get_config("api-key")
        q_param = data_input["q"]

        query = {"q": q_param, "appid": api_key}
        response = requests.get(url, params=query)

        if response.status_code != 200:
            message = "Incorrect status code : {}".format(response.status_code)
            return ScriptResult(success=False, message=message)
        json_response = response.json()
        if json_response is None:
            return ScriptResult(success=False, message="No json in the response body")

        # The check is done manually but we can use pydantic (see SimpleApi)
        if ("weather" in json_response and isinstance(json_response["weather"], list)
                and len(json_response["weather"]) > 0 and "main" in json_response["weather"][0]
           ):
            message = "The weather in '{} 'is '{}'".format(q_param, \
                json_response["weather"][0]["main"])
        else:
            message = "Can't parse weather info but it's ok"

        data = json_response
        return ScriptResult(success=True, message=message, dataOutput=data)
