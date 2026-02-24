from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ItemRead(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # importante para SQLAlchemy