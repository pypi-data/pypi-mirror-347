from fastapi import Request
from quick_jwt.config import QuickJWTConfig


def get_config_from_request(request: Request) -> QuickJWTConfig:
    try:
        return request.state.quick_jwt_config
    except AttributeError:
        raise Exception(
            """
            QuickJWTConfig not defined in middleware. Example of definition:'
            from fastapi import FastAPI
            from quick_jwt import QuickJWTConfig, QuickJWTMiddleware
            
            app = FastAPI()
            quick_jwt_config = QuickJWTConfig(encode_key='key', decode_key='key')
            app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
            """
        )
