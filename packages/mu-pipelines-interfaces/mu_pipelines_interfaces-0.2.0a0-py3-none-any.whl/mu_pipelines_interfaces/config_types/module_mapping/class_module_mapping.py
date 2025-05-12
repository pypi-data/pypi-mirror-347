from typing import NotRequired, TypedDict


class ClassModuleMappingItem(TypedDict):
    module_path: str
    class_name: str
    intialize_context_module: NotRequired[str]
