from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union, List

from app.models import environment as model, user as user_model, workspace as workspace_model
from app.schemas import environment as schema, user as user_schema
from app.services import user as user_service, workspace as workspace_service


def get_environments(db: Session, skip: int, limit: int):
	return db.query(model.Environment).offset(skip).limit(limit).all()


def get_environment_by_id(db: Session, environment_id: int) -> Union[model.Environment, HTTPException]:
	environment = db.query(model.Environment).filter(model.Environment.id == environment_id).first()
	if not environment:
		raise HTTPException(status_code=404, detail="Environment not found")
	return environment


def get_environment_by_workspace_id(db: Session, workspace_id: int) -> Union[List[model.Environment], HTTPException]:
	workspace = workspace_service.get_workspace_by_id(db, workspace_id)
	environment = db.query(model.Environment).filter(model.Environment.workspace_id == workspace.id).all()
	return environment


def create_environment(db: Session, environment: schema.EnvironmentIn) -> Union[
	model.Environment, HTTPException]:
	is_invalid = db.query(model.Environment).filter(
		model.Environment.name == environment.name,
		model.Environment.workspace_id == environment.workspace_id).first()
	if is_invalid:
		raise HTTPException(status_code=400, detail="Workspace already have a environment with this name")
	new_environment = model.Environment(**environment.dict())
	db.add(new_environment)
	db.commit()
	db.refresh(new_environment)
	return new_environment


def update_environment(db: Session, environment_id: int, environment: schema.EnvironmentIn) -> Union[
	model.Environment, HTTPException]:
	new_environment = get_environment_by_id(db, environment_id)
	for field in environment.dict():
		setattr(new_environment, field, environment.dict()[field])
	db.add(new_environment)
	db.commit()
	db.refresh(new_environment)
	return new_environment


def patch_environment(db: Session, environment_id: int, environment: schema.EnvironmentPatch) -> Union[
	model.Environment, HTTPException]:
	new_environment = get_environment_by_id(db, environment_id)
	data = environment.dict(exclude_none=True, exclude_unset=True)
	for field in data:
		setattr(new_environment, field, data[field])
	db.add(new_environment)
	db.commit()
	db.refresh(new_environment)
	return new_environment


def delete_environment(db: Session, environment_id: int) -> Union[JSONResponse, HTTPException]:
	environment = get_environment_by_id(db, environment_id)
	db.delete(environment)
	db.commit()
	return JSONResponse(status_code=200, content={"detail": "Environment deleted!"})


def add_user_to_environment(db: Session, environment_id: int, user_id: int) -> Union[JSONResponse, HTTPException]:
	user = user_service.get_user_by_id(db, user_id)
	environment = get_environment_by_id(db, environment_id)
	is_invalid = db.query(model.EnvironmentUserWorkspace).filter(
		model.EnvironmentUserWorkspace.user_id == user.id,
		model.EnvironmentUserWorkspace.environment_id == environment.id).first()
	if is_invalid:
		raise HTTPException(status_code=409, detail="User already in environment")

	user_environment = model.EnvironmentUserWorkspace(user_id=user.id, environment_id=environment.id)
	db.add(user_environment)
	db.commit()
	db.refresh(user_environment)
	return JSONResponse(status_code=200, content={"detail": "User added to Environment"})


def del_user_from_environment(db: Session, environment_id: int, user_id: int) -> Union[JSONResponse, HTTPException]:
	user = user_service.get_user_by_id(db, user_id)
	environment = get_environment_by_id(db, environment_id)
	user_environment = db.query(model.EnvironmentUserWorkspace).filter(
		model.EnvironmentUserWorkspace.user_id == user.id,
		model.EnvironmentUserWorkspace.environment_id == environment.id).first()
	if not user_environment:
		raise HTTPException(status_code=404, detail="User not found in this environment")
	db.delete(user_environment)
	db.commit()
	return JSONResponse(status_code=200, content={"detail": "User removed from Environment"})
