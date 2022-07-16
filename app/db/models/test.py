from sqlalchemy import Column, Boolean, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.db.models.base import Base


class Test(Base):
    __tablename__ = "test"
    id = Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    flag = Column(Boolean, nullable=False)
    name = Column(String(16), unique=True)
