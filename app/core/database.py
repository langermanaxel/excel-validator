from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

# =========================================================
# 📌 Configuración de base de datos
# =========================================================
# Obtenemos la configuración centralizada (URL de la DB)
# desde variables de entorno.
# Esto permite cambiar de SQLite a PostgreSQL sin tocar código.
settings = get_settings()


# =========================================================
# 📌 Engine de SQLAlchemy
# =========================================================
# El engine es el componente encargado de manejar la conexión
# con la base de datos.
#
# connect_args={"check_same_thread": False}:
# - Específico para SQLite
# - Permite usar la conexión en múltiples hilos
# - Necesario en aplicaciones web como FastAPI
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)


# =========================================================
# 📌 Session Factory
# =========================================================
# sessionmaker es una fábrica de sesiones.
# Cada sesión representa una "transacción" con la base de datos.
#
# Beneficios:
# - Permite manejar commits/rollbacks
# - Aísla operaciones entre requests
# - Facilita testing
SessionLocal = sessionmaker(bind=engine)


# =========================================================
# 📌 Base declarativa (ORM)
# =========================================================
# Base es la clase base para definir modelos ORM.
#
# Ejemplo:
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#
# Beneficio:
# - Permite mapear tablas a clases Python
# - Mejora legibilidad y mantenibilidad
Base = declarative_base()