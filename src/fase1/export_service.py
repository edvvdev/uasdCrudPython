# =====================================================================
# EXPORT SERVICE - Import/Export CSV y JSON
# =====================================================================

import json
from pathlib import Path
from typing import Optional
import pandas as pd
from sqlalchemy import create_engine
from src.config import Config


class ExportService:
    """Servicio para importación y exportación de datos en CSV y JSON."""

    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{Config.USER}:{Config.PASSWORD}@{Config.HOST}:{Config.PORT}/{Config.DATABASE}"
        )

    def _get_connection(self):
        """Obtiene conexión SQLAlchemy."""
        return self.engine.connect()

    def exportar_a_csv(self, nombre_tabla: str, ruta_destino: Optional[str] = None) -> str:
        """
        Exporta una tabla completa a archivo CSV.

        Args:
            nombre_tabla: Nombre de la tabla en la BD
            ruta_destino: Ruta del archivo (opcional, genera automático)

        Returns:
            Ruta del archivo exportado
        """
        if ruta_destino is None:
            ruta_destino = f"data/{nombre_tabla}.csv"

        with self._get_connection() as conn:
            df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)

        df.to_csv(ruta_destino, index=False, encoding='utf-8')
        print(f"[EXPORT CSV] Tabla '{nombre_tabla}' -> {ruta_destino}")
        return ruta_destino

    def exportar_a_json(self, nombre_tabla: str, ruta_destino: Optional[str] = None) -> str:
        """
        Exporta una tabla completa a archivo JSON.

        Args:
            nombre_tabla: Nombre de la tabla en la BD
            ruta_destino: Ruta del archivo (opcional, genera automático)

        Returns:
            Ruta del archivo exportado
        """
        if ruta_destino is None:
            ruta_destino = f"data/{nombre_tabla}.json"

        with self._get_connection() as conn:
            df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)

        lista_diccionarios = df.to_dict(orient="records")
        with open(ruta_destino, 'w', encoding='utf-8') as archivo:
            json.dump(lista_diccionarios, archivo, indent=4, ensure_ascii=False)

        print(f"[EXPORT JSON] Tabla '{nombre_tabla}' -> {ruta_destino}")
        return ruta_destino

    def importar_des_csv(self, ruta_archivo: str, nombre_tabla: str) -> bool:
        """
        Importa datos desde un archivo CSV a una tabla.

        Args:
            ruta_archivo: Ruta del archivo CSV
            nombre_tabla: Nombre de la tabla destino

        Returns:
            True si exitoso
        """
        try:
            df = pd.read_csv(ruta_archivo)
            with self._get_connection() as conn:
                df.to_sql(nombre_tabla, conn, if_exists='append', index=False)
            print(f"[IMPORT CSV] {ruta_archivo} -> tabla '{nombre_tabla}'")
            return True
        except Exception as e:
            print(f"[IMPORT CSV ERROR] {e}")
            return False

    def importar_des_json(self, ruta_archivo: str, nombre_tabla: str) -> bool:
        """
        Importa datos desde un archivo JSON a una tabla.

        Args:
            ruta_archivo: Ruta del archivo JSON
            nombre_tabla: Nombre de la tabla destino

        Returns:
            True si exitoso
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            df = pd.DataFrame(datos)
            with self._get_connection() as conn:
                df.to_sql(nombre_tabla, conn, if_exists='append', index=False)
            print(f"[IMPORT JSON] {ruta_archivo} -> tabla '{nombre_tabla}'")
            return True
        except Exception as e:
            print(f"[IMPORT JSON ERROR] {e}")
            return False
