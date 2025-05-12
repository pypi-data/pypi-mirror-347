from mu_pipelines_interfaces.config_types.module_mapping.class_module_mapping import (
    ClassModuleMappingItem,
)


class SecretsModuleMappingItem(ClassModuleMappingItem):
    provider: str
