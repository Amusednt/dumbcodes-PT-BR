import collections
import re

def contar_frequencia_palavras(texto):
    """
    Conta a frequência de cada palavra em um texto.
    Ignora pontuações e diferencia maiúsculas de minúsculas.
    """
    # Converte para minúsculas e remove pontuações, mantendo apenas letras e espaços
    texto_limpo = re.sub(r'[^\w\s]', '', texto).lower()
    
    # Divide o texto em palavras
    palavras = texto_limpo.split()
    
    # Usa collections.Counter para contar a frequência
    frequencia = collections.Counter(palavras)
    
    return frequencia

if __name__ == "__main__":
    paragrafo = """
    Python é uma linguagem de programação de alto nível, interpretada,
    de script, imperativa, orientada a objetos, funcional e multi-paradigma.
    Ela possui uma tipagem dinâmica forte e é de código aberto.
    """
    
    contagem = contar_frequencia_palavras(paragrafo)
    
    print("Frequência de palavras:")
    for palavra, count in contagem.most_common(5): # As 5 palavras mais comuns
        print(f"'{palavra}': {count}")

    print("\n--- Todas as palavras e suas contagens ---")
    for palavra, count in sorted(contagem.items()):
        print(f"'{palavra}': {count}")


