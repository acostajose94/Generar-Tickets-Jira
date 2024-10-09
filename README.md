# Gestión de Tickets JIRA

Este proyecto es una aplicación de escritorio para gestionar tickets de JIRA utilizando una interfaz gráfica creada con `Tkinter`. Permite crear y cerrar tickets automáticamente, ocultar la ventana en la bandeja del sistema, y gestionar múltiples tickets abiertos.

## Funcionalidades

- **Crear y Cerrar Tickets:** Crea tickets en JIRA basados en la empresa y tipo de solicitud seleccionados. Los tickets se cierran automáticamente después de un tiempo aleatorio (entre 7 y 11 minutos).
- **Bandeja del Sistema:** La aplicación puede minimizarse a la bandeja del sistema y restaurarse desde allí.
- **Lista de Tickets Abiertos:** Muestra los tickets que están abiertos y los actualiza en tiempo real.

## Requisitos

- Python 3.x
- Las siguientes librerías deben estar instaladas:

```bash
    pip install jira tkinter Pillow pystray python-dotenv
```

- Un archivo `.env` con las siguientes variables:

```bash
    JIRA_URL=https://tu-jira-url.com
    JIRA_USERNAME=tu_usuario_jira
    JIRA_TOKEN=tu_token_jira
    ID_USER=id_usuario_jira
    NAME_USER=nombre_usuario_jira
    EMPRESAS=Empresa1,Empresa2,Empresa3
```

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/tu_usuario/gestion-tickets-jira.git
    ```

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Configura el archivo `.env` en la raíz del proyecto con tus credenciales de JIRA y las empresas disponibles.

4. Coloca una imagen llamada `icono.png` en la carpeta raíz para el icono de la aplicación en la bandeja.

## Uso

1. Ejecuta la aplicación:

    ```bash
    python gestion_tickets.py
    ```

2. La interfaz mostrará un combo para seleccionar la empresa y el tipo de solicitud. Haz clic en el botón **Crear y cerrar ticket** para iniciar el proceso.

3. Los tickets abiertos se mostrarán en una lista dentro de la interfaz.

4. Para minimizar la aplicación a la bandeja del sistema, simplemente cierra la ventana. Puedes restaurarla haciendo clic en el icono de la bandeja.

## Estructura del Proyecto

- **`gestion_tickets.py`:** El script principal que gestiona la creación y cierre de tickets.
- **`.env`:** Archivo de configuración que almacena las credenciales de JIRA y la lista de empresas.
- **`icono.png`:** Imagen utilizada para el icono de la bandeja del sistema.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
