import tkinter as tk
from tkinter import ttk,PhotoImage
from jira import JIRA
import random
import time
import datetime
import threading
import os
from dotenv import load_dotenv
from PIL import Image
import pystray
from pystray import MenuItem as item, Icon

# Cargar las variables de entorno
load_dotenv()
jira_url = os.getenv('JIRA_URL')
jira_username = os.getenv('JIRA_USERNAME')
jira_token = os.getenv('JIRA_TOKEN')
id_user=os.getenv('ID_USER')
name_user=os.getenv('NAME_USER')
empresas_str = os.getenv('EMPRESAS')
empresas_list = empresas_str.split(',')
# Lista para almacenar los tickets abiertos
tickets_abiertos = []

# Función para crear y cerrar ticket
def gestionar_ticket():
    empresa = empresa_var.get()
    request_type = request_type_var.get()

    request_type_id = ''
    if request_type == 'REPORTES':
        request_type_id = '55'
    elif request_type == 'PAGO':
        request_type_id = '31'
    elif request_type == 'BASE':
        request_type_id = '32'
    elif request_type == 'BASE y PAGOS':
        request_type_id = '32'
    elif request_type == 'SALDO':
        request_type_id = '31'
    elif request_type == 'Efectividades':
        request_type_id = '55'

    fecha_hoy = datetime.date.today().strftime('%m-%d')
    project_key = 'SOP'
    ticket_summary = f'{request_type} {empresa} {fecha_hoy}'
  
    issue_type_id = 10002

    jira_connection = JIRA(basic_auth=(jira_username, jira_token), server=jira_url)

    issue_dict = {
        'project': {'key': project_key},
        'summary': ticket_summary,
        'description': ticket_summary,
        'issuetype': {'id': issue_type_id},
        'customfield_10010': request_type_id,
        'customfield_10085': [{'id': id_user, 'value': name_user}],
        'customfield_10093': {'value': empresa},
    }

    new_issue = jira_connection.create_issue(fields=issue_dict)
    print(f"El ticket {new_issue.key} ha sido creado exitosamente.")
    
    # Agregar ticket a la lista
    tickets_abiertos.append(new_issue.key)
    actualizar_lista_tickets()

    ticket = jira_connection.issue(new_issue)
    transition_id = jira_connection.find_transitionid_by_name(ticket, 'En curso')
    jira_connection.transition_issue(ticket, transition_id)

    random_minutes = random.uniform(7, 11)
    print(f"Esperando {random_minutes:.2f} minutos para cerrar el ticket...")
    time.sleep(random_minutes * 60)

    ticket_phrase = f'{request_type} {empresa}'
    issues_c = jira_connection.search_issues(f'summary ~ "{ticket_phrase}"', maxResults=1, fields="created")

    if len(issues_c) == 0:
        print('No se encontraron tickets con esa frase parcial')
    else:
        issue = issues_c[0]
        print(f'Cerrando ticket {issue.key}')
        jira_connection.transition_issue(issue, '961')
        print("El ticket ha sido cerrado.")
        
        # Eliminar ticket de la lista
        tickets_abiertos.remove(issue.key)
        actualizar_lista_tickets()

def gestionar_ticket_en_hilo():
    ticket_thread = threading.Thread(target=gestionar_ticket)
    ticket_thread.start()

# Función para salir del icono de la bandeja
def salir(icon, item):
    icon.stop()
    root.quit()
    root.destroy()

# Función para ocultar la ventana
def ocultar_ventana():
    root.withdraw()  # Ocultar la ventana principal

# Función para mostrar la ventana cuando se selecciona "Mostrar" o se hace clic en el icono
def mostrar_ventana(icon=None, item=None):
    root.deiconify()  # Mostrar la ventana principal
    root.lift()  # Traer la ventana al frente

# Función para crear el icono en la bandeja
def crear_icono():
    icon_image = Image.open("icono.png")
    menu = (item('Mostrar', mostrar_ventana), item('Salir', salir))
    icon = Icon("test_icon", icon_image, "Gestión de Tickets JIRA", menu)

    # Asociar el clic izquierdo con mostrar la ventana
    icon.run()

# Cuando la ventana se cierra, se minimiza en lugar de destruir
def cerrar_ventana():
    ocultar_ventana()

# Función para actualizar la lista de tickets
def actualizar_lista_tickets():
    lista_tickets.delete(1.0, tk.END)  # Limpiar el área de texto
    if tickets_abiertos:
        lista_tickets.insert(tk.END, "\n".join(tickets_abiertos))  # Insertar los tickets abiertos
    ajustar_alto_ventana()  # Ajustar la altura de la ventana

# Función para ajustar la altura de la ventana
def ajustar_alto_ventana():
    num_tickets = len(tickets_abiertos)
    # Ajustar la altura del área de texto según la cantidad de tickets
    altura = max(1, num_tickets)  # Al menos 1 fila
    lista_tickets.config(height=altura)

# Configurar la interfaz de usuario
root = tk.Tk()
root.title("Gestión de Tickets JIRA")

# # Configuración de fondo transparente (en sistemas Windows)
# root.attributes('-alpha', 0.9)  # Ajustar la opacidad (0.0 a 1.0)

# Asignar el evento de cierre para ocultar la ventana en lugar de cerrarla
root.protocol("WM_DELETE_WINDOW", cerrar_ventana)


icon_image_tk = PhotoImage(file="icono.png")
root.iconphoto(False, icon_image_tk)

# Variables para los dropdowns
empresa_var = tk.StringVar()
request_type_var = tk.StringVar()

# Etiquetas y campos
ttk.Label(root, text="Seleccione la empresa:").grid(row=0, column=0, padx=10, pady=10)
empresa_combo = ttk.Combobox(root, textvariable=empresa_var, state='readonly')
empresa_combo['values'] = empresas_list
empresa_combo.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(root, text="Seleccione el tipo de solicitud:").grid(row=1, column=0, padx=10, pady=10)
request_type_combo = ttk.Combobox(root, textvariable=request_type_var, state='readonly')
request_type_combo['values'] = ('SALDO', 'PAGO', 'BASE', 'BASE y PAGOS', 'REPORTES', 'Efectividades')
request_type_combo.grid(row=1, column=1, padx=10, pady=10)

# Botón para gestionar ticket
ttk.Button(root, text="Crear y cerrar ticket", command=gestionar_ticket_en_hilo).grid(row=2, columnspan=2, pady=20)

# Área de texto para mostrar los tickets abiertos

lista_tickets = tk.Text(root, width=20, height=2, bg=root.cget("bg"), relief="flat", borderwidth=0)
# lista_tickets = tk.Text(root, height=10, width=50)
lista_tickets.grid(row=3, columnspan=2, padx=10, pady=10)

# Crear el icono en la bandeja en un hilo separado
threading.Thread(target=crear_icono, daemon=True).start()

# Iniciar la interfaz
root.mainloop()
