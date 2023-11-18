import os
import json
import yaml
from backend.base import BaseConfig

config = BaseConfig(__name__)

# utils
def show_json(obj):
    print(json.loads(obj.model_dump_json()))

@config._logger
def get_agent_config(agent):
    # set the path so we only need to pass agent name
    agent_config_path = os.path.join(config.AGENT_CONFIG_PATH, f'{agent}.yaml')
    with open(agent_config_path, 'r') as file:
        agent_config = yaml.safe_load(file)
    return agent_config