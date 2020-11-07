import uvicorn
from fastapi import FastAPI

from app.routes import user as user_ns, workspace as workspace_ns
from app.ext.db import SessionLocal, engine
from app.models import user, workspace

workspace.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_ns.router, prefix="/user", tags=["User"])
app.include_router(workspace_ns.router, prefix="/workspace", tags=["Workspace"])

if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)
