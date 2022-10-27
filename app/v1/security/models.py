from uuid import UUID

from pydantic import BaseModel


class TokenSessionModel(BaseModel):
    uuid: UUID
    session: UUID
