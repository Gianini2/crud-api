from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from .database import Base

class Item(Base):
    __tablename__ = "items"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )