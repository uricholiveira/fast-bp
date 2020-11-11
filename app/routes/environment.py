from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.ext.db import get_db
from app.models import environment as model
from app.schemas import environment as schema
from app.services import environment as service
from app.services.auth import oauth2_scheme

router = APIRouter()


@router.get('/', response_model=List[schema.EnvironmentOut])
def get_environments(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
	return service.get_environments(db, skip, limit)


@router.post('/', response_model=schema.EnvironmentOut)
def create_environment(db: Session = Depends(get_db), environment: schema.EnvironmentIn = Depends()):
	return service.create_environment(db, environment)


@router.get('/{environment_id}', response_model=schema.EnvironmentOut)
def get_environment_by_id(db: Session = Depends(get_db), environment_id: int = None):
	return service.get_environment_by_id(db, environment_id)


@router.get('/workspace/{workspace_id}', response_model=List[schema.EnvironmentOut])
def get_environment_by_workspace_id(db: Session = Depends(get_db), workspace_id: int = None):
	return service.get_environment_by_workspace_id(db, workspace_id)


@router.put('/{environment_id}', response_model=schema.EnvironmentOut)
def update_environment(
		db: Session = Depends(get_db), environment_id: int = None,
		environment: schema.EnvironmentIn = Depends()):
	return service.update_environment(db, environment_id, environment)


@router.patch('/{environment_id}', response_model=schema.EnvironmentOut)
def patch_environment(
		db: Session = Depends(get_db), environment_id: int = None,
		environment: schema.EnvironmentPatch = Depends()):
	return service.patch_environment(db, environment_id, environment)


@router.delete('/{environment_id}', dependencies=[Depends(oauth2_scheme)])
def delete_environment(db: Session = Depends(get_db), environment_id: int = None):
	return service.delete_environment(db, environment_id)


@router.post('/{environment_id}/user/{user_id}', tags=["User_Environment"])
def add_user_to_environment(db: Session = Depends(get_db), environment_id: int = None, user_id: int = None):
	return service.add_user_to_environment(db, environment_id, user_id)


@router.delete('/{environment_id}/user/{user_id}', tags=["User_Environment"], dependencies=[Depends(oauth2_scheme)])
def del_user_from_environment(db: Session = Depends(get_db), environment_id: int = None, user_id: int = None):
	return service.del_user_from_environment(db, environment_id, user_id)
