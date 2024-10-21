import math  # Importa a biblioteca math para funções matemáticas

# Função para realizar operações básicas
def calculadora_basica(num1, num2, operacao):
    if operacao == 'adição':
        return num1 + num2
    elif operacao == 'subtração':
        return num1 - num2
    elif operacao == 'multiplicação':
        return num1 * num2
    elif operacao == 'divisão':
        if num2 != 0:
            return num1 / num2
        else:
            return "Erro: Divisão por zero!"
    else:
        return "Operação inválida!"

# Função para calcular raiz quadrada
def raiz_quadrada(num):
    if num < 0:
        return "Erro: Raiz quadrada de número negativo!"
    return math.sqrt(num)

# Função para uma calculadora completa
def calculadora_completa(num1, num2, operacao):
    if operacao in ['adição', 'subtração', 'multiplicação', 'divisão']:
        return calculadora_basica(num1, num2, operacao)
    elif operacao == 'potenciação':
        return num1 ** num2
    elif operacao == 'raiz quadrada':
        return raiz_quadrada(num1)  # Usando a função de raiz quadrada
    else:
        return "Operação inválida!"

# Exemplo de uso
resultado = calculadora_completa(9, 0, 'raiz quadrada')
print("Resultado:", resultado)