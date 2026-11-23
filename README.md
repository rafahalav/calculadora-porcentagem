<p align="center">
  <img src="./assets/calculadora-banner.png"
       width="100%"
       alt="Calculadora de Porcentagem">
</p>

# 🧮 Calculadora de Porcentagem

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Tkinter](https://img.shields.io/badge/Tkinter-Interface%20Gráfica-green?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)

Aplicativo desktop em Python 3 com interface gráfica em Tkinter, projetado para cálculos percentuais comerciais e financeiros: **desconto, acréscimo, margem de lucro e juros simples**. 

Zero dependências externas. Precisão monetária garantida com o módulo `Decimal`.

---

## 🎯 Sobre o Projeto

O objetivo desta calculadora é oferecer uma ferramenta **simples, modular e didática** para o dia a dia comercial e financeiro. 

Diferente de soluções que usam `float` (sujeitas a erros de arredondamento em ponto flutuante), este projeto utiliza o tipo `Decimal` do Python, garantindo **precisão exata para valores monetários**. A arquitetura segue o princípio de **Separação de Responsabilidades**: a interface (`ui/`) cuida apenas da validação e exibição, enquanto toda a lógica financeira reside isolada nos módulos de `calculos/`.

---

## ✨ Funcionalidades Principais

- **Desconto**: Cálculo de valor do desconto e preço final.
- **Acréscimo**: Cálculo de acréscimos percentuais sobre um valor base.
- **Margem de Lucro**: Cálculo de lucro, margem percentual e preço de venda alvo.
- **Juros Simples**: Cálculo de juros e montante final com base em capital, taxa e tempo.
- **Formatação Brasileira**: Conversão automática para o padrão `R$ 1.250,50`.
- **Zero Dependências**: Funciona nativamente com a biblioteca padrão do Python.

---

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior.
- Tkinter (geralmente incluso no Python. No Linux, pode ser necessário: `sudo apt install python3-tk`).

### Como Executar
Nenhum passo de instalação complexo ou `pip install` é necessário. Basta clonar/copiar e rodar:

```bash
# Clone o repositório (ou extraia a pasta)
git clone https://github.com/rafahalav/calculadora-porcentagem.git
cd calculadora-porcentagem

# Execute a aplicação
python3 main.py
```

---

## 🧮 Fórmulas e Conceitos

### Desconto e Acréscimo
```text
Desconto:   desconto = valor × (percentual / 100)  |  valor_final = valor - desconto
Acréscimo:  acrescimo = valor × (percentual / 100) |  valor_final = valor + acrescimo
```

### Juros Simples
```text
J = C × i × t      (Juros)
M = C + J          (Montante)
```
*Nota: A taxa (`i`) e o tempo (`t`) devem estar na mesma unidade (ex.: taxa mensal com tempo em meses).*

### ⚠️ Margem de Lucro x Markup (Conceito Importante)
Esses dois conceitos costumam ser confundidos, mas **não são a mesma coisa**. Esta calculadora trabalha estritamente com **Margem de Lucro**.

| Conceito | Fórmula | Base de Cálculo |
|----------|---------|-----------------|
| **Margem de Lucro** | `(lucro / preço_venda) × 100` | Sobre o **PREÇO DE VENDA** |
| **Markup** | `(lucro / custo) × 100` | Sobre o **CUSTO** |

**Exemplo prático** (Custo = R$ 80,00 | Venda = R$ 100,00 | Lucro = R$ 20,00):
- **Margem de Lucro**: `20 / 100 × 100 = 20%`
- **Markup**: `20 / 80 × 100 = 25%`

Para calcular o preço de venda necessário para atingir uma margem desejada:
```text
preço_venda = custo / (1 - (margem / 100))
```

---

## 💻 Exemplos de Utilização

| Cálculo | Entrada | Resultado Esperado |
|---------|---------|-------------------|
| **Desconto** | Valor: R$ 1.000,00, Desconto: 15% | Desconto: R$ 150,00 / Final: R$ 850,00 |
| **Acréscimo** | Valor: R$ 500,00, Acréscimo: 20% | Acréscimo: R$ 100,00 / Final: R$ 600,00 |
| **Margem** | Custo: R$ 80,00, Venda: R$ 100,00 | Lucro: R$ 20,00 / Margem: 20% |
| **Preço pela Margem** | Custo: R$ 80,00, Margem Desejada: 20% | Preço de Venda: R$ 100,00 |
| **Juros Simples** | Capital: R$ 1.000,00, Taxa: 2% a.m., Tempo: 6 meses | Juros: R$ 120,00 / Montante: R$ 1.120,00 |

---

## 🛡️ Validações e Robustez

A aplicação foi projetada para **nunca quebrar** devido a entradas do usuário. Todas as exceções são tratadas com `messagebox.showerror`:

- ✅ Campos vazios recebem aviso amigável.
- ✅ Texto não numérico é rejeitado imediatamente.
- ✅ Aceita tanto **ponto** quanto **vírgula** como separador decimal.
- ✅ Valores monetários, custo e capital devem ser positivos.
- ✅ Percentual de desconto limitado a `0 - 100%`.
- ✅ Margem de lucro (no modo "preço pela margem") limitada a `0 ≤ margem < 100%`.
- ✅ Preço de venda igual a zero é rejeitado (evita `ZeroDivisionError`).
- ✅ Taxa e tempo negativos ou zero (quando não fazem sentido) são bloqueados.

---

## 🧪 Testes Realizados

Todos os módulos de cálculo foram testados isoladamente (Unit Testing manual) com os casos do enunciado, todos aprovados:
- [x] Desconto: `1000` com `15%` → `150,00` | `850,00`
- [x] Acréscimo: `500` com `20%` → `100,00` | `600,00`
- [x] Margem: `custo=80`, `venda=100` → `lucro=20,00` | `margem=20%`
- [x] Preço por margem: `custo=80`, `margem=20%` → `venda=100,00`
- [x] Juros simples: `1000`, `2% a.m.`, `6 meses` → `juros=120,00` | `montante=1.120,00`

**Testes de borda e falha:** Campo vazio, texto inválido, vírgula/ponto decimal, valor zero, número negativo, divisão por zero e margem ≥ 100% foram testados e tratados sem encerrar o programa.

---

## 📁 Estrutura do Projeto

```text
calculadora-porcentagem/
├── assets/
│   ├── calculadora-banner.png
│   └── screenshot.png
├── calculos/
│   ├── __init__.py
│   ├── desconto.py
│   ├── acrescimo.py
│   ├── lucro.py
│   └── juros.py
├── ui/
│   ├── __init__.py
│   └── interface.py
├── main.py
├── LICENSE
└── README.md
```

---

## 🔗 Projetos Relacionados

- **CIPHER AUDIT**: Auditor Automatizado de Hardening Linux com Geração de Relatórios Estruturados (JSON/HTML) e Inteligência Híbrida - [github.com/rafahalav/cipher-audit](https://github.com/rafahalav/cipher-audit)
- **PAI AI Coder**: Assistente de geração de código Python - [github.com/rafahalav/pai-ai-coder](https://github.com/rafahalav/pai-ai-coder)
- **PAI Code Reviewer**: Analisador de código com foco em segurança e performance - [github.com/rafahalav/pai-code-reviewer](https://github.com/rafahalav/pai-code-reviewer)

---

## 🧑‍💻 Autor

**Rafael Halav**  
Technology Professional | Telecommunications | IT | Python | AI | Data

🔗 [LinkedIn](https://www.linkedin.com/in/rafael-halav/) *(ajuste o link se necessário)*  
✉️ Contato via GitHub

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.
```

---

### 💡 Dicas Finais para o seu GitHub:
1. **Adicione um `LICENSE`**: Crie um arquivo chamado `LICENSE` na raiz com o texto da Licença MIT (seus outros projetos já usam, então mantém a consistência).
2. **Adicione um Screenshot**: Se possível, tire um print da calculadora rodando, salve como `screenshot.png` e adicione uma linha `![Screenshot](screenshot.png)` logo abaixo do título principal. Isso aumenta muito o engajamento no GitHub.
3. **Topics do Repositório**: Ao criar o repositório, adicione as tags: `python`, `tkinter`, `calculator`, `finance`, `decimal`, `brazil`.

O que achou dessa versão? Ela espelha a qualidade do seu projeto *CIPHER AUDIT*, destacando a separação de responsabilidades e a robustez das validações, que são pontos fortes do seu código. Posso ajustar qualquer seção se quiser!
# calculadora-porcentagem
