from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLACLEHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# load_dotenv()
# SQLACLEHEMY_DATABASE_URL = getenv("SQL_DATABASE_URL")

engine = create_engine(SQLACLEHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
