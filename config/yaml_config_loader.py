import os
import re

import yaml

CHAT_CLIENT_CONFIG_NAME = 'chat_client_config.yaml'
TTS_CLIENT_CONFIG_NAME = 'tts_client_config.yaml'
CONFIG_DIR_PATH = os.path.join(os.path.dirname(__file__))
CHAT_CLIENT_CONFIG = os.path.join(CONFIG_DIR_PATH, CHAT_CLIENT_CONFIG_NAME)
TTS_CLIENT_CONFIG = os.path.join(CONFIG_DIR_PATH, TTS_CLIENT_CONFIG_NAME)
def load_yaml_config(path: str) -> dict:
    """
    读取 YAML
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(r"\$\{(\w+)\}")

    # replace ${VAR_NAME} with os.getenv('VAR_NAME')
    def replacer(match):
        env_var = match.group(1)
        return os.getenv(
            env_var, match.group(0)
        )  # return the original string if the env var is not found

    content = pattern.sub(replacer, content)

    # Load the yaml file
    return yaml.safe_load(content)