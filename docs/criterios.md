# Criterios de Evaluación - Cumplimiento

Este documento mapea cada criterio de evaluación con su implementación y ubicación en el proyecto.

## Rubros de Evaluación

| # | Componente | Puntos | Estado | Ubicación | Evidencia |
|---|------------|--------|--------|-----------|-----------|
| 1 | FASE I: Queries SQL y Python |8 | ✅ | `sql/queries/03_queries.sql`, `src/fase1_main.py` | Scripts y código |
| 2 | FASE II: DbContext + ORM framework | 3 | ✅ | `src/dbcontext.py` | mysql-connector-python |
| 3 | FASE II: Entity | 3 | ✅ | `src/entities/__init__.py` | 4 entidades implementadas |
| 4 | FASE II: Model (list<entity>) | 3 | ✅ | `src/models/data_repository.py` | DataRepository con List<T> |
| 5 | FASE II: Controller (MVC/Router) | 3 | ✅ | `src/controllers/sakila_controller.py` | SakilaWorkflowController |
| 6 | Video explicativo (opcional) | 3 | ❌ | Pendiente | - |

---

## 1. FASE I: Consultas SQL y Queries Python (8 puntos)

### Consultas SQL (`sql/queries/03_queries.sql`)
10 consultas analíticas implementadas:
1. Películas con costo > $15.00
2. Join ciudades-países
3. Conteo ciudades por país
4. Duración promedio por rating
5. Búsqueda por patrón (LIKE)
6. Inventario por tienda
7. Películas tarifa 3-6, duración > 120
8. Conteo copias por título
9. Países sin ciudades (LEFT JOIN WHERE NULL)
10. Máximo costo operativo (subconsulta)

### Queries desde Python (`src/fase1_main.py`)
- `crud_crear_pais()` - INSERT país
- `crud_leer_paises()` - SELECT países
- `crud_crear_ciudad()` - INSERT ciudad
- `crud_actualizar_tarifa_pelicula()` - UPDATE película
- `crud_eliminar_ciudad()` - DELETE ciudad
- `exportar_a_csv()` - Exportar a CSV
- `exportar_a_json()` - Exportar a JSON
- `calcular_metricas_descriptivas()` - Media, rango, desviación, varianza, covarianza

---

## 2. DbContext + ORM Framework (3 puntos)

**Archivo**: `src/dbcontext.py`

**Framework elegido**: `mysql-connector-python` (conector nativo oficial Oracle)

**Componentes implementados**:
- `_conectar()` - Método privado para conexión
- `ejecutar_comando()` - INSERT/UPDATE/DELETE parametrizado
- `ejecutar_consulta()` - SELECT parametrizado

```python
class DbContext:
    def _conectar(self):
        return mysql.connector.connect(
            host=self.host, port=self.port,
            user=self.user, password=self.password,
            database=self.database
        )
```

---

## 3. Entity (3 puntos)

**Archivo**: `src/entities/__init__.py`

**Entities implementadas** (mapeo 1:1 con tablas DBMS):

| Entity | Campos | Tabla DB |
|--------|--------|----------|
| `CountryEntity` | country_id, country, last_update | country |
| `CityEntity` | city_id, city, country_id, last_update | city |
| `FilmEntity` | film_id, title, rental_rate, length, replacement_cost, etc. | film |
| `InventoryEntity` | inventory_id, film_id, store_id, last_update | inventory |

---

## 4. Model - List<Entity> (3 puntos)

**Archivo**: `src/models/data_repository.py`

**DataRepository** implementa:
- `guardar_pais()` → CountryEntity
- `listar_paises()` → `List[CountryEntity]`
- `guardar_ciudad()` → CityEntity
- `listar_ciudades()` → `List[CityEntity]`
- `buscar_pelicula_por_id()` → `Optional[FilmEntity]`
- `listar_peliculas()` → `List[FilmEntity]`
- `actualizar_tarifa_pelicula()` → bool
- `eliminar_ciudad_por_id()` → bool

Ejemplo de hidratación:
```python
def listar_paises(self, limite: int) -> List[CountryEntity]:
    query = "SELECT ... FROM country ORDER BY country_id DESC LIMIT %s"
    filas = self.context.ejecutar_consulta(query, (limite,))
    lista_modelos: List[CountryEntity] = []
    for f in filas:
        lista_modelos.append(CountryEntity(...))
    return lista_modelos
```

---

## 5. Controller - Framework de Flujo (3 puntos)

**Archivo**: `src/controllers/sakila_controller.py`

**SakilaWorkflowController** implementa:
- Creación de entidades en memoria
- Persistencia via Repository
- Hidratación de List<Entity>
- Modificación de estado y sincronización BD
- Eliminación via capa intermedia

```python
class SakilaWorkflowController:
    def __init__(self):
        self.context = DbContext()
        self.repository = DataRepository(self.context)

    def procesar_flujo_completo(self):
        # 1. Crear país
        pais = CountryEntity(country_id=None, country="Portugal")
        self.repository.guardar_pais(pais)
        # 2. Forzar duplicado (auditar constraint)
        #3. Hidratar List<CountryEntity>
        # 4. Crear ciudad vinculada
        # 5. Modificar FilmEntity y sincronizar
        # 6. Eliminar via capa intermedia
```

---

## 6. Video Explicativo (Opcional -3 puntos)

**Estado**: Pendiente

**Contenido planeado**:
- Introducción al proyecto (30s)
- Demostración Fase I (60s)
- Explicación arquitectura ORM (90s)
- Constraints de integridad (45s)
- Conclusiones (45s)

---

## Evidencias de Ejecución

Las evidencias (screenshots) de la corrida de los scripts se almacenan en:
`docs/evidencias/`

Para capturar evidencias:
```bash
# Fase I
python src/fase1_main.py > docs/evidencias/fase1_output.txt

# Fase II
python src/fase2_orm.py > docs/evidencias/fase2_output.txt
```

---

## Estructura Final del Proyecto

```
uasdCrudPython/
├── requirements.txt
├── README.md
├── src/
│   ├── dbcontext.py           # DbContext (1 punto)
│   ├── fase1_main.py          # CRUD + Import/Export + Métricas
│   ├── fase2_orm.py           # Punto de entrada ORM
│   ├── entities/
│   │   └── __init__.py       # Entities (1 punto)
│   ├── models/
│   │   └── data_repository.py # Model List<Entity> (1 punto)
│   └── controllers/
│       └── sakila_controller.py # Controller (2 puntos)
├── sql/
│   ├── ddl/01_ddl.sql        # Constraints
│   ├── dml/02_dml.sql        # Datos
│   └── queries/03_queries.sql # 10 consultas
├── docs/
│   ├── README.md
│   ├── DESIGN.md
│   ├── ensayo/
│   │   └── ensayo.md         # Ensayo académico
│   ├── criterios.md         # Este documento
│   └── evidencias/          # Screenshots de corrida
└── data/                     # Exports CSV/JSON
```