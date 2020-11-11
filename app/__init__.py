import uvicorn
from fastapi import FastAPI

from app.routes import user as user_ns, workspace as workspace_ns, environment as environment_ns
from app.ext.db import SessionLocal, engine, generate_models
from app.models import user, workspace, environment

generate_models()

app = FastAPI()

app.include_router(user_ns.router, prefix="/user", tags=["User"])
app.include_router(workspace_ns.router, prefix="/workspace", tags=["Workspace"])
app.include_router(environment_ns.router, prefix="/environment", tags=["Environment"])

if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)
