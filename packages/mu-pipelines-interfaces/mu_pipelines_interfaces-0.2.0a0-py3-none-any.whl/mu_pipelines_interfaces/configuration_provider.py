from abc import ABC
from typing import Type, TypeVar

from mu_pipelines_interfaces.config_types.connection_properties import (
    ConnectionProperties,
)
from mu_pipelines_interfaces.config_types.global_properties.global_properties import (
    GlobalProperties,
)
from mu_pipelines_interfaces.config_types.job_config import JobConfigItem
from mu_pipelines_interfaces.config_types.secrets.secrets_config import SecretsConfig

TSuppFileType = TypeVar("TSuppFileType")


class ConfigurationProvider(ABC):
    def load_job_supporting_artifact(
        self, relative_artifact: str, content_type: Type[TSuppFileType]
    ) -> TSuppFileType | None:
        raise NotImplementedError()

    @property
    def job_config(self) -> list[JobConfigItem]:
        raise NotImplementedError()

    @property
    def global_properties(self) -> GlobalProperties:
        raise NotImplementedError()

    @property
    def connection_config(self) -> ConnectionProperties:
        raise NotImplementedError()

    @property
    def secrets_config(self) -> SecretsConfig:
        raise NotImplementedError()
