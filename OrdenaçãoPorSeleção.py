def ordenacao_selecao(lista):
    # Itera sobre cada elemento da lista
    for i in range(len(lista)):
        # Assume que o elemento atual é o mínimo
        minimo = i
        # Compara o elemento atual com os elementos restantes da lista
        for j in range(i + 1, len(lista)):
            # Se encontrar um elemento menor, atualiza o índice do mínimo
            if lista[j] < lista[minimo]:
                minimo = j
        # Troca o elemento atual com o menor encontrado
        lista[i], lista[minimo] = lista[minimo], lista[i]
    # Retorna a lista ordenada
    return lista

# Teste da função de ordenação
lista = [5, 2, 8, 1, 9]
# Imprime a lista ordenada
print(ordenacao_selecao(lista))  # Saída: [1, 2, 5, 8, 9]

#Definição da Função: def ordenacao_selecao(lista): - Define a função que recebe uma lista como argumento.
#Loop Externo: for i in range(len(lista)): - Itera sobre cada índice da lista.
#Inicialização do Mínimo: minimo = i - Assume que o elemento na posição i é o menor.
#Loop Interno: for j in range(i + 1, len(lista)): - Compara o elemento atual com os elementos que vêm depois dele.
#Verificação do Mínimo: if lista[j] < lista[minimo]: - Se encontrar um elemento menor, atualiza o índice do mínimo.
#Troca de Elementos: lista[i], lista[minimo] = lista[minimo], lista[i] - Troca o elemento atual com o menor encontrado.
#Retorno da Lista: return lista - Retorna a lista já ordenada.
#Teste da Função: lista = [5, 2, 8, 1, 9] - Cria uma lista para testar a função.
#Impressão do Resultado: print(ordenacao_selecao(lista)) - Imprime a lista ordenada.