import json
import os

from utils.environment import Environment


class StackConfig:
    environment = Environment

    def load_config(file):
        with open(f"{os.path.dirname(os.path.abspath(file))}/config.json", "r") as file:
            return json.loads(file.read())
