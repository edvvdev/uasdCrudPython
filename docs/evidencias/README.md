# Evidencias de Ejecución

Esta carpeta almacena las evidencias (screenshots, logs) de la corrida de los scripts.

## Archivos a generar

Después de ejecutar los scripts, guardar las salidas aquí:

```bash
# Generar evidencias
python src/fase1_main.py > fase1_output.txt
python src/fase2_orm.py > fase2_output.txt
mysql -u root sakila < sql/queries/03_queries.sql > queries_output.txt
```

## Estructura sugerida

```
evidencias/
├── fase1_output.txt # Salida de fase1_main.py
├── fase2_output.txt       # Salida de fase2_orm.py
├── queries_output.txt     # Resultado de las 10 consultas SQL
├── screenshot_db.png      # Captura de la DB importada
├── screenshot_crud.png    # Captura del CRUD en ejecución
└── screenshot_orm.png    # Captura del ORM en ejecución
```