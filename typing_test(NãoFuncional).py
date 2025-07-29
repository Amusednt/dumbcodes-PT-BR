import time

def get_random_text():
    """Retorna um trecho de texto aleatório para o teste."""
    texts = [
        "A ligeira raposa marrom salta sobre o cão preguiçoso.",
        "Programar em Python é divertido e gratificante.",
        "A prática leva à perfeição quando se trata de digitação.",
        "O sol sempre nasce, mesmo nas manhãs mais nubladas.",
        "A paciência é uma virtude que poucos conseguem dominar completamente."
    ]
    import random
    return random.choice(texts)

def calculate_wpm(start_time, end_time, typed_text):
    """Calcula as palavras por minuto (WPM)."""
    time_taken = end_time - start_time
    words = len(typed_text.split())
    # WPM = (número de palavras / tempo em minutos)
    wpm = (words / time_taken) * 60
    return wpm

def calculate_accuracy(original_text, typed_text):
    """Calcula a precisão da digitação."""
    correct_chars = 0
    min_length = min(len(original_text), len(typed_text))

    for i in range(min_length):
        if original_text[i] == typed_text[i]:
            correct_chars += 1

    # Adiciona a penalidade para caracteres extras/faltando
    accuracy = (correct_chars / len(original_text)) * 100
    return accuracy

def speed_typing_test():
    """Executa o teste de velocidade de digitação."""
    print("Bem-vindo ao Teste de Velocidade de Digitação!")
    print("Você terá que digitar o texto abaixo o mais rápido e precisamente possível.")
    print("\nPressione ENTER para iniciar quando estiver pronto...")
    input() # Espera o usuário pressionar Enter

    original_text = get_random_text()
    print("\n--- Texto para Digitar ---")
    print(original_text)
    print("--------------------------\n")

    start_time = time.time()
    typed_text = input("Comece a digitar aqui: ")
    end_time = time.time()

    wpm = calculate_wpm(start_time, end_time, typed_text)
    accuracy = calculate_accuracy(original_text, typed_text)

    print("\n--- Resultados ---")