from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.ext.db import Base

from app.models.user import UserWorkspace


class Workspace(Base):
	__tablename__ = "workspace"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	name = Column(String(255), unique=True, index=True)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
	updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow())
	is_active = Column(Boolean, nullable=False, default=True)

	users = relationship("User", secondary=UserWorkspace.__tablename__, back_populates="workspaces")
