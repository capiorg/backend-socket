from typing import Generic
from typing import Optional
from typing import TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


ChildT = TypeVar("ChildT")


class BaseExceptionError(BaseModel):
    exception: str
    detail: Optional[str] = None
    message: Optional[str] = None


class BaseError(BaseModel):
    code: str
    message: str
    exception: Optional[BaseExceptionError]


class BaseResponse(GenericModel, BaseModel, Generic[ChildT]):
    status: bool = True
    code: int = 200
    error: Optional[BaseError]
    result: Optional[ChildT] = None
