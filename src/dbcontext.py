# =====================================================================
# DBCONTEXT - Gestor de Conexiones y Transacciones
# =====================================================================
# Componente central del ORM nativo. Gestiona el ciclo de vida de las
# conexiones con el motor de base de datos MySQL.

import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Tuple


class DbContext:
    """
    Gestiona el ciclo de vida de las conexiones y transacciones con MySQL.
    Provee métodos para ejecutar comandos (INSERT/UPDATE/DELETE) y
    consultas (SELECT) de forma parametrizada.
    """

    def __init__(self):
        self.host: str = "localhost"
        self.port: int = 3306
        self.user: str = "root"
        self.password: str = "0000"
        self.database: str = "sakila"

    def _conectar(self):
        """Método privado para instanciar la conexión cruda del Driver."""
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def ejecutar_comando(self, query: str, params: tuple) -> Optional[int]:
        """
        Ejecuta operaciones de escritura (INSERT, UPDATE, DELETE) parametrizadas.

        Args:
            query: SQL query con placeholders %s
            params: Tupla con valores para el query

        Returns:
            lastrowid si exitoso, None si hay error de integridad
        """
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"  [DbContext Error] Restricción de Integridad activada: {e.msg}")
            return None
        finally:
            cursor.close()
            conn.close()

    def ejecutar_consulta(self, query: str, params: tuple = ()) -> List[Tuple]:
        """
        Ejecuta operaciones de lectura relacional (SELECT).

        Args:
            query: SQL query con placeholders %s
            params: Tupla con valores para el query

        Returns:
            Lista de tuplas con los resultados
        """
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"  [DbContext Error] Fallo en Query: {e.msg}")
            return []
        finally:
            cursor.close()
            conn.close()
