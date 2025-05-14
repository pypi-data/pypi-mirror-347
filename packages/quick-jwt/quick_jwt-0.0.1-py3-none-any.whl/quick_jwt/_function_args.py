from typing import Any, TypedDict


class ModelValidateKwargs(TypedDict, total=False):
    strict: bool | None = None
    from_attributes: bool | None = None
    context: Any | None = None
    by_alias: bool | None = None
    by_name: bool | None = None
