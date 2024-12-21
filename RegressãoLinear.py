import numpy as np

def treinar(X, y):
    # Calcula o coeficiente angular (a) da reta de regressão
    a = (np.sum((X - np.mean(X)) * (y - np.mean(y))) / np.sum((X - np.mean(X)) ** 2))
    
    # Calcula o coeficiente linear (b) da reta de regressão
    b = np.mean(y) - a * np.mean(X)
    
    # Retorna os coeficientes a e b
    return a, b

def prever(x, a, b):
    # Realiza a previsão usando a equação da reta y = ax + b
    return a * x + b

# Exemplo de uso
X = np.array([1, 2, 3, 4, 5])  # Dados de entrada
y = np.array([2, 3, 5, 7, 11])  # Dados de saída

# Treinando o modelo
a, b = treinar(X, y)

# Exibindo os coeficientes
print(f"Coeficiente angular (a): {a}")
print(f"Coeficiente linear (b): {b}")

# Fazendo uma previsão
x_novo = 6
previsao = prever(x_novo, a, b)

# Exibindo a previsão
print(f"Previsão para x = {x_novo}: {previsao}")