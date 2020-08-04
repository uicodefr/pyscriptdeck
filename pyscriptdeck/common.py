""" Core Module used by scripts and Main module """
import logging
import os
from typing import Any, List, Dict
import abc
from pydantic import BaseModel


logger = logging.getLogger(__name__)

class ScriptDescription(BaseModel):
    """ Description for a script """
    group: str
    name: str
    description: str
    params: List[Any]

class ScriptResult(BaseModel):
    """ Result for a script for the run method """
    success: bool
    message: str
    dataOutput: Any

class ScriptException(Exception):
    """ Exception for ScriptDeck """
    _status = 500

    def __init__(self, message: str, status: int = None):
        super(ScriptException, self).__init__(message)
        if status is not None:
            self._status = status

    def get_status(self) -> int:
        """ Http status code of the response """
        return self._status

class ScriptDeck(abc.ABC):
    """ Abstract call to extends for script """
    def __init__(self, module_name):
        self._id = module_name + '.' + (self.__class__.__name__)

    @abc.abstractmethod
    def get_description(self) -> ScriptDescription:
        """ return the description of the script """
        raise ScriptException("method 'get_description' not implemented")

    @abc.abstractmethod
    def run(self, data_input: Dict) -> ScriptResult:
        """ run the script """
        raise ScriptException("method 'run' not implemented")

    def get_id(self) -> str:
        """ return id of the script """
        return self._id

    def get_full_description(self) -> Dict:
        """ return the full description (description + id) """
        full_description = self.get_description().dict()
        full_description["id"] = self.get_id()
        return full_description

    def get_config(self, key: str) -> Any:
        """ get the config for the script """
        if self._id not in global_config:
            logger.warning("No config found for script : %s", self._id)
            return None

        script_config = global_config[self._id]
        if key not in script_config:
            logger.warning("The key '%s' is not found in script config %s", key, self._id)
            return None

        value_config = script_config[key]
        if (isinstance(value_config, str) and value_config.startswith("${")
                and value_config.endswith("}")):
            env_variable = value_config[2:-1]
            logger.debug("Get environment variable with the value '%s'", env_variable)
            return os.environ.get(env_variable)

        return value_config

global_config = {}
