from typing import TypedDict

from mu_pipelines_interfaces.config_types.secrets.secret_value_mapping import (
    SecretValueMapping,
)


class ConnectionDetails(TypedDict):
    host: str
    database: str
    port: str
    username: str | SecretValueMapping
    password: str | SecretValueMapping
    certificate_path: str
    certificate: SecretValueMapping


class ConnectionConfig(TypedDict):
    name: str
    type: str
    connection_details: ConnectionDetails


class ConnectionProperties(TypedDict):
    connections: list[ConnectionConfig]
