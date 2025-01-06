# Função para decidir se uma pessoa gosta de cartão de crédito
def gosta_de_cartao_de_credito(idade, estado_civil):
    """
    Função que decide se uma pessoa gosta de cartão de crédito com base na idade e estado civil.
    
    Parâmetros:
    idade (int): Idade da pessoa.
    estado_civil (str): Estado civil da pessoa ('casado' ou 'solteiro').
    
    Retorna:
    str: "Gosta de cartão de crédito" ou "Não gosta de cartão de crédito".
    """
    # Nó Raiz: Verifica se a idade é maior que 30
    if idade > 30:
        return "Gosta de cartão de crédito"
    else:
        # Nó Filho: Verifica o estado civil
        if estado_civil == "casado":
            return "Gosta de cartão de crédito"
        else:
            return "Não gosta de cartão de crédito"

# Exemplo de uso da função
idade = 35
estado_civil = "solteiro"
resultado = gosta_de_cartao_de_credito(idade, estado_civil)
print(f"Idade: {idade}, Estado Civil: {estado_civil} -> {resultado}")

idade = 25
estado_civil = "casado"
resultado = gosta_de_cartao_de_credito(idade, estado_civil)
print(f"Idade: {idade}, Estado Civil: {estado_civil} -> {resultado}")

idade = 28
estado_civil = "solteiro"
resultado = gosta_de_cartao_de_credito(idade, estado_civil)
print(f"Idade: {idade}, Estado Civil: {estado_civil} -> {resultado}")