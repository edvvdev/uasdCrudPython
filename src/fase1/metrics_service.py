# =====================================================================
# METRICS SERVICE - Métricas Descriptivas
# =====================================================================
# Calcula: Media, Rango, Desviación Estándar, Varianza, Covarianza

import numpy as np
import pandas as pd
from src.dbcontext import DbContext


class MetricsService:
    """Servicio para cálculo de métricas estadísticas descriptivas."""

    def __init__(self):
        self.context = DbContext()

    def calcular_metricas_descriptivas(self) -> dict:
        """
        Calcula métricas descriptivas para las variables de film:
        - length (duración en minutos)
        - replacement_cost (costo de reemplazo en USD)

        Returns:
            Dict con métricas por variable
        """
        df = pd.read_sql("SELECT length, replacement_cost FROM film", self.context._conectar())
        self.context._conectar().close()

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
        df = pd.read_sql(f"SELECT {var1}, {var2} FROM film", self.context._conectar())
        self.context._conectar().close()
        matriz_cov = np.cov(df[var1], df[var2], ddof=1)
        return matriz_cov[0, 1]
