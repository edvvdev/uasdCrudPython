# =====================================================================
# MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
# CASO PRÁCTICO 2: CRUD/ORM NATIVO Y ESTRUCTURAS DE DATOS
# FASE II: ARQUITECTURA ORM MODULAR (DbContext, Entity, Model, Controller)
# =====================================================================

from src.controllers.sakila_controller import SakilaWorkflowController


def main():
    """Punto de entrada para ejecutar el flujo ORM de la Fase II."""
    controlador = SakilaWorkflowController()
    controlador.procesar_flujo_completo()


if __name__ == "__main__":
    main()
