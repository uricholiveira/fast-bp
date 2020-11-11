from datetime import datetime
from dynaconf import settings
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.ext.db import Base
from app.models.user import EnvironmentUserWorkspace


class Environment(Base):
	__tablename__ = 'environment'

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	name = Column(String(255), index=True, nullable=False)
	description = Column(String(255), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
	updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow())
	is_active = Column(Boolean, nullable=False, default=True)
	workspace_id = Column(Integer, ForeignKey("workspace.id"))

	users = relationship("User", secondary=EnvironmentUserWorkspace.__tablename__, back_populates="environments")
