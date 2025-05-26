import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers import create_task_db, get_all_tasks, update_status_db
from controllers import update_task_db, delete_task_db, close_db, get_task_by_id

menu = [
    "=====🟦 LISTADO DE OPCIONES 🟦=====\n",
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

def show_task(task):
    status_str = "Finalizada" if task.status else "Pendiente"
    description_str = task.description if task.description else "N/A"
    print_task(task, description_str, status_str)

def separation():
    print("\n-------------------------------\n")

def ask_status_input(ask_input):
    while True:
        status_input = input(f"❔ {ask_input} (S/N): ").strip().upper()
        if status_input == "S":
            return True
        elif status_input == "N":
            return False
        else:
            print("⚠️ Por favor, ingresa 'S' para sí o 'N' para no.")   

def display_create_task():
    try:
        print("\n=====🔹 CREAR NUEVA TAREA 🔹=====")
        title=input("\n👉 Ingresa el título de la tarea: ").strip().capitalize()
        description=input("👉 Ingresa la descripción: ").strip().capitalize()
        status=ask_status_input("La tarea está finalizada?")
        create_task_db(title, description, status)
        print("\n✅ Nueva tarea creada con éxito.\n")
        separation()
    except Exception as e:
        print("❌  Error al Crear la tarea.", e)

def show_all_tasks():   
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
                show_task(task)       
        separation()  
    except Exception as e:
        print(f"❌ Error al mostrar las tareas: {e}")

def search_by_id():
    try:
        separation()
        search_id = int(input("🔎 Ingrese un ID: "))
        task = get_task_by_id(search_id)
        if task:
            separation()
            show_task(task)
            separation()
            return task.id
        else:
            print(f"El ID {search_id} no fue encontrado.")
            separation()
            return None
    except Exception as e:
        print(f"❌  Error al buscar una tarea: {e}")
        return None

def update_task():
    try:
        task_id = search_by_id() 

        if task_id is None:
            print("❌ No se encontró la tarea para actualizar.")
            return   
        print("\n=====🔹 ACTUALIZAR UNA TAREA 🔹=====")
        while True:
            condition = input("❔ ¿Actualizar unicamente el estado? (S/N): ").strip().upper()
            if condition == "S":
                if update_status_db(task_id):
                    print("\n✅ Estado actualizado con éxito.")
                    separation()
                else:
                    print("\n❌ No se pudo actualizar estado.\n")
                break
            elif condition == "N":
                current_task = get_task_by_id(task_id)
                if not current_task:
                    print(" No se pudo obtener la tarea actual.")
                    return
                title = input("\n👉 Ingresa el nuevo título de la tarea: ").strip().capitalize()
                description = input("👉 Ingresa la nueva descripción: ").strip().capitalize()
                status = ask_status_input("La tarea está finalizada?")
                if update_task_db(task_id, title, description, status):
                    print("\n ✅ La tarea fue actualizada con exito.")
                    separation()
                else:
                    print("❌ No se pudo actualizar la tarea.")
                    separation()
                break
            else:
                print("⚠️ Por favor, ingresa 'S' para sí o 'N' para no.")
    except Exception as e:
        print(f"❌ Error al actualizar la tarea: {e}")

def delete_task():
    task_id = search_by_id()
    if task_id is None:
        print("⚠️  No se encontró la tarea con ese ID.")
        separation()
        return       
    if ask_status_input("Desea eliminar esta tarea") is True:
        delete_task_db(task_id)
        print("\n✅ Tarea eliminada con éxito.")
        separation()
    else:
        separation()
        return

def exit_task():
    status = ask_status_input("Quiere salir de la aplicación?")
    if status:
        close_db()
        print("Vuelve pronto!")
    else:
        display_menu()
        
def display_menu():
    while True:
        for option in menu:
            print(option)
        menu_input = input("\n🟢 Ingrese el número de la opción deseada: ").strip()
        if not menu_input.isdigit():
            print("⚠️ Opción inválida. Ingrese un número válido.")
            continue
        menu_select = int(menu_input)
        match menu_select:
            case 1:
                display_create_task()
            case 2:
                show_all_tasks()
            case 3:
                search_by_id()
            case 4:
                update_task()
            case 5:
                delete_task()
            case 6:
                exit_task()
                break
            case _:
                separation()
                print("⚠️ Opción inválida. Seleccione una opción correcta.")
                separation()
