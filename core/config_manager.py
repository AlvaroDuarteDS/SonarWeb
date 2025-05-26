import json
import os
from typing import Dict, Any


class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.create_default_config()

    def create_default_config(self) -> Dict[str, Any]:
        default_config = {
            "OPENAI_API_KEY": "",
            "audio": {
                "chunk_size": 1024,
                "sample_rate": 44100,
                "channels": 1
            },
            "browser": {
                "headless": False,
                "window_size": {"width": 1920, "height": 1080}
            },
            "ui": {
                "always_on_top": True,
                "window_size": {"width": 500, "height": 300}
            }
        }

        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)

        return default_config

    def get(self, key: str, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is default:
                break
        return value
