import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

#INVESTIGAR ENGINE Y SESSIONLOCAL

DATABASE_URL = "postgresql+pg8000://postgres:root@localhost/todo_db"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

