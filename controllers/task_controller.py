import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import SessionLocal
from models.task_model import Task

db = SessionLocal()
task=[]

def get_all_tasks():
    return db.query(Task).all()

def create_task_db(db, title: str, description: str = None, status: bool = False):
    task = Task(title=title, description=description, status=status)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task_by_id(id):
    try:
        return db.query(Task).filter(Task.id==id).first()
    except Exception as e:
        print("❌ Error al actualizar EL ID del controller get_task_by_id.", e)

def update_status_db(id):
    try:
        task=get_task_by_id(id)
        task.status = not task.status
        db.commit()
        db.refresh(task)
    except Exception as e:
        print("❌ Error al actualizar EL ID del controller update_status_db.", e)

# def update_task_db(task_id, title, description, status):
#     try:
#         task=get_task_by_id(task_id)
#         print(task)
#         task.title=title
#         task.description=description
#         task.status=status
#         db.commit()
#         db.refresh(task)
#     except Exception as e:
#         print("❌ Error al actualizar la tarea del controller.", e)

def update_task_db(task_id, title, description, status):
    try:
        task = get_task_by_id(task_id)
        if not task:
            print("⚠️ No se encontró la tarea con ese ID.")
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

def delete_task_db():
    try:
        task = db.query(Task).filter_by(id=id).first()
        db.delete(task)
        db.commit()
    except Exception as e:
        print("❌ Error al eliminar la tarea.", e)

def close_db():
    db.close()