"""Cálculo de juros simples.

    J = C x i x t
    M = C + J

Onde:
    J = juros
    C = capital inicial
    i = taxa (fração decimal, ex.: 2% -> 0,02)
    t = tempo

A taxa e o tempo devem estar na mesma unidade (ex.: taxa mensal com tempo
em meses). Esta responsabilidade é do usuário; o cálculo em si é agnóstico
quanto à unidade.
"""

from decimal import Decimal


def calcular_juros_simples(capital: Decimal, taxa_percentual: Decimal, tempo: Decimal):
    """Retorna (juros, montante) para os parâmetros informados.

    `taxa_percentual` deve ser informada em pontos percentuais (ex.: 2 para 2%).
    """
    if capital <= 0:
        raise ValueError("O capital deve ser maior que zero.")
    if taxa_percentual < 0:
        raise ValueError("A taxa não pode ser negativa.")
    if tempo <= 0:
        raise ValueError("O tempo deve ser maior que zero.")

    taxa = taxa_percentual / Decimal(100)
    juros = capital * taxa * tempo
    montante = capital + juros
    return juros, montante
