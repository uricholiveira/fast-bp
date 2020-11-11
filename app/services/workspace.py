from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union

from app.models import workspace as model, user as user_model
from app.schemas import workspace as schema, user as user_schema
from app.services import user as user_service


def get_workspaces(db: Session, skip: int, limit: int) -> model.Workspace:
	return db.query(model.Workspace).offset(skip).limit(limit).all()


def get_workspace_by_id(db: Session, id: int) -> Union[model.Workspace, HTTPException]:
	workspace = db.query(model.Workspace).filter(model.Workspace.id == id).first()
	if not workspace:
		raise HTTPException(status_code=404, detail="Workspace not found")
	return workspace


def create_workspace(db: Session, workspace: schema.WorkspaceBase) -> Union[model.Workspace, HTTPException]:
	is_invalid = db.query(model.Workspace).filter(model.Workspace.name == workspace.name).first()
	if is_invalid:
		raise HTTPException(status_code=400, detail="A Workspace with same name already exists")
	new_workspace = model.Workspace(**workspace.dict())
	db.add(new_workspace)
	db.commit()
	db.refresh(new_workspace)
	return new_workspace


def update_workspace(db: Session, workspace_id: int, workspace: schema.WorkspaceIn) \
		-> Union[model.Workspace, HTTPException]:
	new_workspace = get_workspace_by_id(db, workspace_id)
	for field in workspace.dict(exclude_none=True, exclude_unset=True):
		setattr(new_workspace, field, workspace.dict()[field])
	db.add(new_workspace)
	db.commit()
	db.refresh(new_workspace)
	return new_workspace


def patch_workspace(db: Session, workspace_id: int, workspace: schema.WorkspaceIn) \
		-> Union[model.Workspace, HTTPException]:
	new_workspace = get_workspace_by_id(db, workspace_id)
	data = workspace.dict(exclude_unset=True, exclude_none=True)
	for field in data:
		setattr(new_workspace, field, data[field])
	db.add(new_workspace)
	db.commit()
	db.refresh(new_workspace)
	return new_workspace


def delete_workspace(db: Session, workspace_id: int) -> Union[JSONResponse, HTTPException]:
	workspace = get_workspace_by_id(db, workspace_id)
	db.delete(workspace)
	db.commit()
	return JSONResponse(status_code=200, content={"detail": "Workspace deleted"})


def add_user_to_workspace(db: Session, workspace_id: int, user_id: int) -> Union[HTTPException, JSONResponse]:
	user = user_service.get_user_by_id(db, user_id)
	workspace = get_workspace_by_id(db, workspace_id)
	is_invalid = db.query(model.UserWorkspace).filter(
		model.UserWorkspace.user_id == user.id,
		model.UserWorkspace.workspace_id == workspace.id).first()
	if is_invalid:
		raise HTTPException(status_code=409, detail="User already in this workspace")
	user_workspace = model.UserWorkspace(user_id=user.id, workspace_id=workspace.id)
	db.add(user_workspace)
	db.commit()
	db.refresh(user_workspace)
	return JSONResponse(status_code=404, content={"detail": "User added to Workspace"})


def del_user_from_workspace(db: Session, workspace_id: int, user_id: int) -> Union[HTTPException, JSONResponse]:
	user = user_service.get_user_by_id(db, user_id)
	workspace = get_workspace_by_id(db, workspace_id)
	user_workspace = db.query(model.UserWorkspace).filter(
		model.UserWorkspace.user_id == user.id,
		model.UserWorkspace.workspace_id == workspace.id).first()
	if not user_workspace:
		raise HTTPException(status_code=404, detail="User not found in this workspace")
	db.delete(user_workspace)
	db.commit()
	return JSONResponse(status_code=200, content={"detail": "User removed from Workspace"})
