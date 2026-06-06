# =====================================================================
# METRICS SERVICE - Métricas Descriptivas
# =====================================================================
# Calcula: Media, Rango, Desviación Estándar, Varianza, Covarianza

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from src.config import Config


class MetricsService:
    """Servicio para cálculo de métricas estadísticas descriptivas."""

    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{Config.USER}:{Config.PASSWORD}@{Config.HOST}:{Config.PORT}/{Config.DATABASE}"
        )

    def _get_connection(self):
        """Obtiene conexión SQLAlchemy."""
        return self.engine.connect()

    def calcular_metricas_descriptivas(self) -> dict:
        """
        Calcula métricas descriptivas para las variables de film:
        - length (duración en minutos)
        - replacement_cost (costo de reemplazo en USD)

        Returns:
            Dict con métricas por variable
        """
        with self._get_connection() as conn:
            df = pd.read_sql("SELECT length, replacement_cost FROM film", conn)

        resultados = {}
        variables = {
            'length': 'Duración (Minutos)',
            'replacement_cost': 'Costo de Reemplazo ($)'
        }

        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO DE VARIABLES (FILM)")
        print("=" * 50)

        for var_name, var_label in variables.items():
            datos = df[var_name].dropna().to_numpy()

            media = np.mean(datos)
            rango = np.ptp(datos)
            desviacion = np.std(datos, ddof=1)
            varianza = np.var(datos, ddof=1)

            resultados[var_name] = {
                'label': var_label,
                'media': media,
                'rango': rango,
                'desviacion': desviacion,
                'varianza': varianza
            }

            print(f"\n Variable: {var_label}")
            print(f"  * Media (Promedio): {media:.4f}")
            print(f"  * Rango (Max - Min):   {rango:.4f}")
            print(f"  * Desviación Std:      {desviacion:.4f}")
            print(f"  * Varianza Muestral:   {varianza:.4f}")

        matriz_cov = np.cov(df['length'], df['replacement_cost'], ddof=1)
        covarianza = matriz_cov[0, 1]
        resultados['covarianza'] = {
            'label': 'Covarianza (length vs replacement_cost)',
            'valor': covarianza
        }

        print("\n ANÁLISIS DE COVARIANZA")
        print(f"  * Covarianza Computada: {covarianza:.4f}")
        if covarianza > 0:
            print("    [Interpretación]: Relación lineal positiva directa.")
        else:
            print("    [Interpretación]: No posee co-dependencia lineal positiva.")

        print("=" * 50 + "\n")
        return resultados

    def calcular_covarianza(self, var1: str, var2: str) -> float:
        """Calcula covarianza entre dos variables."""
        with self._get_connection() as conn:
            df = pd.read_sql(f"SELECT {var1}, {var2} FROM film", conn)
        matriz_cov = np.cov(df[var1], df[var2], ddof=1)
        return matriz_cov[0, 1]

    def metricas_payments(self) -> dict:
        """Métricas descriptivas para payments (amount)."""
        with self._get_connection() as conn:
            df = pd.read_sql("SELECT amount FROM payment", conn)

        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - PAYMENTS (AMOUNT)")
        print("=" * 50)

        datos = df['amount'].dropna().to_numpy()

        media = np.mean(datos)
        rango = np.ptp(datos)
        desviacion = np.std(datos, ddof=1)
        varianza = np.var(datos, ddof=1)
        total = np.sum(datos)

        print(f"\n Variable: Monto de Pagos ($)")
        print(f"  * Total de ingresos:     ${total:.2f}")
        print(f"  * Media (Promedio):      ${media:.4f}")
        print(f"  * Rango (Max - Min):     ${rango:.4f}")
        print(f"  * Desviación Std:        ${desviacion:.4f}")
        print(f"  * Varianza Muestral:     ${varianza:.4f}")
        print("=" * 50 + "\n")

        return {'media': media, 'rango': rango, 'desviacion': desviacion,
                'varianza': varianza, 'total': total}

    def metricas_rental_duration(self) -> dict:
        """Métricas de duración de alquileres (días entre rental y return)."""
        with self._get_connection() as conn:
            df = pd.read_sql("""SELECT DATEDIFF(IFNULL(return_date, NOW()), rental_date) AS dias
 FROM rental WHERE return_date IS NOT NULL""", conn)

        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - DURACIÓN ALQUILERES")
        print("=" * 50)

        datos = df['dias'].dropna().to_numpy()

        if len(datos) == 0:
            print("  No hay datos de alquileres completados.")
            print("=" * 50 + "\n")
            return {}

        media = np.mean(datos)
        rango = np.ptp(datos)
        desviacion = np.std(datos, ddof=1)
        varianza = np.var(datos, ddof=1)

        print(f"\n Variable: Duración de Alquiler (Días)")
        print(f"  * Media (Promedio):      {media:.2f} días")
        print(f"  * Rango (Max - Min):     {rango:.0f} días")
        print(f"  * Desviación Std:        {desviacion:.2f} días")
        print(f"  * Varianza Muestral:     {varianza:.2f}")
        print("=" * 50 + "\n")

        return {'media': media, 'rango': rango, 'desviacion': desviacion, 'varianza': varianza}

    def metricas_inventory_by_store(self) -> dict:
        """Métricas de inventario por tienda."""
        with self._get_connection() as conn:
            df = pd.read_sql("""SELECT store_id, COUNT(*) as total
 FROM inventory GROUP BY store_id""", conn)

        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - INVENTARIO POR TIENDA")
        print("=" * 50)

        for _, row in df.iterrows():
            print(f"  Tienda {row['store_id']}: {row['total']} unidades")

        print("=" * 50 + "\n")
        return df.to_dict('records')

    def metricas_customer_activity(self) -> dict:
        """Métricas de actividad por cliente (alquileres y pagos)."""
        with self._get_connection() as conn:
            df = pd.read_sql("""SELECT c.customer_id, c.first_name, c.last_name,
 COUNT(r.rental_id) as total_rentals,
                                COALESCE(SUM(p.amount), 0) as total_spent
                                FROM customer c
                                LEFT JOIN rental r ON c.customer_id = r.customer_id
                                LEFT JOIN payment p ON c.customer_id = p.customer_id
                                GROUP BY c.customer_id""", conn)

        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - ACTIVIDAD POR CLIENTE")
        print("=" * 50)

        if len(df) == 0:
            print("  No hay datos de clientes.")
            print("=" * 50 + "\n")
            return {}

        rentals = df['total_rentals'].to_numpy()
        spent = df['total_spent'].to_numpy()

        print(f"\n Alquileres por Cliente:")
        print(f"  * Media:   {np.mean(rentals):.2f}")
        print(f"  * Max:     {np.max(rentals):.0f}")
        print(f"  * Min:     {np.min(rentals):.0f}")

        print(f"\n Gasto por Cliente:")
        print(f"  * Total:   ${np.sum(spent):.2f}")
        print(f"  * Media:   ${np.mean(spent):.2f}")
        print(f"  * Max:     ${np.max(spent):.2f}")

        print("=" * 50 + "\n")
        return df.to_dict('records')
