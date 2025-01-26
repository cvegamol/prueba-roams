from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from databases import Database

from database import metadata, DATABASE_URL

database = Database(DATABASE_URL)
# Tabla Cliente
clientes = Table(
    "clientes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100), nullable=False),
    Column("dni", String(9), unique=True, nullable=False),
    Column("email", String(100), nullable=False),
    Column("capital_solicitado", Float, nullable=False),
)
# Tabla Hipotecas
hipotecas = Table(
    "hipotecas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tae", Float, nullable=False),
    Column("plazo", Integer, nullable=False),
    Column("cuota_mensual", Float, nullable=False),
    Column("total_a_devolver", Float, nullable=False),
    Column("cliente_id", Integer, ForeignKey("clientes.id"), nullable=False),
)
