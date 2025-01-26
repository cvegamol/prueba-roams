from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./clientes.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

def init_db():
    import models
    metadata.create_all(bind=engine)
