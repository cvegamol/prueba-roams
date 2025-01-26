# API de Hipotecas y Clientes

Esta es una API para la gestión de clientes y sus hipotecas, desarrollada con FastAPI y utilizando SQLite como base de datos.

## Descripción

La API permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre clientes, así como gestionar hipotecas asociadas a dichos clientes. La documentación de la API se genera automáticamente utilizando Swagger y ReDoc.

## Requisitos

- Python 3.8 o superior

## Instalación

1. Clona el repositorio:
    ```bash
    git clone 
    cd 
    ```

2. Crea un entorno virtual y actívalo:
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración de la Base de Datos

1. Crea la base de datos SQLite ejecutando el archivo `database.py`:
    ```bash
    python database.py
    ```

   Este archivo creará la base de datos `clientes.db` en el directorio actual.

## Ejecución

1. Inicia la aplicación:
    ```bash
    uvicorn main:app --reload
    ```

2. Abre tu navegador y ve a `http://localhost:8000/docs` para ver la documentación interactiva de Swagger, o a `http://localhost:8000/redoc` para ver la documentación generada con ReDoc.

## Endpoints

- `POST /clientes`: Crea un nuevo cliente.
- `GET /clientes/{dni}`: Obtén los detalles de un cliente utilizando su DNI.
- `PUT /clientes/{dni}`: Actualiza los datos de un cliente existente utilizando su DNI.
- `DELETE /clientes/{dni}`: Elimina un cliente existente utilizando su DNI.
- `POST /hipotecas`: Crea una hipoteca para un cliente existente.


