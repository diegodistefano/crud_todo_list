import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.task_controller import create_task_bd, get_all_tasks
from controllers.task_controller import update_task_db, delete_task_db, close_db
from controllers.task_controller import task, db
from models.task_model import Task

menu = [
    "1. ✏️ Crear tarea",
    "2. 📄 Ver todas las tareas",
    "3. 🔍 Ver tarea por ID",
    "4. 🔄 Actualizar tarea",
    "5. 🗑️ Eliminar tarea",
    "6. 🚪 Salir"
]

def init_menu():
    print("\n=====📋 BIENVENID@S AL GESTOR DE TAREAS 📋=====")
    print("\n===🔹 Ya no podras olvidar tus pendientes 🔹===\n")
    display_menu()

def ask_status_input(ask_input):
    while True:
        status_input=input(f"❔ {ask_input} (S/N): ")
        if status_input.strip().upper() == "S":
            return True
        elif status_input.strip().upper() == "N":
            return False
        else:
            print("⚠️ Por favor, ingresa 'S' para sí o 'N' para no.")   

def display_create_task():
    try:
        print("\n=====🔹 CREAR NUEVA TAREA 🔹=====")
        title=input("\n👉 Ingresa el título de la tarea: ")
        description=input("👉 Ingresa la descripción: ")
        status=ask_status_input("La tarea está finalizada?")
        task.append({
            "title":title,
            "description":description,
            "status":status})
        create_task_bd(db, title, description, status)
    except Exception as e:
        print("❌  Error al Crear la tarea.", e)

def show_tasks():   
    try:
        try:
            print("\n=====🔹 LISTA DE TAREAS 🔹=====\n")
            tasks = get_all_tasks(db)
        except:
            print(f"❌ Error al mostrar las tareas.")
        if not tasks:
            print("No hay tareas registradas.")
        else:
            for task in tasks:
                status_str = "Finalizada" if task.status else "Pendiente"
                description_str = task.description if task.description else "N/A"
                print(
                    f"  🆔 ID: {str(task.id).ljust(6)} "
                    f"📝 Título: {task.title.ljust(25)} "
                    f"📃 Descripción: {description_str.ljust(50)} "
                    f"📌 Estado: {status_str.ljust(10)}"
                )

        print("\n")           
    except Exception as e:
        print(f"❌ Error al mostrar las tareas: {e}")

def search_by_id():
    try:
        print("\n-------------------------------\n")
        search=int(input("🔎 Ingrese un ID: "))
        tasks = get_all_tasks(db)
        if not tasks:
            print("⚠️  No se encontró la tarea con ese ID.")
        else:
            for task in tasks:
                if (search == task.id):
                    status_str = "Finalizada" if task.status else "Pendiente"
                    description_str = task.description if task.description else "N/A"
                    print(
                        f"  🆔 ID: {str(task.id).ljust(6)} "
                        f"📝 Título: {task.title.ljust(25)} "
                        f"📃 Descripción: {description_str.ljust(50)} "
                        f"📌 Estado: {status_str.ljust(10)}"
                    )
        return task.id
    except:
        print("❌  Error al buscar una tarea.")

def update_task():
    try:
        try:
            task_id = search_by_id()
            task = db.query(Task).filter_by(id=task_id).first()
        except:
            print("❌ Error al buscar un ID")
        if task is None:
            print("⚠️  No se encontró la tarea con ese ID.")
            return
        print("\n=====🔹 ACTUALIZAR UNA TAREA 🔹=====")
        while True:
            condition =input("❔ ¿Desea actualizar unicamente el Estado? (S/N): ")
            if condition.strip().upper() == "S":
                task.status = not task.status
                break
            elif condition.strip().upper() == "N":
                task.title=input("\n👉 Ingresa el nuevo título de la tarea: ")
                task.description=input("👉 Ingresa la nueva descripción: ")
                task.status=ask_status_input("La tarea está finalizada?")   
                break
            else:
                print("⚠️ Por favor, ingresa 'S' para sí o 'N' para no.") 
        update_task_db(task)
        print("\n ✅ La tarea fue actualizada con exito.")

    except Exception as e:
        print("❌ Error al actualizar la tarea del view.", e)


def delete_task():
    try:
        delete_task_db()
        print("✅ Tarea eliminada con éxito.")
    except Exception as e:
        print("❌ Error en delete:", e)

def exit_task():
    status=ask_status_input("Quiere salir de la aplicación?")
    if status:
        close_db()
        print("Vuelve pronto!")
    else:
        display_menu()
        
def display_menu():
    try:
        for option in menu:
            print(option)
        menu_select=int(input("\n🟢 Ingrese el numero de la opcion deseada: "))
        match menu_select:
            case 1:
                display_create_task()
            case 2:
                show_tasks()
            case 3:
                search_by_id()
            case 4:
                update_task()
            case 5:
                delete_task_db()
            case 6:
                exit_task()
            case _:
                print("⚠️  Opcion invalida. Seleccione una opcion correcta.")
    except:
        print("❌  Error de excepcion en display_menu")
    finally:
        if (menu_select!=6):
            display_menu()

init_menu()


#TAREAS PENDIENTES (MINI-JIRA)

# MODIFICAR STATUS SOLO V
# SALIR DEL PROGRAMA v
# CERRAR LA BD v
# contextmanager de Python (investigar)
# MODULARIZAR FUNCIONES v
# COMENTARIOS SEGUN ENUNCIADO
# persistencia de ID

#Que metodos corresponden a controller y cuales a models
