from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.ext.db import get_db

from app.schemas import workspace as schema, auth as auth_schema
from app.services import workspace as service, auth as auth_service
from app.services.auth import oauth2_scheme

router = APIRouter()


@router.get('/', response_model=List[schema.WorkspaceOut])
def get_workspaces(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
	return service.get_workspaces(db, skip, limit)


@router.post('/', response_model=schema.WorkspaceOut)
def create_workspace(db: Session = Depends(get_db), workspace: schema.WorkspaceIn = None):
	return service.create_workspace(db, workspace)


@router.get('/{workspace_id}', response_model=schema.WorkspaceOut)
def get_workspace_by_id(db: Session = Depends(get_db), workspace_id: int = None):
	return service.get_workspace_by_id(db, workspace_id)


@router.put('/{workspace_id}', response_model=schema.WorkspaceOut)
def update_workspace(db: Session = Depends(get_db), workspace_id: int = None,
                     workspace: schema.WorkspaceIn = Depends()):
	return service.update_workspace(db, workspace_id, workspace)


@router.patch('/{workspace_id}', response_model=schema.WorkspaceOut)
def patch_workspace(db: Session = Depends(get_db), workspace_id: int = None, workspace: schema.WorkspaceIn = Depends()):
	return service.patch_workspace(db, workspace_id, workspace)


@router.delete('/{workspace_id}', dependencies=[Depends(oauth2_scheme)])
def delete_workspace(db: Session = Depends(get_db), workspace_id: int = None):
	return service.delete_workspace(db, workspace_id)


@router.post('/{workspace_id}/user/{user_id}', tags=['User_Workspace'])
def add_user_to_workspace(db: Session = Depends(get_db), workspace_id: int = None, user_id: int = None):
	return service.add_user_to_workspace(db, workspace_id, user_id)


@router.delete('/{workspace_id}/user/{user_id}', tags=['User_Workspace'], dependencies=[Depends(oauth2_scheme)])
def del_user_from_workspace(db: Session = Depends(get_db), workspace_id: int = None, user_id: int = None):
	return service.del_user_from_workspace(db, workspace_id, user_id)