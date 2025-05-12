from typing import NotRequired, TypedDict

from mu_pipelines_interfaces.config_types.module_mapping.secrets_module_mapping import (
    SecretsModuleMappingItem,
)


class SecretsConfigItem(TypedDict):
    name: str
    provider: str
    additional_attributes: dict


class SecretsConfig(TypedDict):
    secrets: list[SecretsConfigItem]
    extra_secrets_modules: NotRequired[list[SecretsModuleMappingItem]]
