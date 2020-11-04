import arrow
from datetime import datetime, timedelta

from dynaconf import settings
from pydantic import BaseModel, validator
from typing import Optional

from app.schemas.user import UserOut


class Token(BaseModel):
	access_token: str
	token_expire: Optional[timedelta]
	token_type: Optional[str]

	class Config:
		orm_mode = True


class TokenData(Token):
	email: Optional[str] = None
	user: Optional[UserOut] = None


class Auth(BaseModel):
	username: str
	password: str
