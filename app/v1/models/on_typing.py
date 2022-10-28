import datetime
from uuid import UUID

from pydantic import BaseModel

from app.v1.security.models import SmallUserModel


class TypingSubModel(BaseModel):
    conversation_id: UUID


class TypingPubModel(BaseModel):
    author: SmallUserModel
    conversation_id: UUID
    created_at: datetime.datetime


