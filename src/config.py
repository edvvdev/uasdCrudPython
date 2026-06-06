# =====================================================================
# CONFIGURACIÓN CENTRALIZADA
# =====================================================================
# Carga credenciales desde .env usando python-dotenv.
# Si no existe .env, usa valores por defecto para desarrollo local.

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    HOST = os.getenv("DB_HOST", "localhost")
    PORT = int(os.getenv("DB_PORT", 3306))
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "0000")
    DATABASE = os.getenv("DB_NAME", "sakila")

    @classmethod
    def to_dict(cls):
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "user": cls.USER,
            "database": cls.DATABASE,
        }
