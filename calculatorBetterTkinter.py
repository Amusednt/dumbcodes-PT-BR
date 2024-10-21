import tkinter as tk
from tkinter import ttk  # Importa ttk para estilos mais modernos

def calcular():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operacao = combo_operacao.get()

        if operacao == '+':
            resultado = num1 + num2
        elif operacao == '-':
            resultado = num1 - num2
        elif operacao == '*':
            resultado = num1 * num2
        elif operacao == '/':
            if num2 != 0:
                resultado = num1 / num2
            else:
                resultado = "Erro: Divisão por zero"
        else:
            resultado = "Operação inválida"

        label_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        label_resultado.config(text="Erro: Entrada inválida")

# Interface Gráfica
root = tk.Tk()
root.title("Calculadora")
root.geometry("300x250")  # Define o tamanho da janela
root.configure(bg="#f0f0f0")  # Cor de fundo

# Estilo do título
title_label = tk.Label(root, text="Calculadora", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)  # Espaçamento vertical

# Entrada do primeiro número
entry_num1 = tk.Entry(root, width=20, font=("Arial", 14))
entry_num1.pack(pady=5)

# Entrada do segundo número
entry_num2 = tk.Entry(root, width=20, font=("Arial", 14))
entry_num2.pack(pady=5)

# Menu suspenso para operações
combo_operacao = ttk.Combobox(root, values=["+", "-", "*", "/"], font=("Arial", 14))
combo_operacao.set("+")  # Define o valor padrão
combo_operacao.pack(pady=5)

# Botão de calcular
button_calcular = tk.Button(root, text="Calcular", command=calcular, font=("Arial", 14), bg="#4CAF50", fg="white")
button_calcular.pack(pady=10)

# Label para mostrar o resultado
label_resultado = tk.Label(root, text="Resultado: ", font=("Arial", 14), bg="#f0f0f0")
label_resultado.pack(pady=5)

# Inicia o loop principal da interface
root.mainloop()