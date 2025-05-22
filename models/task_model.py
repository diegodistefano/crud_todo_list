import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)  #INDEX
    title = Column(String, nullable=False)
    description = Column(String) 
    status = Column(Boolean, nullable=False)