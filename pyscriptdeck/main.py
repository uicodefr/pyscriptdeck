import logging
import importlib
import inspect
from datetime import datetime
from typing import Dict
import bcrypt
from flask import abort, session, current_app
from pyscriptdeck._version import VERSION
from pyscriptdeck.config import getconfig
from pyscriptdeck.common import ScriptDeck, global_config
from pyscriptdeck.dao import UserDao, ExecutionHistory, ExecutionHistoryDao, ParameterDao


EXECUTION_HISTORY_LIMIT = 10
logger = logging.getLogger(__name__)

class Main:
    def __init__(self):
        self._config = {}
        self._scripts = {}
        self._load_config()
        self._load_modules()

    def _load_config(self):
        self._config = getconfig()
        global_config.update(self._config)
        logger.info("config loaded")

    def _load_modules(self):
        self._scripts = {}
        for module_name in self._config["app.script.modules"]:
            module = importlib.import_module(module_name)
            self._load_module(module)

    def _load_module(self, module):
        scripts_count = 0
        for attribute_name in dir(module):
            if (
                not attribute_name.startswith("__")
                and inspect.isclass(getattr(module, attribute_name))
                and issubclass(getattr(module, attribute_name), ScriptDeck)
                and not inspect.isabstract(getattr(module, attribute_name))
            ):
                script_instance = getattr(module, attribute_name)()
                self._scripts[script_instance.get_id()] = script_instance
                logger.info("%s discovered", attribute_name)
                scripts_count += 1

        logger.info("'%s' module loaded (%d scripts)", module.__name__, scripts_count)

    def is_script_exist(self, script_id: str):
        return script_id in self._scripts

    def get_scripts_descriptions(self):
        if current_app.config["ENV"] == "development":
            self._load_modules()
        logger.info("Get scripts descriptions")
        scripts = list(map(lambda script: script.get_full_description(), self._scripts.values()))
        scripts.sort(key=lambda script: script["id"])
        return scripts

    def get_script_info(self, script_id: str):
        logger.info("Get script info for %s", script_id)
        script_info = self._scripts[script_id].get_full_description()
        script_info["executions"] = self.get_script_executions(script_id)
        return script_info

    def get_script_executions(self, script_id: str):
        logger.info("Get script executions for %s", script_id)
        return list(map(lambda exec: exec.dict(), ExecutionHistoryDao.findall_by_script_id( \
            script_id, EXECUTION_HISTORY_LIMIT)))

    def run_script(self, script_id: str, data_input: Dict):
        try:
            script_result = self._scripts[script_id].run(data_input).dict()
        except Exception as exception:
            logger.exception("Error while running the script %s", script_id)
            script_result = {}
            script_result["success"] = False
            script_result["message"] = getattr(exception, 'message', repr(exception))

        script_result["runAt"] = datetime.now().timestamp()

        user_id = self.get_current_user_id()
        execution_history = ExecutionHistory(
            script_id=script_id,
            run_at=datetime.now(),
            executed_by_id=user_id,
            execution_success=script_result["success"],
            execution_message=script_result["message"]
        )
        ExecutionHistoryDao.insert(execution_history)

        logger.info("Script %s run with the status %s", script_id, script_result["success"])
        return script_result

    def get_executions(self):
        logger.info("Get executions")
        return list(map(lambda exec: exec.dict(), ExecutionHistoryDao.findall()))

    def get_groups(self):
        logger.info("Get groups")
        groups = list(set(map(lambda script: script["group"], self.get_scripts_descriptions())))
        groups.sort()
        return groups

    def get_current_user_id(self):
        if "user" not in session:
            abort(403, "cannot get current user_id with session")
        user = UserDao.find_by_username(session["user"])
        return user.id

    def login(self, username: str, password: str):
        user = UserDao.find_by_username(username)
        if user is None:
            logger.info("User '%s' not found", username)
            return False
        login = bcrypt.checkpw(password.encode(), user.password)
        logger.info("Login attempt for %s and the result is %s", username, login)
        return login

    def get_status(self):
        return {
            "status": ParameterDao.find_by_id("general.status").value,
            "currentDate": datetime.now().timestamp(),
            "coreVersion": VERSION,
            "appVersion": self._config["app.version"]
        }
