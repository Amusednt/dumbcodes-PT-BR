def busca_linear(lista, alvo):
    # Inicia uma função chamada busca_linear que recebe uma lista e um alvo a ser encontrado
    for i in range(len(lista)):
        # Itera sobre cada índice 'i' da lista usando a função range para obter o comprimento da lista
        if lista[i] == alvo:
            # Verifica se o elemento na posição 'i' da lista é igual ao alvo
            return i
            # Se for igual, retorna o índice 'i' onde o alvo foi encontrado
    return -1
    # Se o alvo não for encontrado após percorrer toda a lista, retorna -1

# Teste
lista = [1, 2, 3, 4, 5]
# Define uma lista de números de 1 a 5
alvo = 3
# Define o alvo que queremos encontrar na lista
print(busca_linear(lista, alvo))  # Saída: 2
# Chama a função busca_linear e imprime o resultado, que deve ser 2, pois o número 3 está na posição 2 da lista