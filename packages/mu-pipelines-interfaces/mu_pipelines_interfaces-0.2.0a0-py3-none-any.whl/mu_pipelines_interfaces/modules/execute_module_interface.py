from typing import Any

from mu_pipelines_interfaces.config_types.execute_config import ExecuteConfig
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider
from mu_pipelines_interfaces.context import Context
from mu_pipelines_interfaces.modules.injectable_module_interface import (
    InjectableModuleInterface,
)


class ExecuteModuleInterface(InjectableModuleInterface):
    _config: ExecuteConfig
    _configuration_provider: ConfigurationProvider

    def __init__(
        self, config: ExecuteConfig, configuration_provider: ConfigurationProvider
    ):
        self._config = config
        self._configuration_provider = configuration_provider

    def execute(self, context: Context) -> Any | None:

        raise NotImplementedError()
