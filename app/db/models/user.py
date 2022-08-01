from sqlalchemy import Column, DateTime, Index, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    username = Column(String(32), nullable=False)
    discord_id = Column(String(24), nullable=False)
    last_login = Column(DateTime, nullable=False)

    __table_args__ = (Index("discord_idx", discord_id, unique=True),)

    @classmethod
    def lookup_by_id(cls, id_, provider=None, session=None):
        column_name = f"{provider}_id" if provider else "id"
        return cls.query(session).filter(getattr(cls, column_name) == id_).first()
