import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.task_controller import create_task_db, get_all_tasks, update_status_db
from controllers.task_controller import update_task_db, delete_task_db, close_db, get_task_by_id
from controllers.task_controller import task, db
from models.task_model import Task

menu = [
    "1. ✏️  Crear tarea",
    "2. 📄 Ver todas las tareas",
    "3. 🔍 Ver tarea por ID",
    "4. 🔄 Actualizar tarea",
    "5. 🗑️  Eliminar tarea",
    "6. 🚪 Salir"
]

def init_menu():
    print(
        f"\n=====📋 BIENVENID@S AL GESTOR DE TAREAS 📋====="
        f"\n===🔹 Ya no podras olvidar tus pendientes 🔹===\n"
        )
    display_menu()

def print_task(task, description_str, status_str ):
    print(
            f"  🆔 ID: {str(task.id).ljust(6)} "
            f"📝 Título: {task.title.ljust(25)} "
            f"📃 Descripción: {description_str.ljust(50)} "
            f"📌 Estado: {status_str.ljust(10)}"
        )

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
        create_task_db(db, title, description, status)
        print("\n=====🔹 CREAR NUEVA TAREA 🔹=====")

    except Exception as e:
        print("❌  Error al Crear la tarea.", e)

def show_tasks():   
    try:
        try:
            print("\n=====🔹 LISTA DE TAREAS 🔹=====\n")
            tasks = get_all_tasks()
        except:
            print(f"❌ Error al mostrar las tareas.")
        if not tasks:
            print("No hay tareas registradas.")
        else:
            for task in tasks:
                status_str = "Finalizada" if task.status else "Pendiente"
                description_str = task.description if task.description else "N/A"
                print_task(task, description_str, status_str)           
    except Exception as e:
        print(f"❌ Error al mostrar las tareas: {e}")

def search_by_id():
    try:
        print("\n-------------------------------\n")
        search=int(input("🔎 Ingrese un ID: "))
        tasks = get_all_tasks()
        if not tasks:
            print("⚠️  No hay tareas registradas.")
            return
        
        # found_task = None
        for task in tasks:
            if (search == task.id):
                status_str = "Finalizada" if task.status else "Pendiente"
                description_str = task.description if task.description else "N/A"
                print(f"\n{print_task(task, description_str, status_str)}\n")
                found_task = task
                break
        
        # if found_task is None:
        #     print("⚠️  No se encontró la tarea con ese ID.")
        #     return
            
        return found_task.id
    except Exception as e:
        print(f"❌  Error al buscar una tarea: {e}")
        return None

def update_task():
    try:
        try:
            task_id = search_by_id()
        except:
            print("❌ Error al buscar un ID")
            return
        if task_id is None:
            print("⚠️  No se encontró la tarea con ese ID.")
            return       
        print("\n=====🔹 ACTUALIZAR UNA TAREA 🔹=====")
        
        while True:
            condition =input("❔ ¿Desea actualizar unicamente el Estado? (S/N): ")
            if condition.strip().upper() == "S":
                if update_status_db(task_id):
                    print("\n✅ El estado de la tarea fue actualizado con éxito.\n")
                else:
                    print("\n❌ No se pudo actualizar el estado de la tarea.\n")
                break
            elif condition.strip().upper() == "N":
                current_task = get_task_by_id(task_id)
                if not current_task:
                    print(" No se pudo obtener la tarea actual.")
                    return
                title=input("\n👉 Ingresa el nuevo título de la tarea: ")
                description=input("👉 Ingresa la nueva descripción: ")
                status=ask_status_input("La tarea está finalizada?")
                if update_task_db(task_id, title, description, status):
                    print("\n ✅ La tarea fue actualizada con exito.")
                else:
                    print("❌ No se pudo actualizar la tarea.")
                break
            else:
                print("⚠️ Por favor, ingresa 'S' para sí o 'N' para no.")
    except Exception as e:
        print(f"❌ Error al actualizar la tarea: {e}")

def delete_task():
    task_id = search_by_id()
    if task_id is None:
        print("⚠️  No se encontró la tarea con ese ID.")
        return       
    try:
        delete_task_db(task_id)
        print("\n✅ Tarea eliminada con éxito.\n")

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
                delete_task()
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
