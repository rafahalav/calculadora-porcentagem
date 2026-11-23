"""Cálculo de desconto percentual sobre um valor.

    desconto     = valor x percentual / 100
    valor_final  = valor - desconto
"""

from decimal import Decimal


def calcular_desconto(valor: Decimal, percentual: Decimal):
    """Retorna (desconto, valor_final) aplicando `percentual` de desconto sobre `valor`."""
    if valor <= 0:
        raise ValueError("O valor original deve ser maior que zero.")
    if percentual < 0 or percentual > 100:
        raise ValueError("O percentual de desconto deve estar entre 0 e 100.")

    desconto = valor * percentual / Decimal(100)
    valor_final = valor - desconto
    return desconto, valor_final
