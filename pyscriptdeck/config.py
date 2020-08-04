from typing import Dict
import yaml


_config = {}
def getconfig() -> Dict:
    if _config:
        return _config

    with open("config.yml") as file:
        _config.update(yaml.load(file, Loader=yaml.FullLoader))
    return _config
