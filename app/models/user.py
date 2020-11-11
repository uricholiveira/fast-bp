import arrow
from datetime import datetime
from passlib.context import CryptContext
from dynaconf import settings
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.ext.db import Base

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserWorkspace(Base):
	__tablename__ = "user_workspace"
	user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
	workspace_id = Column(Integer, ForeignKey('workspace.id'), primary_key=True)


class EnvironmentUserWorkspace(Base):
	__tablename__ = 'user_workspace_environment'

	user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
	environment_id = Column(Integer, ForeignKey('environment.id'), primary_key=True)
	role = Column(String, nullable=True, default='Guest')


class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True, autoincrement=True, index=True)
	name = Column(String, nullable=False)
	email = Column(String, nullable=False, index=True)
	passw = Column(String, nullable=False, name="password")
	created_at = Column(DateTime, nullable=True, default=datetime.utcnow())
	updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.utcnow())
	is_active = Column(Boolean, nullable=False, default=True)
	is_admin = Column(Boolean, nullable=False, default=False)

	workspaces = relationship("Workspace", secondary=UserWorkspace.__tablename__, back_populates="users")
	environments = relationship("Environment", secondary=EnvironmentUserWorkspace.__tablename__, back_populates="users")

	@property
	def password(self):
		return self.passw

	@password.setter
	def password(self, value):
		self.passw = crypt.hash(value)

	def check_password(self, value):
		if crypt.verify(value, self.password):
			return True
