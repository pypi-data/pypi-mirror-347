from typing import Type, Unpack

from fastapi import Request, Response, HTTPException, status
from jwt import InvalidTokenError
from pydantic import BaseModel

from quick_jwt._function_args import ModelValidateKwargs
from quick_jwt.security import access_bearer_security, access_cookies_security
from quick_jwt.utils import get_config_from_request


class CheckJWT:
    def __init__(
            self,
            jwt_payload_model: Type[BaseModel],
            **jwt_payload_model_validate_kwargs: Unpack[ModelValidateKwargs],
    ):
        self._jwt_payload_model = jwt_payload_model
        self._jwt_payload_model_validate_kwargs = jwt_payload_model_validate_kwargs

    async def __call__(
            self,
            request: Request,
            response: Response,
            bearer_token: access_bearer_security,
            cookies_token: access_cookies_security,
    ) -> BaseModel:
        config = get_config_from_request(request)

        if bearer_token is not None and bearer_token.credentials is not None:
            token = bearer_token.credentials
        elif cookies_token is not None:
            token = cookies_token
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            raw_payload = config.py_jwt.decode(token, **config.build_decode_params())
            return self._jwt_payload_model.model_validate(
                raw_payload,
                **self._jwt_payload_model_validate_kwargs
            )
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
