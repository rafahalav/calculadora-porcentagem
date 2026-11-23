"""Ponto de entrada da Calculadora de Porcentagem."""

import tkinter as tk

from ui.interface import CalculadoraPorcentagemApp


def main():
    root = tk.Tk()
    CalculadoraPorcentagemApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
