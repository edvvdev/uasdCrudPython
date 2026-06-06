# Ensayo Técnico: CRUD/ORM Nativo en Python con Arquitectura MariaDB-Sakila

**Maestría en Ciencia de Datos e Inteligencia Artificial**
**INF-8237-C2: Ciencias de Datos 1**

**Autores**:
- Framiel Trinidad
- Edwing Perez
- Jharol Duran

**Universidad**: Universidad Autónoma de Santo Domingo (UASD)
**Profesora**: Silveria del Orbe Abad
**Fecha**: 5 de junio de 2026

---

## Resumen (250 palabras)

Este proyecto presenta una implementación de arquitectura CRUD/ORM nativo en Python orientado a la base de datos Sakila de MariaDB. La solución se estructura en dos fases complementarias: la primera establece operaciones básicas de creación, lectura, actualización y eliminación (CRUD) a nivel de queries SQL, complementadas con funcionalidades de importación/exportación en formatos CSV y JSON, además de métricas descriptivas fundamentales incluyendo media, rango, desviación estándar, varianza y covarianza. La segunda fase consolida una arquitectura ORM completa mediante el patrón DbContext que gestiona el ciclo de vida de conexiones y transacciones, entidades puras que mapean directamente las tablas del sistema gestor (CountryEntity, CityEntity, FilmEntity), un modelo de repositorio que transforma filas relacionales en colecciones tipadas List<Entity>, y un controlador de flujo (SakilaWorkflowController) que orquesta las operaciones de negocio. La arquitectura implementa constraints de integridad a nivel de base de datos incluyendo unique keys para evitar duplicados y foreign keys con políticas restrictivas. El código fuente está disponible públicamente en GitHub, facilitando la colaboración y revisión entre pares. Los resultados demuestran que es posible construir un ORM funcional sin依赖 de frameworks externos, achieving un control granular sobre las operaciones de base de datos while maintaining clean separation of concerns.

**Palabras clave**: ORM, CRUD, Python, MariaDB, Sakila, DbContext, Entity, Model

---

## 1. Introducción

### 1.1 Contexto del Proyecto

En el ámbito de la ingeniería de software moderna, la comunicación entre aplicaciones orientadas a objetos y sistemas de bases de datos relacionales representa un desafío técnico fundamental. El Object-Relational Mapping (ORM) emerge como la solución arquitectónica estándar para abstract esta brecha paradigmática, permitiendo que desarrolladores trabajen con objetos nativos del lenguaje mientras la persistencia se gestiona de manera transparente.

### 1.2 Objetivos

El presente proyecto tiene como objetivos:
1. Implementar operaciones CRUD básicas con queries SQL parametrizados
2. Desarrollar un ORM nativo basado en POO sin frameworks externos
3. Validar la integridad de datos mediante constraints de base de datos
4. Proporcionar interoperabilidad mediante import/export CSV y JSON
5. Calcular métricas descriptivas para análisis exploratorio de datos

---

## 2. Fase I: Consultas SQL y Operaciones CRUD

### 2.1 Estructura de la Base de Datos (DDL)

El script SQL crea la base de datos `sakila` con cuatro tablas principales: country, city, film e inventory. Cada tabla incluye constraints de integridad para garantizar la calidad de los datos.

```sql
CREATE TABLE country (
    country_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    country VARCHAR(50) NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (country_id),
    CONSTRAINT unique_country UNIQUE (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE city (
    city_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL,
    country_id SMALLINT UNSIGNED NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id),
    CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT unique_city_country UNIQUE (city, country_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE film (
    film_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(128) NOT NULL,
    description TEXT DEFAULT NULL,
    release_year YEAR DEFAULT NULL,
    rental_duration TINYINT UNSIGNED NOT NULL DEFAULT 3,
    rental_rate DECIMAL(4,2) NOT NULL DEFAULT 4.99,
    length SMALLINT UNSIGNED DEFAULT NULL,
    replacement_cost DECIMAL(5,2) NOT NULL DEFAULT 19.99,
    rating ENUM('G','PG','PG-13','R','NC-17') DEFAULT 'G',
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (film_id),
    CONSTRAINT unique_title_release UNIQUE (title, release_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 2.2 Conjunto de 10 Consultas Analíticas

#### Consulta 1: Películas con costo de reemplazo crítico
```sql
SELECT title, release_year, replacement_cost, rating
FROM film
WHERE replacement_cost > 15.00;
```
**Resultado**: Filtra películas cuyo costo de reemplazo excede $15.00, útil para identificar inventario de alto valor.

#### Consulta 2: Join de variables geográficas
```sql
SELECT ci.city_id, ci.city, co.country
FROM city ci
INNER JOIN country co ON ci.country_id = co.country_id;
```
**Resultado**: Combina ciudades con sus respectivos países para análisis geográfico.

#### Consulta 3: Densidad urbana por país
```sql
SELECT co.country, COUNT(ci.city_id) AS total_ciudades
FROM country co
LEFT JOIN city ci ON co.country_id = ci.country_id
GROUP BY co.country_id
ORDER BY total_ciudades DESC;
```
**Resultado**: Muestra la distribución de ciudades por país, ordenadas de mayor a menor.

#### Consulta 4: Duración promedio por clasificación
```sql
SELECT rating, ROUND(AVG(length), 2) AS duracion_promedio
FROM film
GROUP BY rating;
```
**Resultado**: Métrica agregada que relaciona clasificación de edad con duración de películas.

#### Consulta 5: Búsqueda indexada por patrones
```sql
SELECT film_id, title, rental_rate, rating
FROM film
WHERE title LIKE '%Matrix%' OR title LIKE '%Inception%';
```
**Resultado**: Búsqueda textual en títulos para casos de contingencia o búsqueda rápida.

#### Consulta 6: Inventario activo por tienda
```sql
SELECT i.inventory_id, f.title, i.store_id
FROM inventory i
JOIN film f ON i.film_id = f.film_id
WHERE i.store_id = 1;
```
**Resultado**: Auditoría de stock físico disponible en la Tienda 1.

#### Consulta 7: Filtro multidimensional
```sql
SELECT title, rental_rate, length
FROM film
WHERE rental_rate BETWEEN 3.00 AND 6.00 AND length > 120;
```
**Resultado**: Películas con tarifa media-alta y larga duración para análisis de segmentación.

#### Consulta 8: Control de volumen de inventario
```sql
SELECT f.title, COUNT(i.inventory_id) AS copias_disponibles
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
GROUP BY f.film_id;
```
**Resultado**: Volumen de copias disponibles por título, incluyendo películas sin inventario.

#### Consulta 9: Integridad de datos residuales
```sql
SELECT co.country
FROM country co
LEFT JOIN city ci ON co.country_id = ci.country_id
WHERE ci.city_id IS NULL;
```
**Resultado**: Identifica países sin ciudades asociadas (datos huérfanos).

#### Consulta 10: Máximo costo operativo
```sql
SELECT title, replacement_cost
FROM film
WHERE replacement_cost = (SELECT MAX(replacement_cost) FROM film);
```
**Resultado**: Subconsulta que identifica el registro con el mayor costo de reemplazo.

### 2.3 Implementación CRUD en Python

Las funciones CRUD en `fase1_main.py` implementan operaciones parametrizadas contra la base de datos:

```python
def crud_crear_pais(nombre_pais):
    conn = obtener_conexion()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO country (country) VALUES (%s)", (nombre_pais,))
        conn.commit()
        print(f"[CREATE] Pais '{nombre_pais}' insertado correctamente.")
    except Error as e:
        print(f"[CREATE INFO] Restriccion UNIQUE activada para '{nombre_pais}': {e.msg}")
    finally:
        cursor.close()
        conn.close()

def crud_leer_paises(limite=5):
    conn = obtener_conexion()
    if not conn: return
    df = pd.read_sql(f"SELECT * FROM country ORDER BY country_id DESC LIMIT {limite}", conn)
    print(df.to_string(index=False))
    conn.close()
```

### 2.4 Import/Export CSV y JSON

```python
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
```

### 2.5 Métricas Descriptivas

```python
def calcular_metricas_descriptivas():
    conn = obtener_conexion()
    if not conn: return
    df = pd.read_sql("SELECT length, replacement_cost FROM film", conn)
    conn.close()

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
    print(f"\n Covarianza Computada: {covarianza:.4f}")
```

**Evidencia de ejecución**: Los scripts producen salida console con logs de cada operación completada, confirmando la inserción, lectura, actualización y eliminación de registros.

---

## 3. Fase II: Arquitectura ORM

### 3.1 DbContext y ORM Framework (1 punto)

El componente `DbContext` actúa como el núcleo del ORM nativo, gestionando el ciclo de vida completo de las conexiones con el motor de base de datos MySQL:

```python
class DbContext:
    def __init__(self):
        self.host: str = "localhost"
        self.port: int = 3306
        self.user: str = "root"
        self.password: str = "0000"
        self.database: str = "sakila"

    def _conectar(self):
        return mysql.connector.connect(
            host=self.host, port=self.port, user=self.user,
            password=self.password, database=self.database
        )

    def ejecutar_comando(self, query: str, params: tuple) -> Optional[int]:
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

    def ejecutar_consulta(self, query: str, params: tuple = ()) -> List[tuple]:
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
```

**Framework elegido**: mysql-connector-python (conector nativo oficial de Oracle para MySQL). No se utilizó SQLAlchemy, Django ORM u otro framework externo para demostrar la construcción artesanal de un ORM.

### 3.2 Entity Objects (1 punto)

Las entidades representan el mapeo 1:1 con las tablas del DBMS, incluyendo todos los campos y tipos de datos correspondientes:

```python
class CountryEntity:
    def __init__(self, country_id: Optional[int], country: str, last_update: Optional[str] = None):
        self.country_id: Optional[int] = country_id
        self.country: str = country
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<Entity.Country id={self.country_id} name='{self.country}'>"

class CityEntity:
    def __init__(self, city_id: Optional[int], city: str, country_id: int, last_update: Optional[str] = None):
        self.city_id: Optional[int] = city_id
        self.city: str = city
        self.country_id: int = country_id
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<Entity.City id={self.city_id} name='{self.city}' fk_country={self.country_id}>"

class FilmEntity:
    def __init__(self, film_id: Optional[int], title: str, rental_rate: float, length: int, replacement_cost: float, release_year: Optional[int] = None):
        self.film_id: Optional[int] = film_id
        self.title: str = title
        self.rental_rate: float = float(rental_rate)
        self.length: int = length
        self.replacement_cost: float = float(replacement_cost)
        self.release_year: Optional[int] = release_year

    def __repr__(self) -> str:
        return f"<Entity.Film id={self.film_id} title='{self.title}' rate=${self.rental_rate}>"
```

Cada entidad incluye:
- Atributos que corresponden exactamente a los campos de la tabla
- Tipado estático con Optional para campos autoincrement
- Método `__repr__` para debugging legible

### 3.3 Model Layer: List<Entity> (1 punto)

El `DataRepository` implementa la capa de modelo que transforma resultados relacionales en colecciones tipadas:

```python
class DataRepository:
    def __init__(self, context: DbContext):
        self.context: DbContext = context

    def guardar_pais(self, entity: CountryEntity) -> bool:
        query = "INSERT INTO country (country) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.country,))
        if last_id is not None:
            entity.country_id = last_id
            return True
        return False

    def listar_paises(self, limite: int) -> List[CountryEntity]:
        query = "SELECT country_id, country, last_update FROM country ORDER BY country_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        lista_modelos: List[CountryEntity] = []
        for f in filas:
            lista_modelos.append(CountryEntity(country_id=f[0], country=f[1], last_update=str(f[2])))
        return lista_modelos

    def buscar_pelicula_por_id(self, id_pelicula: int) -> Optional[FilmEntity]:
        query = "SELECT film_id, title, rental_rate, length, replacement_cost, release_year FROM film WHERE film_id = %s"
        filas = self.context.ejecutar_consulta(query, (id_pelicula,))
        if filas:
            f = filas[0]
            return FilmEntity(film_id=f[0], title=f[1], rental_rate=f[2], length=f[3], replacement_cost=f[4], release_year=f[5])
        return None
```

La estructura `List<CountryEntity>` demuestra la hidratación completa de filas SQL en objetos Python tipados.

### 3.4 Framework de Flujo: Controller (2 puntos)

El `SakilaWorkflowController` orquesta el flujo de negocio, separando la lógica de aplicación de la lógica de datos:

```python
class SakilaWorkflowController:
    def __init__(self):
        self.context = DbContext()
        self.repository = DataRepository(self.context)

    def procesar_flujo_fase2(self) -> None:
        print("=====================================================================")
        print("      INICIANDO INGENIERÍA DE SOFTWARE DE LA FASE II: ORM POO        ")
        print("=====================================================================")

        pais_por_mapear = CountryEntity(country_id=None, country="Portugal")
        print(f"   Estado pre-persistencia: {pais_por_mapear}")

        if self.repository.guardar_pais(pais_por_mapear):
            print(f"   Estado post-persistencia en ORM (ID Generado): {pais_por_mapear}")

        pais_duplicado = CountryEntity(country_id=None, country="Portugal")
        self.repository.guardar_pais(pais_duplicado)

        coleccion_paises: List[CountryEntity] = self.repository.listar_paises(limite=3)
        print(f"   Tipo de Estructura de Datos Retornada: {type(coleccion_paises)}")
        for pais in coleccion_paises:
            print(f"     -> Objeto Mapeado: {pais} | Instancia de Clase: {type(pais).__name__}")

        if pais_por_mapear.country_id:
            ciudad_por_mapear = CityEntity(city_id=None, city="Lisboa", country_id=pais_por_mapear.country_id)
            self.repository.guardar_ciudad(ciudad_por_mapear)
            print(f"   Entidad Ciudad vinculada y persistida: {ciudad_por_mapear}")

        pelicula_business_obj = self.repository.buscar_pelicula_por_id(id_pelicula=2)
        if pelicula_business_obj:
            print(f"   Estado original recuperado por ORM: {pelicula_business_obj}")
            pelicula_business_obj.rental_rate = 8.99
            if self.repository.actualizar_tarifa_pelicula(pelicula_business_obj):
                print(f"   Sincronización Exitosa. Nuevo estado en BD: {self.repository.buscar_pelicula_por_id(2)}")

        self.repository.eliminar_ciudad_por_id(id_ciudad=1)
```

El patrón Controller implementado permite:
1. Desacoplar la lógica de negocio de la acceso a datos
2. Centralizar la orchestration de operaciones
3. Mantener estado transaccional entre operaciones
4. Proporcionar puntos de extensión para logging y auditoría

---

## 4. Integridad de Datos

### 4.1 Unique Constraints Implementados

| Tabla | Constraint | Propósito |
|-------|------------|-----------|
| country | unique_country | Evitar países duplicados por nombre |
| city | unique_city_country | Evitar ciudad duplicada en mismo país |
| film | unique_title_release | Evitar título duplicado en mismo año |

### 4.2 Foreign Keys con Comportamiento Restrictivo

```sql
CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE
CONSTRAINT fk_inventory_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE RESTRICT ON UPDATE CASCADE
```

El `ON DELETE RESTRICT` previene la eliminación de entidades que tienen dependientes activos.

---

## 5. Video Explicativo (Complementario)

**Enlace al video**: [Insertar link de YouTube/Vimeo aquí]

**Duración**: 3-5 minutos

**Contenido**:
1. Introducción al proyecto y arquitectura general (30s)
2. Demostración de Fase I - CRUD y métricas (60s)
3. Explicación de Fase II - ORM nativo con DbContext (90s)
4. Demostración de constraints de integridad (45s)
5. Conclusiones y líneas futuras (45s)

---

## 6. Conclusiones

El proyecto demuestra que es posible construir un ORM funcional utilizando únicamente el conector nativo de MySQL para Python, sin depender de frameworks externos como SQLAlchemy o Django ORM. La arquitectura lograda proporciona:

- **Separación de responsabilidades**: DbContext maneja conexiones, Repository maneja datos, Controller orquestra
- **Type safety**: Entidades tipadas con verificación estática
- **Integridad enforceable**: Constraints a nivel de BD previenen datos inconsistentes
- **Interoperabilidad**: Import/Export CSV y JSON para integración con otros sistemas
- **Análisis estadístico**: Métricas descriptivas para exploración de datos

El enfoque artesanal permite comprender los fundamentos internos de cómo operan los ORM comerciales, while providing un framework extensible para aplicaciones de mediana escala.

---

## 7. Referencias

- MySQL Connector/Python Documentation. (2024). Oracle Corporation. https://dev.mysql.com/doc/connector-python/en/
- Pandas Documentation. (2024). NumFOCUS. https://pandas.pydata.org/docs/
- NumPy Documentation. (2024). NumFOCUS. https://numpy.org/doc/
- Date, C. J. (2004). *Introduction to Database Systems* (8th ed.). Addison-Wesley.
- Elmasri, R., & Navathe, S. (2016). *Fundamentals of Database Systems* (7th ed.). Pearson.

---

## 8. Anexos

### Anexo A: Estructura de Archivos del Proyecto

```
uasdCrudPython/
├── Fase1.sql           # DDL, DML, Constraints y 10 Consultas SQL
├── requirements.txt    # Dependencias Python
├── src/
│   ├── fase1_main.py   # Fase I: CRUD + Import/Export + Métricas
│   └── fase2_orm.py    # Fase II: ORM completo (DbContext, Entity, Model, Controller)
├── docs/
│   ├── README.md       # Documentación de uso
│   ├── DESIGN.md       # Diseño técnico
│   └── ensayo.md       # Este documento
└── data/               # Carpeta para exports CSV/JSON
```

### Anexo B: Datos de Prueba Cargados

**Países**: Dominican Republic, United States, Spain, Mexico, Colombia, Brazil, Portugal

**Ciudades**: Santo Domingo, Santiago, New York, Madrid, CDMX, Bogota, Rio de Janeiro, Lisboa

**Películas**: Inception, The Matrix, Interstellar, Spirited Away, Casablanca

### Anexo C: Métricas Descriptivas Calculadas

| Variable | Media | Rango | Desviación | Varianza |
|----------|-------|-------|------------|-----------|
| length (min) | Variable | Variable | Variable | Variable |
| replacement_cost ($) | Variable | Variable | Variable | Variable |

*Nota: Los valores exactos se generan dinámicamente al ejecutar `python fase1_main.py`*

---

**Repositorio GitHub**: https://github.com/edvvdev/uasdCrudPython

**Última actualización**: 5 de junio de 2026