# =====================================================================
# FASE2_ORM.PY - VALIDACIÓN DE FASE II ORM (SAKILA COMPLETO)
# =====================================================================
# Punto de entrada para validación de Fase II: Arquitectura ORM POO
#
# MAESTRANTES:
#   - Framiel Trinidad
#   - Edwing Perez
#   - Jharol Duran
#
# Universidad Autónoma de Santo Domingo (UASD)
# INF-8237-C2: Ciencias de Datos 1
# Profesora: Silveria del Orbe Abad

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.controllers import SakilaWorkflowController
from src.utils.helpers import clear_screen


def main():
    """Ejecuta la validación completa de la Fase II ORM."""
    clear_screen()
    print("=" * 70)
    print(" INGENIERÍA DE SOFTWARE FASE II: ORM POO - SAKILA COMPLETO")
    print("=" * 70)
    print()

    ctrl = SakilaWorkflowController()

    # === Flujo Completo ORM ===
    ctrl.procesar_flujo_completo()
    print()

    # === CRUD Actor ===
    print("=" * 70)
    print(" VALIDACIÓN CRUD -ACTOR (ENTITY + REPOSITORY)")
    print("=" * 70)
    print()
    actor = ctrl.crear_actor("Leonardo", "DiCaprio")
    print(f"  Creado: {actor}")
    actores = ctrl.obtener_actores(5)
    print(f"  List<ActorEntity>: {len(actores)} elementos")
    for a in actores:
        print(f"    {a}")
    print()

    # === CRUD Category ===
    print("=" * 70)
    print(" VALIDACIÓN CRUD - CATEGORY")
    print("=" * 70)
    print()
    cat = ctrl.crear_categoria("Drama")
    print(f"  Creada: {cat}")
    cats = ctrl.obtener_categorias(10)
    print(f"  List<CategoryEntity>: {len(cats)} elementos")
    for c in cats:
        print(f"    {c}")
    print()

    # === CRUD Staff ===
    print("=" * 70)
    print(" VALIDACIÓN CRUD - STAFF")
    print("=" * 70)
    print()
    staff = ctrl.crear_staff("Jon", "Sullivan", 1, 1, "JonS", "jon@sakila.com")
    print(f"  Creado: {staff}")
    staff_list = ctrl.obtener_staff(5)
    print(f"  List<StaffEntity>: {len(staff_list)} elementos")
    for s in staff_list:
        print(f"    {s}")
    print()

    # === CRUD Customer ===
    print("=" * 70)
    print(" VALIDACIÓN CRUD - CUSTOMER")
    print("=" * 70)
    print()
    cust = ctrl.crear_cliente(1, "Maria", "Rodriguez", 1, "maria@email.com")
    print(f"  Creado: {cust}")
    customers = ctrl.obtener_clientes(5)
    print(f"  List<CustomerEntity>: {len(customers)} elementos")
    for c in customers:
        print(f"    {c}")
    print()

    # === CRUD Rental ===
    print("=" * 70)
    print(" VALIDACIÓN CRUD - RENTAL")
    print("=" * 70)
    print()
    rental = ctrl.crear_alquiler(1, 1, 1)
    print(f"  Creado: {rental}")
    rentals = ctrl.obtener_alquileres(5)
    print(f"  List<RentalEntity>: {len(rentals)} elementos")
    for r in rentals:
        print(f"    {r}")
    print()

    # === CRUD Payment ===
    print("=" * 70)
    print(" VALIDACIÓN CRUD - PAYMENT")
    print("=" * 70)
    print()
    payment = ctrl.crear_pago(1, 1, 5.99)
    print(f"  Creado: {payment}")
    payments = ctrl.obtener_pagos(5)
    print(f"  List<PaymentEntity>: {len(payments)} elementos")
    for p in payments:
        print(f"    {p}")
    print()

    total = ctrl.total_pagos_cliente(1)
    print(f"  Total pagos cliente 1: ${total:.2f}")
    print()

    print("=" * 70)
    print(" 🏁 FASE II ORM COMPLETADA - SAKILA COMPLETO VALIDADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
