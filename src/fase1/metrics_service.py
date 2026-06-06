# =====================================================================
# METRICS SERVICE - Métricas Descriptivas con Manejo de Errores
# =====================================================================

import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from src.config import Config


class MetricsService:
    """Servicio para cálculo de métricas estadísticas descriptivas."""

    def __init__(self):
        try:
            self.engine = create_engine(
                f"mysql+mysqlconnector://{Config.USER}:{Config.PASSWORD}@{Config.HOST}:{Config.PORT}/{Config.DATABASE}"
            )
        except Exception as e:
            print(f"[CRITICAL] No se pudo crear conexión a la base de datos: {e}")
            sys.exit(1)

    def _get_connection(self):
        """Obtiene conexión SQLAlchemy."""
        try:
            return self.engine.connect()
        except Exception as e:
            print(f"[ERROR] No se pudo obtener conexión: {e}")
            return None

    def _leer_dataframe(self, query: str) -> pd.DataFrame:
        """Ejecuta query y retorna DataFrame con manejo de errores."""
        conn = self._get_connection()
        if conn is None:
            return pd.DataFrame()
        try:
            df = pd.read_sql(query, conn)
            return df
        except SQLAlchemyError as e:
            print(f"[ERROR] Fallo en consulta SQL: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"[ERROR] Error inesperado: {e}")
            return pd.DataFrame()
        finally:
            try:
                conn.close()
            except:
                pass

    def calcular_metricas_descriptivas(self) -> dict:
        """Calcula métricas descriptivas para las variables de film."""
        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO DE VARIABLES (FILM)")
        print("=" * 50)

        try:
            df = self._leer_dataframe("SELECT length, replacement_cost FROM film")
            if df.empty:
                print("  No hay datos de películas.")
                print("=" * 50 + "\n")
                return {}

            resultados = {}
            variables = {
                'length': 'Duración (Minutos)',
                'replacement_cost': 'Costo de Reemplazo ($)'
            }

            for var_name, var_label in variables.items():
                datos = df[var_name].dropna().to_numpy()

                if len(datos) == 0:
                    print(f"\n Variable: {var_label}")
                    print("  Sin datos válidos.")
                    continue

                media = float(np.mean(datos))
                rango = float(np.ptp(datos))
                desviacion = float(np.std(datos, ddof=1))
                varianza = float(np.var(datos, ddof=1))

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

            if 'length' in df.columns and 'replacement_cost' in df.columns:
                length_clean = df['length'].dropna()
                cost_clean = df['replacement_cost'].dropna()
                if len(length_clean) > 1 and len(cost_clean) > 1:
                    matriz_cov = np.cov(length_clean, cost_clean, ddof=1)
                    covarianza = float(matriz_cov[0, 1])
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

        except Exception as e:
            print(f"[ERROR] Fallo general en métricas de film: {e}")

        print("=" * 50 + "\n")
        return resultados

    def calcular_covarianza(self, var1: str, var2: str) -> float:
        """Calcula covarianza entre dos variables."""
        try:
            df = self._leer_dataframe(f"SELECT {var1}, {var2} FROM film")
            if df.empty or var1 not in df.columns or var2 not in df.columns:
                return 0.0
            matriz_cov = np.cov(df[var1], df[var2], ddof=1)
            return float(matriz_cov[0, 1])
        except Exception as e:
            print(f"[ERROR] No se pudo calcular covarianza: {e}")
            return 0.0

    def metricas_payments(self) -> dict:
        """Métricas descriptivas para payments (amount)."""
        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - PAYMENTS (AMOUNT)")
        print("=" * 50)

        try:
            df = self._leer_dataframe("SELECT amount FROM payment")
            if df.empty:
                print("  No hay datos de pagos.")
                print("=" * 50 + "\n")
                return {}

            datos = df['amount'].dropna().to_numpy()

            if len(datos) == 0:
                print("  No hay montos de pago válidos.")
                print("=" * 50 + "\n")
                return {}

            media = float(np.mean(datos))
            rango = float(np.ptp(datos))
            desviacion = float(np.std(datos, ddof=1))
            varianza = float(np.var(datos, ddof=1))
            total = float(np.sum(datos))

            print(f"\n Variable: Monto de Pagos ($)")
            print(f"  * Total de ingresos:     ${total:.2f}")
            print(f"  * Media (Promedio):      ${media:.4f}")
            print(f"  * Rango (Max - Min):     ${rango:.4f}")
            print(f"  * Desviación Std:        ${desviacion:.4f}")
            print(f"  * Varianza Muestral:     ${varianza:.4f}")
            print("=" * 50 + "\n")

            return {'media': media, 'rango': rango, 'desviacion': desviacion,
                    'varianza': varianza, 'total': total}
        except Exception as e:
            print(f"[ERROR] Fallo en métricas de payments: {e}")
            print("=" * 50 + "\n")
            return {}

    def metricas_rental_duration(self) -> dict:
        """Métricas de duración de alquileres (días entre rental y return)."""
        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - DURACIÓN ALQUILERES")
        print("=" * 50)

        try:
            df = self._leer_dataframe("""SELECT DATEDIFF(IFNULL(return_date, NOW()), rental_date) AS dias
 FROM rental WHERE return_date IS NOT NULL""")
            if df.empty:
                print("  No hay datos de alquileres completados.")
                print("=" * 50 + "\n")
                return {}

            datos = df['dias'].dropna().to_numpy()

            if len(datos) == 0:
                print("  No hay duraciones válidas.")
                print("=" * 50 + "\n")
                return {}

            media = float(np.mean(datos))
            rango = float(np.ptp(datos))
            desviacion = float(np.std(datos, ddof=1))
            varianza = float(np.var(datos, ddof=1))

            print(f"\n Variable: Duración de Alquiler (Días)")
            print(f"  * Media (Promedio):      {media:.2f} días")
            print(f"  * Rango (Max - Min):     {rango:.0f} días")
            print(f"  * Desviación Std:        {desviacion:.2f} días")
            print(f"  * Varianza Muestral:     {varianza:.2f}")
            print("=" * 50 + "\n")

            return {'media': media, 'rango': rango, 'desviacion': desviacion, 'varianza': varianza}
        except Exception as e:
            print(f"[ERROR] Fallo en métricas de rental duration: {e}")
            print("=" * 50 + "\n")
            return {}

    def metricas_inventory_by_store(self) -> dict:
        """Métricas de inventario por tienda."""
        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - INVENTARIO POR TIENDA")
        print("=" * 50)

        try:
            df = self._leer_dataframe("""SELECT store_id, COUNT(*) as total
 FROM inventory GROUP BY store_id""")
            if df.empty:
                print("  No hay datos de inventario.")
                print("=" * 50 + "\n")
                return {}

            for _, row in df.iterrows():
                print(f"  Tienda {row['store_id']}: {row['total']} unidades")

            print("=" * 50 + "\n")
            return df.to_dict('records')
        except Exception as e:
            print(f"[ERROR] Fallo en métricas de inventory: {e}")
            print("=" * 50 + "\n")
            return {}

    def metricas_customer_activity(self) -> dict:
        """Métricas de actividad por cliente (alquileres y pagos)."""
        print("\n" + "=" * 50)
        print("      REPORTING ESTADÍSTICO - ACTIVIDAD POR CLIENTE")
        print("=" * 50)

        try:
            df = self._leer_dataframe("""SELECT c.customer_id, c.first_name, c.last_name,
 COUNT(r.rental_id) as total_rentals,
 COALESCE(SUM(p.amount), 0) as total_spent
                                FROM customer c
                                LEFT JOIN rental r ON c.customer_id = r.customer_id
                                LEFT JOIN payment p ON c.customer_id = p.customer_id
                                GROUP BY c.customer_id""")
            if df.empty:
                print("  No hay datos de clientes.")
                print("=" * 50 + "\n")
                return {}

            rentals = df['total_rentals'].to_numpy()
            spent = df['total_spent'].to_numpy()

            print(f"\n Alquileres por Cliente:")
            print(f"  * Media:   {float(np.mean(rentals)):.2f}")
            print(f"  * Max:     {int(np.max(rentals)):.0f}")
            print(f"  * Min:     {int(np.min(rentals)):.0f}")

            print(f"\n Gasto por Cliente:")
            print(f"  * Total:   ${float(np.sum(spent)):.2f}")
            print(f"  * Media:   ${float(np.mean(spent)):.2f}")
            print(f"  * Max:     ${float(np.max(spent)):.2f}")

            print("=" * 50 + "\n")
            return df.to_dict('records')
        except Exception as e:
            print(f"[ERROR] Fallo en métricas de customer activity: {e}")
            print("=" * 50 + "\n")
            return {}
