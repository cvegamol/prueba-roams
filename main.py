from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
from database import init_db
from models import database, clientes, hipotecas

app = FastAPI(title="API de Hipotecas y Clientes", description="Documentación de la API utilizando Swagger", version="1.0.0")

# Clase base para Cliente con validación de DNI
class ClienteBase(BaseModel):
    nombre: str
    dni: str
    email: str
    capital_solicitado: float

    # Validador de Pydantic para comprobar el DNI
    @validator('dni')
    def validar_dni(cls, dni):
        if not comprobar_dni(dni):
            raise ValueError('DNI inválido')
        return dni

# Clase para la creación de Cliente
class ClienteCreate(ClienteBase):
    pass

# Clase para Cliente con ID incluido
class Cliente(ClienteBase):
    id: int

# Clase base para Hipoteca con validación de DNI
class HipotecaBase(BaseModel):
    dni: str
    tae: float
    plazo: int

    # Validador de Pydantic para comprobar el DNI
    @validator('dni')
    def validar_dni(cls, dni):
        if not comprobar_dni(dni):
            raise ValueError('DNI inválido')
        return dni

# Clase para la creación de Hipoteca
class HipotecaCreate(HipotecaBase):
    pass

# Función que se ejecuta al inicio de la aplicación
@app.on_event("startup")
async def startup():
    init_db()
    await database.connect()

# Función que se ejecuta al apagar la aplicación
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Endpoint para crear un nuevo cliente
@app.post("/clientes", response_model=Cliente, summary="Crear Cliente", description="Crea un nuevo cliente con los datos proporcionados.")
async def crear_cliente(cliente: ClienteCreate):
    try:
        query = clientes.insert().values(
            nombre=cliente.nombre,
            dni=cliente.dni,
            email=cliente.email,
            capital_solicitado=cliente.capital_solicitado
        )
        last_record_id = await database.execute(query)
        return {**cliente.dict(), "id": last_record_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Función para comprobar si un DNI es válido
def comprobar_dni(dni:str)->bool:
    # Comprobamos que el tamaño del dni es el correcto
    if len(dni) != 9:
        return False

    # Dividimos en numeros y letra
    numeros = dni[:-1]
    letra = dni[-1]
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"

    # Comprobamos que los primeros 8 caracteres son dígitos
    if not numeros.isdigit():
        return False

    # Calculamos la letra correspondiente al número
    indice = int(numeros) % 23
    letra_correcta = letras[indice]

    # Comprobar si la letra es correcta
    return letra.upper() == letra_correcta

# Endpoint para obtener un cliente por su DNI
@app.get("/clientes/{dni}", response_model=Cliente, summary="Obtener Cliente", description="Obtén los detalles de un cliente utilizando su DNI.")
async def obtener_cliente(dni: str):
    query = clientes.select().where(clientes.c.dni == dni)
    cliente = await database.fetch_one(query)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Endpoint para actualizar un cliente por su DNI
@app.put("/clientes/{dni}", response_model=Cliente, summary="Actualizar Cliente", description="Actualiza los datos de un cliente existente utilizando su DNI.")
async def actualizar_cliente(dni: str, cliente: ClienteCreate):
    query = clientes.update().where(clientes.c.dni == dni).values(
        nombre=cliente.nombre,
        email=cliente.email,
        capital_solicitado=cliente.capital_solicitado
    )
    await database.execute(query)
    return {**cliente.dict(), "dni": dni}

# Endpoint para eliminar un cliente por su DNI
@app.delete("/clientes/{dni}", summary="Eliminar Cliente", description="Elimina un cliente existente utilizando su DNI.")
async def eliminar_cliente(dni: str):
    query = clientes.delete().where(clientes.c.dni == dni)
    await database.execute(query)
    return {"message": "Cliente eliminado exitosamente"}

# Endpoint para crear una nueva hipoteca
@app.post("/hipotecas", summary="Crear Hipoteca", description="Crea una hipoteca para un cliente existente.")
async def crear_hipoteca(hipoteca: HipotecaCreate):
    query_cliente = clientes.select().where(clientes.c.dni == hipoteca.dni)
    cliente = await database.fetch_one(query_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cuota, total = calcular_cuota(cliente["capital_solicitado"], hipoteca.tae, hipoteca.plazo)

    query_hipoteca = hipotecas.insert().values(
        tae=hipoteca.tae,
        plazo=hipoteca.plazo,
        cuota_mensual=cuota,
        total_a_devolver=total,
        cliente_id=cliente["id"]
    )
    await database.execute(query_hipoteca)
    return {
        "cuota_mensual": cuota,
        "total_a_devolver": total
    }

# Función para calcular la cuota mensual y el total a devolver de una hipoteca
def calcular_cuota(capital, tae, plazo):
    i = tae / 100 / 12
    n = plazo * 12
    cuota = capital * i / (1 - (1 + i) ** -n)
    total_a_devolver = cuota * n
    return cuota, total_a_devolver

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8999)
