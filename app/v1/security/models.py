import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr


class RoleDTO(BaseModel):
    id: int
    title: str


class AvatarDTO(BaseModel):
    document_id: UUID
    url: str


class TokenSessionModel(BaseModel):
    uuid: UUID
    session: UUID


class SmallUserModel(BaseModel):
    uuid: UUID
    login: str
    first_name: str
    last_name: str
    login_at: Optional[str]
    avatar: AvatarDTO
    role: RoleDTO

    is_online: bool
    last_activity: datetime.datetime


class GetUserModel(SmallUserModel):
    is_me: Optional[bool]
    phone: str
    email: Optional[EmailStr]
    session_id: Optional[UUID]
    jwt: Optional[str] = None


