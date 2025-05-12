from typing import Any, Protocol, TypedDict

from mu_pipelines_interfaces.config_types.secrets.secret_value_mapping import (
    SecretValueMapping,
)


class GetSecretFunc(Protocol):
    def __call__(self, secret_value_mapping: SecretValueMapping) -> Any:
        ...


class Context(TypedDict):
    get_secret: GetSecretFunc
