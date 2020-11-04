from datetime import timedelta
from dynaconf import settings
from fastapi import APIRouter, Depends, Body, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.ext.db import get_db
from app.schemas import user as schema, auth as auth_schema
from app.services import user as service, auth as auth_service
from app.services.auth import oauth2_scheme

router = APIRouter()


@router.get('/', response_model=List[schema.UserOut])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
	return service.get_users(db=db, skip=skip, limit=limit)


@router.get('/{user_id}', response_model=schema.UserOut)
def get_user_by_id(db: Session = Depends(get_db), user_id: int = None):
	return service.get_user_by_id(db, user_id)


@router.post('/', response_model=schema.UserOut)
def create_user(db: Session = Depends(get_db), user: schema.UserRegister = Depends()):
	return service.create_user(db, user)


@router.put('/{user_id}', response_model=schema.UserOut)
def update_user(db: Session = Depends(get_db), user_id: int = None, user: schema.UserIn = Depends()):
	return service.update_user(db, user_id, user)


@router.patch('/{user_id}', response_model=schema.UserOut)
def patch_user(db: Session = Depends(get_db),
               user_id: int = Path(None, title="User id", description="User identification"),
               user: schema.UserPatch = Body(...)):
	return service.patch_user(db, user_id, user)


@router.delete('/{user_id}', dependencies=[Depends(oauth2_scheme)])
def delete_user(db: Session = Depends(get_db), user_id: int = None):
	return service.delete_user(db, user_id)


@router.post('/login', response_model=auth_schema.TokenData)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = auth_service.authenticate_user(db, form)
	if not user:
		raise HTTPException(status_code=404, detail="Incorrect email or password", headers={"Authorization": "Bearer"})
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = auth_service.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
	return {"access_token": access_token, "token_expire": access_token_expires, "token_type": "Bearer", "user": user}
