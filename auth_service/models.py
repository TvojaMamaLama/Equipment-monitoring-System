import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"
    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, unique=True)
    password = Column(String)

    def __init__(self, login, password):
        self.login = login
        self.password = password