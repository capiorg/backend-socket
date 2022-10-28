from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr


class TokenSessionModel(BaseModel):
    uuid: UUID
    session: UUID


class SmallUserModel(BaseModel):
    uuid: UUID
    login: str
    first_name: str
    last_name: str
    login_at: Optional[str]


class GetUserModel(SmallUserModel):
    is_me: Optional[bool]
    phone: str
    email: Optional[EmailStr]
    session_id: Optional[UUID]

