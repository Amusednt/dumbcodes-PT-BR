def busca_binaria(lista, alvo):
    # Inicializa o índice do início da lista
    inicio = 0
    # Inicializa o índice do fim da lista
    fim = len(lista) - 1
    
    # Enquanto o índice do início for menor ou igual ao índice do fim
    while inicio <= fim:
        # Calcula o índice do meio da lista
        meio = (inicio + fim) // 2
        
        # Verifica se o elemento no meio é o alvo
        if lista[meio] == alvo:
            # Retorna o índice do elemento encontrado
            return meio
        # Se o elemento no meio é menor que o alvo, busca na metade direita
        elif lista[meio] < alvo:
            inicio = meio + 1
        # Se o elemento no meio é maior que o alvo, busca na metade esquerda
        else:
            fim = meio - 1
            
    # Se o alvo não for encontrado, retorna -1
    return -1

# Teste da função
lista = [1, 2, 3, 4, 5]  # Lista ordenada para busca
alvo = 3  # Elemento que estamos buscando
print(busca_binaria(lista, alvo))  # Saída: 2 (índice do elemento 3 na lista)