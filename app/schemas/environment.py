import arrow
from datetime import datetime, timedelta

from dynaconf import settings
from pydantic import BaseModel, validator
from typing import Optional, List

from app.schemas.user import UserOut


class EnvironmentBase(BaseModel):
	name: str
	description: str


class EnvironmentIn(EnvironmentBase):
	is_active: Optional[bool] = None
	workspace_id: int


class EnvironmentOut(EnvironmentIn):
	users: List[UserOut]

	class Config:
		orm_mode = True


class EnvironmentPatch(BaseModel):
	name: Optional[str] = None
	description: Optional[str] = None
	is_active: Optional[bool] = None
