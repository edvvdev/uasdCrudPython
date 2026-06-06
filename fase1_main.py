# =====================================================================
# MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
# FASE I: ENTORNO PYTHON - REFACTORIZADO Y BLINDADO CONTRA ERRORES
# =====================================================================

import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import json

# ---------------------------------------------------------------------
# CONFIGURACIÓN DE LA CONEXIÓN (CONECTOR NATIVO)
# ---------------------------------------------------------------------
def obtener_conexion():
    """Establece una sesión de conexión segura con el motor local de MySQL."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,          
            user="root",        # Modifica si tu usuario difiere
            password="8095224147Gael",# Modifica con tu contraseña real de MySQL
            database="sakila"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[ERROR] No se pudo conectar al DBMS: {e}")
        return None

# ---------------------------------------------------------------------
# 1. COMPONENTE: OPERACIONES CRUD (A nivel de Query Parametrizado)
# ---------------------------------------------------------------------

def crud_crear_pais(nombre_pais):
    conn = obtener_conexion()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO country (country) VALUES (%s)", (nombre_pais,))
        conn.commit()
        print(f"[CREATE] Pais '{nombre_pais}' insertado correctamente.")
    except Error as e:
        # Aquí atrapamos el IntegrityError de duplicados sin romper el programa
        print(f"[CREATE INFO] Restriccion UNIQUE activada para '{nombre_pais}': {e.msg}")
    finally:
        cursor.close()
        conn.close()

def crud_leer_paises(limite=5):
    conn = obtener_conexion()
    if not conn: return
    print(f"\n[READ] Mostrando los ultimos {limite} paises en la BD:")
    df = pd.read_sql(f"SELECT * FROM country ORDER BY country_id DESC LIMIT {limite}", conn)
    print(df.to_string(index=False))
    conn.close()

def crud_crear_ciudad(nombre_ciudad, id_pais):
    conn = obtener_conexion()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO city (city, country_id) VALUES (%s, %s)", (nombre_ciudad, id_pais))
        conn.commit()
        print(f"[CREATE] Ciudad '{nombre_ciudad}' enlazada al pais ID {id_pais}.")
    except Error as e:
        print(f"[CREATE INFO] Restriccion de Ciudad activada: {e.msg}")
    finally:
        cursor.close()
        conn.close()

def crud_actualizar_tarifa_pelicula(id_pelicula, nueva_tarifa):
    conn = obtener_conexion()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE film SET rental_rate = %s WHERE film_id = %s", (nueva_tarifa, id_pelicula))
        conn.commit()
        print(f"[UPDATE] Pelicula ID {id_pelicula} actualizada con tarifa de ${nueva_tarifa}.")
    except Error as e:
        print(f"[UPDATE ERROR] No se pudo actualizar: {e.msg}")
    finally:
        cursor.close()
        conn.close()

def crud_eliminar_ciudad(id_ciudad):
    conn = obtener_conexion()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM city WHERE city_id = %s", (id_ciudad,))
        conn.commit()
        print(f"[DELETE] Ciudad con ID {id_ciudad} eliminada.")
    except Error as e:
        print(f"[DELETE INFO] Comportamiento FK esperado (No eliminada): {e.msg}")
    finally:
        cursor.close()
        conn.close()

# ---------------------------------------------------------------------
# 2. COMPONENTE: INTEROPERABILIDAD DE ARCHIVOS (Import/Export CSV & JSON)
# ---------------------------------------------------------------------

def exportar_a_csv(nombre_tabla, ruta_destino):
    conn = obtener_conexion()
    if not conn: return
    df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)
    df.to_csv(ruta_destino, index=False, encoding='utf-8')
    conn.close()
    print(f"[EXPORT CSV] Tabla '{nombre_tabla}' guardada en: {ruta_destino}")

def exportar_a_json(nombre_tabla, ruta_destino):
    conn = obtener_conexion()
    if not conn: return
    df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)
    
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)
            
    lista_diccionarios = df.to_dict(orient="records")
    with open(ruta_destino, 'w', encoding='utf-8') as archivo:
        json.dump(lista_diccionarios, archivo, indent=4, ensure_ascii=False)
    conn.close()
    print(f"[EXPORT JSON] Tabla '{nombre_tabla}' guardada en: {ruta_destino}")

# ---------------------------------------------------------------------
# 3. COMPONENTE: MATRICES Y ESTADÍSTICA DESCRIPTIVA (Data Science)
# ---------------------------------------------------------------------

def calcular_metricas_descriptivas():
    conn = obtener_conexion()
    if not conn: return
    df = pd.read_sql("SELECT length, replacement_cost FROM film", conn)
    conn.close()
    
    print("\n" + "="*50)
    print("      REPORTING ESTADISTICO DE VARIABLES (FILM)      ")
    print("="*50)
    
    variables = {'length': 'Duracion (Minutos)', 'replacement_cost': 'Costo de Reemplazo ($)'}
    
    for var_name, var_label in variables.items():
        datos = df[var_name].dropna().to_numpy()
        
        media = np.mean(datos)
        rango = np.ptp(datos) 
        desviacion = np.std(datos, ddof=1)
        varianza = np.var(datos, ddof=1)
        
        print(f"\n Variable: {var_label}")
        print(f"  * Media (Promedio):  {media:.4f}")
        print(f"  * Rango (Max - Min): {rango:.4f}")
        print(f"  * Desviacion Std:    {desviacion:.4f}")
        print(f"  * Varianza Muestral: {varianza:.4f}")

    matriz_cov = np.cov(df['length'], df['replacement_cost'], ddof=1)
    covarianza = matriz_cov[0, 1]
    
    print("\n ANALISIS DE COVARIANZA")
    print(f"  * Covarianza Computada: {covarianza:.4f}")
    if covarianza > 0:
        print("    [Interpretacion]: Relacion lineal positiva directa.")
    else:
        print("    [Interpretacion]: No posee co-dependencia lineal positiva.")
    print("="*50 + "\n")

# ---------------------------------------------------------------------
# ORQUESTADOR DE PROCESOS
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("=== PROCESANDO VALIDACION DE LA FASE I ===")
    
    # 1. Probar Escritura/Lectura CRUD con control de errores
    crud_crear_pais("Brasil")
    crud_crear_pais("Brasil") # Forzar el duplicado para validar la restricción en consola
    
    # Intentamos insertar vinculando a un ID de país válido (por ejemplo, el 1)
    crud_crear_ciudad("Rio de Janeiro", 1) 
    crud_actualizar_tarifa_pelicula(1, 4.99)
    crud_leer_paises(3)
    crud_eliminar_ciudad(1)
    
    # 2. Almacenamiento de Archivos (I/O)
    exportar_a_csv("film", "peliculas_fase1.csv")
    exportar_a_json("city", "ciudades_fase1.json")
    
    # 3. Analítica Descriptiva
    calcular_metricas_descriptivas()
    
    print("--- FASE I COMPLETADA CON EXITO ---")