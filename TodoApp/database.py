from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLACLEHEMY_DATABASE_URL = "sqlite:///./todos.db"

# FASTAPI can communicate with db via multiple threads, thus don't want to limit to one thread
engine = create_engine(SQLACLEHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
