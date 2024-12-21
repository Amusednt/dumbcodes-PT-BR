def busca_linear(lista, alvo):
    # Retorna o índice do alvo na lista ou -1 se não encontrado
    resultado = lista.index(alvo) if alvo in lista else -1
    return resultado

def ordenacao_selecao(lista):
    # Ordena a lista usando o algoritmo de ordenação por seleção
    for i in range(len(lista)):
        minimo = i  # Assume que o primeiro elemento é o mínimo
        for j in range(i + 1, len(lista)):
            # Se encontrar um elemento menor, atualiza o índice do mínimo
            if lista[j] < lista[minimo]:
                minimo = j
        # Troca o elemento atual com o mínimo encontrado
        lista[i], lista[minimo] = lista[minimo], lista[i]
    return lista  # Retorna a lista ordenada

def busca_binaria(lista, alvo):
    # Realiza a busca binária para encontrar o índice do alvo
    inicio = 0
    fim = len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2  # Calcula o índice do meio
        if lista[meio] == alvo:
            return meio  # Retorna o índice se o alvo for encontrado
        elif lista[meio] < alvo:
            inicio = meio + 1  # Ajusta o início se o alvo for maior
        else:
            fim = meio - 1  # Ajusta o fim se o alvo for menor
    return -1  # Retorna -1 se o alvo não for encontrado

# Exemplo de uso
lista = [5, 3, 8, 1, 2]
alvo_linear = 3
alvo_binario = 8

# Ordenação
lista_ordenada = ordenacao_selecao(lista)
print(f'Ordenação por Seleção: Lista ordenada é {lista_ordenada}')

# Busca Linear
resultado_linear = busca_linear(lista_ordenada, alvo_linear)
print(f'Busca Linear: O índice do alvo {alvo_linear} é {resultado_linear}')

# Busca Binária
resultado_binaria = busca_binaria(lista_ordenada, alvo_binario)
print(f'Busca Binária: O índice do alvo {alvo_binario} é {resultado_binaria}')