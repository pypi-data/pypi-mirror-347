from typing import Annotated, Type, Unpack

from fastapi import Depends
from pydantic import BaseModel

from quick_jwt import CheckJWT
from quick_jwt._function_args import ModelValidateKwargs


def build_check_jwt_depends[JWTModelType: Type[BaseModel]](
        jwt_model: JWTModelType,
        **_jwt_payload_model_validate_kwargs: Unpack[ModelValidateKwargs],
) -> JWTModelType:
    depends = CheckJWT(
        jwt_model,
        **_jwt_payload_model_validate_kwargs
    )
    return Annotated[JWTModelType, Depends(depends)]
