# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["V1CreateSqlResponse", "Rows", "Error"]


class Rows(BaseModel):
    rows: List[object]


class Error(BaseModel):
    error: str


V1CreateSqlResponse: TypeAlias = Union[Rows, Error]
