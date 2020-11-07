from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union

from app.models import workspace as model
from app.schemas import workspace as schema


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


def delete_workspace(db: Session, workspace_id: int) -> JSONResponse:
	workspace = get_workspace_by_id(db, workspace_id)
	db.delete(workspace)
	db.commit()
	return JSONResponse(status_code=200, content={"detail": "Workspace deleted"})
