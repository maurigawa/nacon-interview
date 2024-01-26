from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class NSQLModel(SQLModel):
    class Config:
        # forbids extra attributes when
        # constructing model (default: 'ignore')
        extra = "forbid"


class PersistenceBase(SQLModel):
    # Database related attrobutes, that are found in DB and Response
    id: Optional[int] = Field(default=None, primary_key=True)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
