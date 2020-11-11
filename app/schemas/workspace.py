import arrow
from datetime import datetime
from dynaconf import settings
from pydantic import BaseModel, validator
from typing import Optional, List

from app.schemas.user import UserOut
from app.schemas.environment import EnvironmentOut


class WorkspaceBase(BaseModel):
	name: str


class WorkspaceIn(WorkspaceBase):
	is_active: Optional[bool] = None


class WorkspaceOut(WorkspaceBase):
	is_active: bool
	users: List[UserOut]

	class Config:
		orm_mode = True


