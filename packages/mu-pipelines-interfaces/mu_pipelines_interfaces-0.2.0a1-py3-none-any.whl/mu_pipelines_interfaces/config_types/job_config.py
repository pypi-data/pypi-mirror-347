from typing import TypedDict

from mu_pipelines_interfaces.config_types.destination_config import DestinationConfig
from mu_pipelines_interfaces.config_types.execute_config import ExecuteConfig


class JobConfigItem(TypedDict):
    execution: list[ExecuteConfig]
    destination: list[DestinationConfig]
