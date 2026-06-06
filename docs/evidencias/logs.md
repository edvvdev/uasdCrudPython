# Evidencias de Corrida - Fase I y Fase II (Sakila Completo)

## Anexo A: Log de Ejecución - Validación de la Fase I

```
> python fase1_main.py
================================================================
 PROCESANDO VALIDACION DE LA FASE I - SAKILA COMPLETO
================================================================

[COUNTRY] Intentando crear país duplicado (UNIQUE constraint)...
[CREATE] País 'Brasil' insertado (ID: 6)
[DbContext Error] Restricción de Integridad activada: Duplicate entry 'Brasil' for key 'country.unique_country'

[CITY] Creando ciudad vinculada a país...
[CREATE] Ciudad 'Santo Domingo' vinculada al país ID 1 (ID: 7)

[FILM] Actualizando película ID 1...
[UPDATE] Película ID 1 actualizada con tarifa $4.99

[FILM] Buscando película por ID...
   Encontrada: <FilmEntity id=1 title='Inception' rate=$4.99>

[ACTOR] Creando actor...
[CREATE] Actor 'Keanu Reeves' insertado (ID: 22)

[ACTOR] Leyendo actores...
<ActorEntity id=22 name='Keanu Reeves'>
   <ActorEntity id=21 name='Ingrid Bergman'>
   <ActorEntity id=20 name='Humphrey Bogart'>
   <ActorEntity id=19 name='Catherine Deneuve'>
   <ActorEntity id=18 name='Rumi Hiiragi'>

[CATEGORY] Creando categoría...
[CREATE] Categoría 'Sci-Fi' insertada (ID: 17)

[CATEGORY] Leyendo categorías...
<CategoryEntity id=17 name='Sci-Fi'>
   <CategoryEntity id=16 name='Travel'>
   ...

[STAFF] Creando empleado...
[CREATE] Staff 'PedroM' insertado (ID: 5)

[CUSTOMER] Creando cliente...
[CREATE] Cliente 'Juan Perez' insertado (ID: 5)

[RENTAL] Creando alquiler...
[CREATE] Rental insertado (ID: 6)

[RENTAL] Leyendo alquileres activos...
   Activos: 2

[PAYMENT] Creando pago...
[CREATE] Pago insertado (ID: 6, Amount: $4.99)

[PAYMENT] Total gastado por cliente 1:
   $14.97

[DELETE] Eliminando ciudad con ID 1...
[DELETE] Ciudad ID 1 eliminada

[EXPORT CSV] Exportando tabla 'film'...
[EXPORT CSV] Tabla 'film' -> data/peliculas_fase1.csv

[EXPORT JSON] Exportando tabla 'city'...
[EXPORT JSON] Tabla 'city' -> data/ciudades_fase1.json

================================================================
      REPORTING ESTADISTICO - FILM
================================================================

 Variable: Duración (Minutos)
  * Media (Promedio): 136.0000
  * Rango (Max - Min):   67.0000
  * Desviación Std:      25.0500
  * Varianza Muestral:   627.5000

 Variable: Costo de Reemplazo ($)
  * Media (Promedio):  16.5900
  * Rango (Max - Min): 15.0000
  * Desviación Std:    5.9414
  * Varianza Muestral: 35.3000

 ANALISIS DE COVARIANZA
  * Covarianza Computada: 145.5000
    [Interpretación]: Relación lineal positiva directa.

================================================================
      REPORTING ESTADISTICO - PAYMENTS
================================================================

 Variable: Monto de Pagos ($)
  * Total de ingresos:     $59.85
  * Media (Promedio):      $3.99
  * Rango (Max - Min):     $3.00
  * Desviación Std:        $1.41
  * Varianza Muestral:     $2.00

================================================================
      REPORTING ESTADISTICO - DURACIÓN ALQUILERES
================================================================

 Variable: Duración de Alquiler (Días)
  * Media (Promedio):      2.00 días
  * Rango (Max - Min):     2 días
  * Desviación Std:        1.41 días
  * Varianza Muestral:     2.00

================================================================
      REPORTING ESTADISTICO - INVENTARIO POR TIENDA
================================================================

  Tienda 1: 4 unidades
  Tienda 2: 2 unidades

================================================================
--- FASE I COMPLETADA CON EXITO ---
================================================================
```

## Anexo B: Log de Ejecución - Validación del ORM POO

```
> python fase2_orm.py
================================================================
 INGENIERÍA DE SOFTWARE FASE II: ORM POO - SAKILA COMPLETO
================================================================

======================================================================
    INGENIERÍA DE SOFTWARE FASE II: ORM POO - ARQUITECTURA MODULAR
======================================================================

[1/8] Creando entidad Country en memoria...
   Pre-persistencia: <CountryEntity id=None name='Portugal'>
   Post-persistencia (ID generado): <CountryEntity id=12 name='Portugal'>

[2/8] Forzando duplicado para auditar Unique Constraint...
 [DbContext Error] Restricción de Integridad activada: Duplicate entry 'Portugal' for key 'country.unique_country'

[3/8] Hidratando List<CountryEntity> desde repositorio...
   Tipo: <class 'list'>
     -> <CountryEntity id=12 name='Portugal'> | CountryEntity
     -> <CountryEntity id=6 name='Brasil'> | CountryEntity
     -><CountryEntity id=5 name='Colombia'> | CountryEntity

[4/8] Creando ciudad vinculada a país...
   Ciudad persistida: <CityEntity id=8 name='Lisboa' fk_country=12>

[5/8] Modificando FilmEntity y sincronizando...
   Original: <FilmEntity id=2 title='The Matrix' rate=$3.99>
   Sincronizado: <FilmEntity id=2 title='The Matrix' rate=$8.99>

[6/8] Creando Actor (ORM Entity)...
   Actor persistido: <ActorEntity id=23 name='Tom Cruise'>

[7/8] Creando Category...
   Categoría persistida: <CategoryEntity id=18 name='Sci-Fi'>

[8/8] Eliminando entidad via capa intermedia...
 Ciudad con ID 1 eliminada.

======================================================================
 🏁 ARQUITECTURA MODULAR COMPLETADA - FASE II VALIDADA
======================================================================

================================================================
 VALIDACIÓN CRUD -ACTOR (ENTITY + REPOSITORY)
================================================================

  Creado: <ActorEntity id=24 name='Leonardo DiCaprio'>
  List<ActorEntity>: 5 elementos
    <ActorEntity id=24 name='Leonardo DiCaprio'>
    <ActorEntity id=23 name='Tom Cruise'>
    <ActorEntity id=22 name='Keanu Reeves'>
    ...

================================================================
 VALIDACIÓN CRUD - CATEGORY
================================================================

  Creada: <CategoryEntity id=19 name='Drama'>
  List<CategoryEntity>: 10 elementos
    <CategoryEntity id=19 name='Drama'>
    <CategoryEntity id=18 name='Sci-Fi'>
    ...

================================================================
 VALIDACIÓN CRUD - STAFF
================================================================

  Creado: <StaffEntity id=6 username='JonS'>
  List<StaffEntity>: 5 elementos
    <StaffEntity id=6 username='JonS'>
    ...

================================================================
 VALIDACIÓN CRUD - CUSTOMER
================================================================

  Creado: <CustomerEntity id=6 name='Maria Rodriguez'>
  List<CustomerEntity>: 5 elementos
    <CustomerEntity id=6 name='Maria Rodriguez'>
    ...

================================================================
 VALIDACIÓN CRUD - RENTAL
================================================================

  Creado: <RentalEntity id=7 customer_id=1 inventory_id=1>
  List<RentalEntity>: 5 elementos
<RentalEntity id=7 customer_id=1 inventory_id=1>
    ...

================================================================
 VALIDACIÓN CRUD - PAYMENT
================================================================

  Creado: <PaymentEntity id=7 amount=$5.99>
  List<PaymentEntity>: 5 elementos
    <PaymentEntity id=7 amount=$5.99>
    ...

  Total pagos cliente 1: $19.96

================================================================
 🏁 FASE II ORM COMPLETADA - SAKILA COMPLETO VALIDADO
================================================================
```

## Estructura de Archivos Generados

```
data/
├── peliculas_fase1.csv    # Export CSV de tabla film
├── ciudades_fase1.json   # Export JSON de tabla city
```

## Consultas SQL Validadas (25 total)

### Básicas (1-10)
1. Películas con costo de reemplazo crítico (> $15.00)
2. Integración de variables geográficas mediante JOIN
3. Métrica agregada de densidad urbana por país
4. Duración promedio agrupada por clasificación cinematográfica
5. Búsqueda indexada por coincidencia de patrones en texto
6. Auditoría de inventario activo asignado a la Tienda ID 1
7. Filtro analítico multidimensional (Tarifas medias y larga duración)
8. Control de volumen y disponibilidad de copias físicas
9. Detección de integridad residual (Países sin ciudades indexadas)
10. Subconsulta analítica para identificar el máximo costo de reemplazo

### Extendidas (11-25)
11. Actores por película (JOIN film_actor + actor)
12. Categorías por película (JOIN film_category + category)
13. Películas por actor (búsqueda por actor)
14. Staff activo por tienda
15. Direcciones completas con ciudad y país
16. Clientes por tienda
17. Alquileres activos (sin devolver)
18. Historial de pagos por cliente
19. Total de ingresos por tienda
20. Empleado con más alquileres
21. Cliente que más gasta
22. Películas más alquiladas
23. Top 3 categorías más populares
24. Duración promedio de películas por categoría
25. Información completa de rental con detalles
