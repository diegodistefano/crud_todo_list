import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import SessionLocal
from models.task_model import Task

db = SessionLocal()
task=[]

def get_all_tasks(db):
    return db.query(Task).all()

def create_task_bd(db, title: str, description: str = None, status: bool = False):
    task = Task(title=title, description=description, status=status)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_db(task):
    try:
        # task = db.query(Task).filter_by(id=id).first()
        db.commit()
        db.refresh(task)
    except Exception as e:
        print("❌ Error al actualizar del controller la tarea.", e)

def delete_task_db():
    try:
        task = db.query(Task).filter_by(id=id).first()
        db.delete(task)
        db.commit()
    except Exception as e:
        print("❌ Error al eliminar la tarea.", e)

def close_db():
    db.close()