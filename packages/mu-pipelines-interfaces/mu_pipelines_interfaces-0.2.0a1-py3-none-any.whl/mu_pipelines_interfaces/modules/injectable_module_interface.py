from abc import ABC
from typing import Any, cast

from mu_pipelines_interfaces.config_types.secrets.secret_value_mapping import (
    SecretValueMapping,
)
from mu_pipelines_interfaces.context import Context, GetSecretFunc


def recursively_inject_secret(input: dict | list, get_secret: GetSecretFunc) -> None:

    if isinstance(input, list):
        for item in input:
            recursively_inject_secret(item, get_secret)
    else:
        for k, v in input.items():
            if isinstance(v, dict):
                if "secret_name" in v:
                    secret: Any = get_secret(cast(SecretValueMapping, v))
                    input[k] = secret
                else:
                    recursively_inject_secret(input[k], get_secret)
            else:
                recursively_inject_secret(input[k], get_secret)


class InjectableModuleInterface(ABC):
    __config: dict

    def __init__(self, config: dict):
        self.__config = config

    def inject_secrets(self, context: Context) -> None:
        recursively_inject_secret(self.__config, context["get_secret"])
