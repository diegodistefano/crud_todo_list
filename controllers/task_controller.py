import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import SessionLocal
from models import Task
from sqlalchemy import asc

db = SessionLocal()

def verify_task(task):
    if not task:
        print("❌ No se encontró la tarea.")
        return False
    return True 

def get_all_tasks():
    try:
        return db.query(Task).order_by(Task.id.asc()).all()
    except Exception as e:
        print("❌ Error al obtener el listado de tareas.", {e})
        return []

def create_task_db(title: str, description: str = None, status: bool = False):
    try:
        task = Task(title = title, description = description, status = status)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        print("❌ Error al crear la tarea.", e)
        return None

def get_task_by_id(id):
    try:
        return db.query(Task).filter(Task.id == id).first()
    except Exception as e:
        print("❌ Error al obtener el ID.", e)
        return None

def update_status_db(id):
    try:
        task = get_task_by_id(id)
        if not verify_task(task):
            return False
        task.status = not task.status
        db.commit()
        db.refresh(task)
        return True
    except Exception as e:
        print(f"❌ Error al actualizar el estado: {e}")
        return False

def update_task_db(task_id, title, description, status):
    try:
        task = get_task_by_id(task_id)
        if not verify_task(task):
            return False
        task.title = title
        task.description = description
        task.status = status  
        db.commit()
        db.refresh(task)
        return True
    except Exception as e:
        print(f"❌ Error al actualizar la tarea: {e}")
        return False

def delete_task_db(task_id):
    try:
        task = db.query(Task).filter_by(id = task_id).first()
        if not verify_task(task):
            return False
        db.delete(task)
        db.commit()
    except Exception as e:
        print("❌ Error al eliminar la tarea.", e)

def close_db():
    try:
        db.close()
    except Exception as e:
        print("❌ Error al intentar cerrar la base de datos.", e)
