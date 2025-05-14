from typing import Annotated

from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyCookie

access_bearer_security = Annotated[
    HTTPAuthorizationCredentials | None,
    Security(
        HTTPBearer(
            scheme_name='Bearer', description='Set refresh token to header (without Bearer in start).',
            auto_error=False
        )
    )
]

access_cookies_security = Annotated[
    str | None,
    Security(
        APIKeyCookie(
            name='access', description='Set refresh token to cookies.', auto_error=False,
        )
    )
]
