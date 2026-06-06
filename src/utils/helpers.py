# =====================================================================
# HELPERS UTILITARIOS
# =====================================================================
# Funciones reutilizables para formateo, validación y manejo de errores.

from functools import wraps
from typing import Optional, Callable, Any
import sys


def handle_errors(func: Callable) -> Callable:
    """Decorador para manejo centralizado de errores."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            return None
    return wrapper


def print_header(title: str, width: int = 70) -> None:
    """Imprime un header formateado."""
    print("\n" + "=" * width)
    print(f" {title}")
    print("=" * width)


def print_subheader(title: str, width: int = 70) -> None:
    """Imprime un subheader formateado."""
    print(f"\n--- {title} ---")


def format_list(items: list, prefix: str = "  - ") -> str:
    """Formatea una lista para display."""
    return "\n".join(f"{prefix}{item}" for item in items)


def clear_screen() -> None:
    """Limpia la pantalla de la consola."""
    os.system("cls" if os.name == "nt" else "clear")


import os
