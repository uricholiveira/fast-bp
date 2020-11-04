from datetime import timedelta, datetime
from dynaconf import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Union, Optional, Any

from app.ext.db import get_db
from app.schemas import auth as schema, user as user_schema
from app.models import user as model
from app.services import user as service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def authenticate_user(db: Session, form: OAuth2PasswordRequestForm = Depends()) -> Union[model.User, HTTPException]:
	user = db.query(model.User).filter(model.User.email == form.username).first()
	if not user:
		raise HTTPException(status_code=404, detail="User not found!")
	if not user.check_password(form.password):
		raise HTTPException(status_code=404, detail="Wrong password")
	return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
	return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Any:
	credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials",
	                                      headers={"WWW-Authenticate": "Bearer"})
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		email: str = payload.get("sub")
		if email is None:
			raise credentials_exception
		token_data = schema.TokenData(email=email)
	except JWTError:
		raise credentials_exception
	user = service.get_user_by_email(db=db, email=token_data.email)
	if user is None:
		raise credentials_exception
	return user


def get_current_active_user(current_user: user_schema.UserIn = Depends(get_current_user)):
	if not current_user.is_active:
		raise HTTPException(status_code=400, detail="User is inactive")
	return current_user
