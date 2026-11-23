"""Cálculos de lucro e margem de lucro.

    Modo 1 (lucro e margem a partir do custo e da venda):
        lucro  = preço_venda - custo
        margem = (lucro / preço_venda) x 100

    Modo 2 (preço de venda a partir do custo e da margem desejada):
        preço_venda = custo / (1 - margem / 100)

IMPORTANTE: margem de lucro é calculada sobre o PREÇO DE VENDA, enquanto
markup é calculado sobre o CUSTO. Os dois conceitos não são a mesma coisa
(ver README.md para mais detalhes).
"""

from decimal import Decimal


def calcular_lucro_margem(custo: Decimal, preco_venda: Decimal):
    """Retorna (lucro, margem_percentual) a partir do custo e do preço de venda."""
    if custo < 0:
        raise ValueError("O custo não pode ser negativo.")
    if preco_venda <= 0:
        raise ValueError("O preço de venda deve ser maior que zero.")

    lucro = preco_venda - custo
    margem = (lucro / preco_venda) * Decimal(100)
    return lucro, margem


def calcular_preco_venda_por_margem(custo: Decimal, margem: Decimal) -> Decimal:
    """Retorna o preço de venda necessário para atingir `margem` de lucro sobre `custo`."""
    if custo <= 0:
        raise ValueError("O custo deve ser maior que zero.")
    if margem < 0 or margem >= 100:
        raise ValueError("A margem deve ser maior ou igual a 0 e menor que 100%.")

    preco_venda = custo / (Decimal(1) - margem / Decimal(100))
    return preco_venda
