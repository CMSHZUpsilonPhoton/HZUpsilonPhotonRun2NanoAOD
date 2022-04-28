from __future__ import annotations

from typing import Any, Dict

import yaml


class Configs(Dict[Any, Any]):
    def __getattr__(self, name: str) -> Configs:
        value: Dict[Any, Any] = self[name]
        if isinstance(value, Dict):
            value = Configs(value)
        return value


with open("config/config.yml") as f:
    config_dict = yaml.load(f, Loader=yaml.FullLoader)

config = Configs(config_dict)
