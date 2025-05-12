from typing import NotRequired, TypedDict


class SecretValueMapping(TypedDict):
    secret_name: str
    secret_value: NotRequired[str]
