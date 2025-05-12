from abc import ABC
from typing import Any, NotRequired

from mu_pipelines_interfaces.config_types.secrets.secrets_config import (
    SecretsConfigItem,
)
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider
from mu_pipelines_interfaces.context import Context


class SecretsContext(Context):
    secrets: NotRequired[dict]


class SecretsModuleInterface(ABC):
    _config: SecretsConfigItem
    _configuration_provider: ConfigurationProvider
    secret_name: str

    def __init__(
        self, config: SecretsConfigItem, configuration_provider: ConfigurationProvider
    ):
        self._config = config
        self._configuration_provider = configuration_provider
        self.secret_name = config["name"]

    def _check_cached_secret(self, context: SecretsContext) -> Any | None:
        if "secrets" not in context:
            context["secrets"] = dict()

        if self._config["name"] in context["secrets"]:
            return context["secrets"][self._config["name"]]

        return None

    def _cache_secret(self, secret_value: Any | None, context: SecretsContext) -> None:
        if secret_value is None:
            return

        if "secrets" not in context:
            context["secrets"] = dict()

        context["secrets"][self._config["name"]] = secret_value

    def get(self, context: SecretsContext) -> Any | None:
        cached_secret: Any | None = self._check_cached_secret(context)
        if cached_secret is not None:
            return cached_secret

        new_secrets_value: Any | None = self.get_uncached_secret(context)
        self._cache_secret(new_secrets_value, context)

        return new_secrets_value

    def get_uncached_secret(self, context: SecretsContext) -> Any | None:

        raise NotImplementedError()
