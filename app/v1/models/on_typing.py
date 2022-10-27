from uuid import UUID

from pydantic import BaseModel


class TypingSubModel(BaseModel):
    conversation_id: UUID


class TypingPubModel(BaseModel):
    pass
