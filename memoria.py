import random
import os
import time

# --- Configurações do Jogo ---

# Definimos os pares de símbolos que serão usados no jogo.
# Para mais pares, basta adicionar mais letras ou símbolos aqui.
simbolos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Quantidade de pares que queremos no jogo.
# Precisa ser menor ou igual ao número de símbolos.
num_pares = 6

# --- Inicialização do Jogo ---

# 1. Cria a lista de pares.
# A lista de pares será o dobro do número de pares,
# pois cada símbolo aparece duas vezes.
pares_jogo = simbolos[:num_pares] * 2

# 2. Embaralha a lista para que os pares fiquem em posições aleatórias.
random.shuffle(pares_jogo)

# 3. Cria a lista que representa o tabuleiro "escondido".
# Inicialmente, todas as cartas estão viradas para baixo, representadas por 'X'.
tabuleiro_escondido = ['X'] * len(pares_jogo)

# 4. Define as variáveis de controle do jogo.
jogadas = 0
pares_encontrados = 0

# --- Funções do Jogo ---

def limpar_tela():
    """Função para limpar o console, tornando a visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_tabuleiro():
    """Mostra o tabuleiro atual do jogo com as cartas viradas e as escondidas."""
    print('  1   2   3   4')
    print('-----------------')
    for i in range(len(tabuleiro_escondido)):
        # Adiciona uma nova linha a cada 4 cartas para formar uma grade.
        if i > 0 and i % 4 == 0:
            print('\n')
        # Imprime o conteúdo da carta (virada ou escondida) seguido de um espaço.
        print(f'| {tabuleiro_escondido[i]} |', end='')
    print('\n-----------------')

def pegar_jogada():
    """Pede ao jogador para escolher uma posição e valida a entrada."""
    while True:
        try:
            # Pede a posição da carta e converte para um índice de lista (começa em 0).
            posicao = int(input('Escolha uma carta (1-12): ')) - 1
            
            # Verifica se a posição é válida (dentro dos limites do tabuleiro).
            if 0 <= posicao < len(pares_jogo):
                # Verifica se a carta já não foi virada ou não é um par encontrado.
                if tabuleiro_escondido[posicao] == 'X':
                    return posicao
                else:
                    print('Esta carta já foi virada ou é um par. Escolha outra.')
            else:
                print('Posição inválida. Por favor, escolha um número de 1 a 12.')
        except ValueError:
            print('Entrada inválida. Por favor, digite um número.')

# --- Loop Principal do Jogo ---

limpar_tela()
print('Bem-vindo ao Jogo da Memória!')
time.sleep(2)

# O jogo continua enquanto não encontrarmos todos os pares.
while pares_encontrados < num_pares:
    
    limpar_tela()
    mostrar_tabuleiro()

    # --- Primeira Jogada ---
    print(f'Jogada {jogadas + 1}. Escolha a primeira carta.')
    posicao1 = pegar_jogada()
    
    # Vira a primeira carta no tabuleiro para que o jogador possa vê-la.
    tabuleiro_escondido[posicao1] = pares_jogo[posicao1]
    
    limpar_tela()
    mostrar_tabuleiro()

    # --- Segunda Jogada ---
    print('Escolha a segunda carta.')
    posicao2 = pegar_jogada()
    
    # Vira a segunda carta no tabuleiro.
    tabuleiro_escondido[posicao2] = pares_jogo[posicao2]
    
    limpar_tela()
    mostrar_tabuleiro()
    
    # --- Verificação do Par ---
    print('Analisando as cartas...')
    time.sleep(2) # Pausa para o jogador ver as cartas.

    if pares_jogo[posicao1] == pares_jogo[posicao2]:
        # Se as cartas são iguais, é um par!
        print('Par encontrado! Parabéns!')
        pares_encontrados += 1
        # As cartas ficam viradas, então não voltamos a 'X'.
    else:
        # Se as cartas são diferentes, vira-as de volta.
        print('Não é um par. Tente novamente!')
        tabuleiro_escondido[posicao1] = 'X'
        tabuleiro_escondido[posicao2] = 'X'
    
    # Incrementa o contador de jogadas e pausa antes da próxima rodada.
    jogadas += 1
    time.sleep(2)

# --- Fim do Jogo ---
limpar_tela()
print('Parabéns! Você encontrou todos os pares!')
print(f'Você venceu o jogo em {jogadas} jogadas.')