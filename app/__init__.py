import uvicorn
from fastapi import FastAPI

from app.routes.user import router as user_router
from app.ext.db import SessionLocal, engine
from app.models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["User"])

if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)
