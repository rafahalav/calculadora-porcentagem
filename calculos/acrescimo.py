"""Cálculo de acréscimo percentual sobre um valor.

    acrescimo    = valor x percentual / 100
    valor_final  = valor + acrescimo
"""

from decimal import Decimal


def calcular_acrescimo(valor: Decimal, percentual: Decimal):
    """Retorna (acrescimo, valor_final) aplicando `percentual` de acréscimo sobre `valor`."""
    if valor <= 0:
        raise ValueError("O valor original deve ser maior que zero.")
    if percentual < 0:
        raise ValueError("O percentual de acréscimo não pode ser negativo.")

    acrescimo = valor * percentual / Decimal(100)
    valor_final = valor + acrescimo
    return acrescimo, valor_final
