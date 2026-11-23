"""Interface gráfica da Calculadora de Porcentagem (Tkinter).

Este módulo é responsável apenas por:
    - montar a interface (abas, campos, botões);
    - ler e validar os valores digitados pelo usuário;
    - chamar as funções matemáticas dos módulos em `calculos/`;
    - apresentar os resultados e mensagens de erro.

Nenhuma fórmula financeira deve ser calculada diretamente aqui.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from calculos.desconto import calcular_desconto
from calculos.acrescimo import calcular_acrescimo
from calculos.lucro import calcular_lucro_margem, calcular_preco_venda_por_margem
from calculos.juros import calcular_juros_simples


# ---------------------------------------------------------------------------
# Funções auxiliares reutilizáveis (validação e formatação)
# ---------------------------------------------------------------------------

DUAS_CASAS = Decimal("0.01")


def texto_para_decimal(texto: str) -> Decimal:
    """Converte um texto em Decimal.

    Aceita ponto ou vírgula como separador decimal (ex.: "1000.50" ou "1000,50").
    Lança ValueError se o texto estiver vazio ou não for um número válido.
    """
    texto = texto.strip()
    if texto == "":
        raise ValueError("Preencha todos os campos.")
    texto = texto.replace(",", ".")
    try:
        return Decimal(texto)
    except InvalidOperation:
        raise ValueError("Valor inválido. Digite apenas números.")


def formatar_moeda(valor: Decimal) -> str:
    """Formata um Decimal como moeda no padrão brasileiro. Ex.: R$ 1.250,50"""
    valor = valor.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)
    negativo = valor < 0
    valor = abs(valor)

    inteiro, decimal = f"{valor:.2f}".split(".")
    grupos = []
    while len(inteiro) > 3:
        grupos.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    grupos.insert(0, inteiro)
    parte_inteira = ".".join(grupos)

    sinal = "-" if negativo else ""
    return f"{sinal}R$ {parte_inteira},{decimal}"


def formatar_percentual(valor: Decimal) -> str:
    """Formata um Decimal como percentual no padrão brasileiro. Ex.: 20,00%"""
    valor = valor.quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)
    texto = f"{valor:.2f}".replace(".", ",")
    return f"{texto}%"


# ---------------------------------------------------------------------------
# Aplicação principal
# ---------------------------------------------------------------------------

class CalculadoraPorcentagemApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculadora de Porcentagem")
        self.root.geometry("800x600")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        aba_desconto = ttk.Frame(notebook)
        aba_acrescimo = ttk.Frame(notebook)
        aba_lucro = ttk.Frame(notebook)
        aba_juros = ttk.Frame(notebook)
        aba_sobre = ttk.Frame(notebook)

        notebook.add(aba_desconto, text="Desconto")
        notebook.add(aba_acrescimo, text="Acréscimo")
        notebook.add(aba_lucro, text="Margem de Lucro")
        notebook.add(aba_juros, text="Juros Simples")
        notebook.add(aba_sobre, text="Sobre")

        self._montar_aba_desconto(aba_desconto)
        self._montar_aba_acrescimo(aba_acrescimo)
        self._montar_aba_lucro(aba_lucro)
        self._montar_aba_juros(aba_juros)
        self._montar_aba_sobre(aba_sobre)

    # -----------------------------------------------------------------
    # ABA 1 - DESCONTO
    # -----------------------------------------------------------------
    def _montar_aba_desconto(self, aba: ttk.Frame):
        container = ttk.Frame(aba, padding=25)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Valor original:").grid(row=0, column=0, sticky="e", pady=8, padx=(0, 8))
        self.desc_valor = ttk.Entry(container, width=18)
        self.desc_valor.grid(row=0, column=1, sticky="w")

        ttk.Label(container, text="Desconto (%):").grid(row=1, column=0, sticky="e", pady=8, padx=(0, 8))
        self.desc_percentual = ttk.Entry(container, width=18)
        self.desc_percentual.grid(row=1, column=1, sticky="w")

        botoes = ttk.Frame(container)
        botoes.grid(row=2, column=0, columnspan=2, pady=20, sticky="w")
        ttk.Button(botoes, text="CALCULAR", command=self._calcular_desconto).pack(side="left", padx=(0, 10))
        ttk.Button(botoes, text="LIMPAR", command=self._limpar_desconto).pack(side="left")

        ttk.Label(container, text="Desconto aplicado:", font=("", 11, "bold")).grid(row=3, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.desc_resultado_desconto = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.desc_resultado_desconto.grid(row=3, column=1, sticky="w", pady=(6, 0))

        ttk.Label(container, text="Valor final:", font=("", 11, "bold")).grid(row=4, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.desc_resultado_final = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.desc_resultado_final.grid(row=4, column=1, sticky="w", pady=(6, 0))

        for entry in (self.desc_valor, self.desc_percentual):
            entry.bind("<Return>", lambda _e: self._calcular_desconto())

    def _limpar_desconto(self):
        self.desc_valor.delete(0, "end")
        self.desc_percentual.delete(0, "end")
        self.desc_resultado_desconto.config(text="—")
        self.desc_resultado_final.config(text="—")

    def _calcular_desconto(self):
        try:
            valor = texto_para_decimal(self.desc_valor.get())
            percentual = texto_para_decimal(self.desc_percentual.get())
            desconto, valor_final = calcular_desconto(valor, percentual)
            self.desc_resultado_desconto.config(text=formatar_moeda(desconto))
            self.desc_resultado_final.config(text=formatar_moeda(valor_final))
        except ValueError as erro:
            messagebox.showerror("Valor inválido", str(erro))

    # -----------------------------------------------------------------
    # ABA 2 - ACRÉSCIMO
    # -----------------------------------------------------------------
    def _montar_aba_acrescimo(self, aba: ttk.Frame):
        container = ttk.Frame(aba, padding=25)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Valor original:").grid(row=0, column=0, sticky="e", pady=8, padx=(0, 8))
        self.acr_valor = ttk.Entry(container, width=18)
        self.acr_valor.grid(row=0, column=1, sticky="w")

        ttk.Label(container, text="Acréscimo (%):").grid(row=1, column=0, sticky="e", pady=8, padx=(0, 8))
        self.acr_percentual = ttk.Entry(container, width=18)
        self.acr_percentual.grid(row=1, column=1, sticky="w")

        botoes = ttk.Frame(container)
        botoes.grid(row=2, column=0, columnspan=2, pady=20, sticky="w")
        ttk.Button(botoes, text="CALCULAR", command=self._calcular_acrescimo).pack(side="left", padx=(0, 10))
        ttk.Button(botoes, text="LIMPAR", command=self._limpar_acrescimo).pack(side="left")

        ttk.Label(container, text="Acréscimo:", font=("", 11, "bold")).grid(row=3, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.acr_resultado_acrescimo = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.acr_resultado_acrescimo.grid(row=3, column=1, sticky="w", pady=(6, 0))

        ttk.Label(container, text="Valor final:", font=("", 11, "bold")).grid(row=4, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.acr_resultado_final = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.acr_resultado_final.grid(row=4, column=1, sticky="w", pady=(6, 0))

        for entry in (self.acr_valor, self.acr_percentual):
            entry.bind("<Return>", lambda _e: self._calcular_acrescimo())

    def _limpar_acrescimo(self):
        self.acr_valor.delete(0, "end")
        self.acr_percentual.delete(0, "end")
        self.acr_resultado_acrescimo.config(text="—")
        self.acr_resultado_final.config(text="—")

    def _calcular_acrescimo(self):
        try:
            valor = texto_para_decimal(self.acr_valor.get())
            percentual = texto_para_decimal(self.acr_percentual.get())
            acrescimo, valor_final = calcular_acrescimo(valor, percentual)
            self.acr_resultado_acrescimo.config(text=formatar_moeda(acrescimo))
            self.acr_resultado_final.config(text=formatar_moeda(valor_final))
        except ValueError as erro:
            messagebox.showerror("Valor inválido", str(erro))

    # -----------------------------------------------------------------
    # ABA 3 - MARGEM DE LUCRO
    # -----------------------------------------------------------------
    def _montar_aba_lucro(self, aba: ttk.Frame):
        container = ttk.Frame(aba, padding=25)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Calcular:", font=("", 11, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self.lucro_modo = tk.StringVar(value="lucro_margem")
        ttk.Radiobutton(
            container, text="Lucro e margem (a partir do custo e da venda)",
            variable=self.lucro_modo, value="lucro_margem", command=self._atualizar_modo_lucro,
        ).grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(
            container, text="Preço de venda (a partir do custo e da margem desejada)",
            variable=self.lucro_modo, value="preco_venda", command=self._atualizar_modo_lucro,
        ).grid(row=2, column=0, columnspan=2, sticky="w")

        ttk.Label(container, text="Custo:").grid(row=3, column=0, sticky="e", pady=8, padx=(0, 8))
        self.lucro_custo = ttk.Entry(container, width=18)
        self.lucro_custo.grid(row=3, column=1, sticky="w")

        self.rotulo_lucro_campo2 = ttk.Label(container, text="Preço de venda:")
        self.rotulo_lucro_campo2.grid(row=4, column=0, sticky="e", pady=8, padx=(0, 8))
        self.lucro_campo2 = ttk.Entry(container, width=18)
        self.lucro_campo2.grid(row=4, column=1, sticky="w")

        botoes = ttk.Frame(container)
        botoes.grid(row=5, column=0, columnspan=2, pady=20, sticky="w")
        ttk.Button(botoes, text="CALCULAR", command=self._calcular_lucro).pack(side="left", padx=(0, 10))
        ttk.Button(botoes, text="LIMPAR", command=self._limpar_lucro).pack(side="left")

        self.rotulo_lucro_resultado1 = ttk.Label(container, text="Lucro:", font=("", 11, "bold"))
        self.rotulo_lucro_resultado1.grid(row=6, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.lucro_resultado1 = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.lucro_resultado1.grid(row=6, column=1, sticky="w", pady=(6, 0))

        self.rotulo_lucro_resultado2 = ttk.Label(container, text="Margem de lucro:", font=("", 11, "bold"))
        self.rotulo_lucro_resultado2.grid(row=7, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.lucro_resultado2 = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.lucro_resultado2.grid(row=7, column=1, sticky="w", pady=(6, 0))

        nota = (
            "Nota: margem de lucro é calculada sobre o PREÇO DE VENDA.\n"
            "Não confunda com markup, que é calculado sobre o CUSTO.\n"
            "Veja o README.md para mais detalhes."
        )
        ttk.Label(container, text=nota, foreground="#555555", justify="left", font=("", 9)).grid(
            row=8, column=0, columnspan=2, sticky="w", pady=(20, 0)
        )

        for entry in (self.lucro_custo, self.lucro_campo2):
            entry.bind("<Return>", lambda _e: self._calcular_lucro())

    def _atualizar_modo_lucro(self):
        if self.lucro_modo.get() == "lucro_margem":
            self.rotulo_lucro_campo2.config(text="Preço de venda:")
            self.rotulo_lucro_resultado1.config(text="Lucro:")
            self.rotulo_lucro_resultado2.config(text="Margem de lucro:")
        else:
            self.rotulo_lucro_campo2.config(text="Margem desejada (%):")
            self.rotulo_lucro_resultado1.config(text="Preço de venda:")
            self.rotulo_lucro_resultado2.config(text="")
        self.lucro_campo2.delete(0, "end")
        self.lucro_resultado1.config(text="—")
        self.lucro_resultado2.config(text="—")

    def _limpar_lucro(self):
        self.lucro_custo.delete(0, "end")
        self.lucro_campo2.delete(0, "end")
        self.lucro_resultado1.config(text="—")
        self.lucro_resultado2.config(text="—")

    def _calcular_lucro(self):
        try:
            custo = texto_para_decimal(self.lucro_custo.get())
            valor_campo2 = texto_para_decimal(self.lucro_campo2.get())

            if self.lucro_modo.get() == "lucro_margem":
                lucro, margem = calcular_lucro_margem(custo, valor_campo2)
                self.lucro_resultado1.config(text=formatar_moeda(lucro))
                self.lucro_resultado2.config(text=formatar_percentual(margem))
            else:
                preco_venda = calcular_preco_venda_por_margem(custo, valor_campo2)
                self.lucro_resultado1.config(text=formatar_moeda(preco_venda))
                self.lucro_resultado2.config(text="")

        except ValueError as erro:
            messagebox.showerror("Valor inválido", str(erro))

    # -----------------------------------------------------------------
    # ABA 4 - JUROS SIMPLES
    # -----------------------------------------------------------------
    def _montar_aba_juros(self, aba: ttk.Frame):
        container = ttk.Frame(aba, padding=25)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Capital:").grid(row=0, column=0, sticky="e", pady=8, padx=(0, 8))
        self.juros_capital = ttk.Entry(container, width=18)
        self.juros_capital.grid(row=0, column=1, sticky="w")

        ttk.Label(container, text="Taxa (%):").grid(row=1, column=0, sticky="e", pady=8, padx=(0, 8))
        self.juros_taxa = ttk.Entry(container, width=18)
        self.juros_taxa.grid(row=1, column=1, sticky="w")

        ttk.Label(container, text="Tempo:").grid(row=2, column=0, sticky="e", pady=8, padx=(0, 8))
        self.juros_tempo = ttk.Entry(container, width=18)
        self.juros_tempo.grid(row=2, column=1, sticky="w")

        ttk.Label(container, text="Unidade:").grid(row=3, column=0, sticky="e", pady=8, padx=(0, 8))
        self.juros_unidade = ttk.Combobox(
            container, values=["Dias", "Meses", "Anos"], width=15, state="readonly"
        )
        self.juros_unidade.current(2)
        self.juros_unidade.grid(row=3, column=1, sticky="w")

        aviso = ttk.Label(
            container,
            text="A taxa e o tempo devem estar na mesma unidade (ex.: taxa mensal com tempo em meses).",
            foreground="#555555", font=("", 9), wraplength=400, justify="left",
        )
        aviso.grid(row=4, column=0, columnspan=2, sticky="w", pady=(4, 0))

        botoes = ttk.Frame(container)
        botoes.grid(row=5, column=0, columnspan=2, pady=20, sticky="w")
        ttk.Button(botoes, text="CALCULAR", command=self._calcular_juros).pack(side="left", padx=(0, 10))
        ttk.Button(botoes, text="LIMPAR", command=self._limpar_juros).pack(side="left")

        ttk.Label(container, text="Juros:", font=("", 11, "bold")).grid(row=6, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.juros_resultado_juros = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.juros_resultado_juros.grid(row=6, column=1, sticky="w", pady=(6, 0))

        ttk.Label(container, text="Montante:", font=("", 11, "bold")).grid(row=7, column=0, sticky="e", padx=(0, 8), pady=(6, 0))
        self.juros_resultado_montante = ttk.Label(container, text="—", font=("", 13, "bold"), foreground="#0a6e0a")
        self.juros_resultado_montante.grid(row=7, column=1, sticky="w", pady=(6, 0))

        for entry in (self.juros_capital, self.juros_taxa, self.juros_tempo):
            entry.bind("<Return>", lambda _e: self._calcular_juros())

    def _limpar_juros(self):
        self.juros_capital.delete(0, "end")
        self.juros_taxa.delete(0, "end")
        self.juros_tempo.delete(0, "end")
        self.juros_unidade.current(2)
        self.juros_resultado_juros.config(text="—")
        self.juros_resultado_montante.config(text="—")

    def _calcular_juros(self):
        try:
            capital = texto_para_decimal(self.juros_capital.get())
            taxa = texto_para_decimal(self.juros_taxa.get())
            tempo = texto_para_decimal(self.juros_tempo.get())
            juros, montante = calcular_juros_simples(capital, taxa, tempo)
            self.juros_resultado_juros.config(text=formatar_moeda(juros))
            self.juros_resultado_montante.config(text=formatar_moeda(montante))
        except ValueError as erro:
            messagebox.showerror("Valor inválido", str(erro))

    # -----------------------------------------------------------------
    # ABA 5 - SOBRE
    # -----------------------------------------------------------------
    def _montar_aba_sobre(self, aba: ttk.Frame):
        container = ttk.Frame(aba, padding=30)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Calculadora de Porcentagem", font=("", 16, "bold")).pack(anchor="w", pady=(0, 10))
        texto = (
            "Aplicativo desktop para cálculos percentuais comerciais e financeiros.\n\n"
            "Desenvolvido em Python 3 com Tkinter, sem dependências externas. "
            "Os cálculos monetários utilizam o módulo Decimal para maior precisão.\n\n"
            "Funcionalidades:\n"
            "  • Desconto percentual\n"
            "  • Acréscimo percentual\n"
            "  • Margem de lucro (lucro/margem e preço de venda)\n"
            "  • Juros simples\n\n"
            "Margem de lucro x Markup:\n"
            "  A margem de lucro é calculada sobre o PREÇO DE VENDA:\n"
            "      margem = (lucro / preço_venda) x 100\n"
            "  O markup é calculado sobre o CUSTO:\n"
            "      markup = (lucro / custo) x 100\n"
            "  Os dois valores são diferentes para o mesmo produto — não devem "
            "ser confundidos.\n"
        )
        ttk.Label(container, text=texto, justify="left").pack(anchor="w")
