import logging
import os
from app import models
from dynaconf import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.getLogger().setLevel('INFO')

check_same_thread = False if str(settings.SQLALCHEMY_URL).startswith("sqlite") else True
engine = create_engine(settings.SQLALCHEMY_URL, connect_args={"check_same_thread": check_same_thread})

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


# Handler db method
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# Generate all models
def generate_models():
	logging.info("Creating database models...")
	models.user.Base.metadata.create_all(bind=engine)
	models.workspace.Base.metadata.create_all(bind=engine)
	models.environment.Base.metadata.create_all(bind=engine)
	logging.info("Database models created!")
