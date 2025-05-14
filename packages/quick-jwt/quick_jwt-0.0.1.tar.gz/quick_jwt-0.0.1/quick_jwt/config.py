import json
from datetime import timedelta
from typing import Any, Sequence, Iterable

from jwt import PyJWT
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class QuickJWTConfig(BaseSettings):
    model_config = SettingsConfigDict()

    py_jwt: PyJWT = Field(PyJWT())

    encode_key:  str | bytes = Field(...)
    encode_algorithm: str | None = Field(None)
    encode_headers: dict[str, Any] | None = Field(None)
    encode_json_encoder: type[json.JSONEncoder] | None = Field(None)
    encode_sort_headers: bool = Field(True)

    decode_key:  str | bytes = Field(...)
    decode_algorithms: Sequence[str] | None = Field(None)
    decode_options: dict[str, Any] | None = Field(None)
    decode_verify: bool | None = Field(None)
    decode_detached_payload: bytes | None = Field(None)
    decode_audience: str | Iterable[str] | None = Field(None)
    decode_subject: str | None = Field(None)
    decode_issuer: str | Sequence[str] | None = Field(None)
    decode_leeway: float | timedelta = Field(0)

    def build_encode_params(self) -> dict[str, Any]:
        return {
            'key': self.encode_key,
            'algorithm': self.encode_algorithm,
            'headers': self.encode_headers,
            'json_encoder': self.encode_json_encoder,
            'sort_headers': self.encode_sort_headers,
        }

    def build_decode_params(self) -> dict[str, Any]:
        return {
            'key': self.decode_key,
            'algorithms': self.decode_algorithms,
            'options': self.decode_options,
            'verify': self.decode_verify,
            'detached_payload': self.decode_detached_payload,
            'audience': self.decode_audience,
            'subject': self.decode_subject,
            'issuer': self.decode_issuer,
            'leeway': self.decode_leeway,
        }
