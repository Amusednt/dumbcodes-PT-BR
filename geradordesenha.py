import random
import string
import secrets

def gerar_senha(comprimento=12, incluir_maiusculas=True, incluir_minusculas=True, 
                incluir_numeros=True, incluir_simbolos=True, excluir_ambiguos=False):
    """
    Gera uma senha aleatória com base nos parâmetros especificados.
    
    Args:
        comprimento (int): Comprimento da senha (padrão: 12)
        incluir_maiusculas (bool): Incluir letras maiúsculas (padrão: True)
        incluir_minusculas (bool): Incluir letras minúsculas (padrão: True)
        incluir_numeros (bool): Incluir números (padrão: True)
        incluir_simbolos (bool): Incluir símbolos especiais (padrão: True)
        excluir_ambiguos (bool): Excluir caracteres ambíguos como 0, O, l, I (padrão: False)
    
    Returns:
        str: Senha gerada
    """
    
    # Conjuntos de caracteres disponíveis
    maiusculas = string.ascii_uppercase  # A-Z
    minusculas = string.ascii_lowercase  # a-z
    numeros = string.digits             # 0-9
    simbolos = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Caracteres que podem ser confundidos visualmente
    caracteres_ambiguos = "0Ol1I"
    
    # Construir o conjunto de caracteres baseado nas opções selecionadas
    caracteres_disponiveis = ""
    
    if incluir_maiusculas:
        caracteres_disponiveis += maiusculas
    
    if incluir_minusculas:
        caracteres_disponiveis += minusculas
    
    if incluir_numeros:
        caracteres_disponiveis += numeros
    
    if incluir_simbolos:
        caracteres_disponiveis += simbolos
    
    # Remover caracteres ambíguos se solicitado
    if excluir_ambiguos:
        caracteres_disponiveis = ''.join(char for char in caracteres_disponiveis 
                                       if char not in caracteres_ambiguos)
    
    # Verificar se pelo menos um tipo de caractere foi selecionado
    if not caracteres_disponiveis:
        raise ValueError("Pelo menos um tipo de caractere deve ser incluído!")
    
    # Gerar a senha usando secrets (mais seguro que random para criptografia)
    senha = ''.join(secrets.choice(caracteres_disponiveis) for _ in range(comprimento))
    
    return senha

def avaliar_forca_senha(senha):
    """
    Avalia a força de uma senha baseada em critérios de segurança.
    
    Args:
        senha (str): A senha a ser avaliada
    
    Returns:
        tuple: (pontuação, classificação, sugestões)
    """
    pontuacao = 0
    sugestoes = []
    
    # Verificar comprimento
    if len(senha) >= 12:
        pontuacao += 25
    elif len(senha) >= 8:
        pontuacao += 15
    else:
        sugestoes.append("Use pelo menos 8 caracteres (recomendado: 12+)")
    
    # Verificar presença de letras minúsculas
    if any(c.islower() for c in senha):
        pontuacao += 15
    else:
        sugestoes.append("Inclua letras minúsculas")
    
    # Verificar presença de letras maiúsculas
    if any(c.isupper() for c in senha):
        pontuacao += 15
    else:
        sugestoes.append("Inclua letras maiúsculas")
    
    # Verificar presença de números
    if any(c.isdigit() for c in senha):
        pontuacao += 15
    else:
        sugestoes.append("Inclua números")
    
    # Verificar presença de símbolos especiais
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in senha):
        pontuacao += 20
    else:
        sugestoes.append("Inclua símbolos especiais")
    
    # Verificar repetição de caracteres
    if len(set(senha)) == len(senha):
        pontuacao += 10
    else:
        sugestoes.append("Evite repetir caracteres")
    
    # Classificar a força da senha
    if pontuacao >= 80:
        classificacao = "Muito Forte"
    elif pontuacao >= 60:
        classificacao = "Forte"
    elif pontuacao >= 40:
        classificacao = "Média"
    elif pontuacao >= 20:
        classificacao = "Fraca"
    else:
        classificacao = "Muito Fraca"
    
    return pontuacao, classificacao, sugestoes

def gerar_multiplas_senhas(quantidade=5, **kwargs):
    """
    Gera múltiplas senhas de uma vez.
    
    Args:
        quantidade (int): Número de senhas a gerar
        **kwargs: Parâmetros para passar para gerar_senha()
    
    Returns:
        list: Lista de senhas geradas
    """
    return [gerar_senha(**kwargs) for _ in range(quantidade)]

def main():
    """
    Função principal que executa o gerador de senhas interativo.
    """
    print("=== GERADOR DE SENHAS SEGURAS ===\n")
    
    while True:
        try:
            # Solicitar parâmetros do usuário
            print("Configurações da senha:")
            comprimento = int(input("Comprimento da senha (padrão 12): ") or 12)
            
            # Opções de caracteres
            incluir_maiusculas = input("Incluir letras maiúsculas? (S/n): ").lower() != 'n'
            incluir_minusculas = input("Incluir letras minúsculas? (S/n): ").lower() != 'n'
            incluir_numeros = input("Incluir números? (S/n): ").lower() != 'n'
            incluir_simbolos = input("Incluir símbolos especiais? (S/n): ").lower() != 'n'
            excluir_ambiguos = input("Excluir caracteres ambíguos (0,O,l,1,I)? (s/N): ").lower() == 's'
            
            # Quantidade de senhas
            quantidade = int(input("Quantas senhas gerar? (padrão 1): ") or 1)
            
            print("\n" + "="*50)
            
            # Gerar as senhas
            if quantidade == 1:
                senha = gerar_senha(
                    comprimento=comprimento,
                    incluir_maiusculas=incluir_maiusculas,
                    incluir_minusculas=incluir_minusculas,
                    incluir_numeros=incluir_numeros,
                    incluir_simbolos=incluir_simbolos,
                    excluir_ambiguos=excluir_ambiguos
                )
                
                print(f"Senha gerada: {senha}")
                
                # Avaliar a força da senha
                pontuacao, classificacao, sugestoes = avaliar_forca_senha(senha)
                print(f"\nAvaliação da senha:")
                print(f"Pontuação: {pontuacao}/100")
                print(f"Classificação: {classificacao}")
                
                if sugestoes:
                    print("Sugestões para melhorar:")
                    for sugestao in sugestoes:
                        print(f"  • {sugestao}")
                        
            else:
                senhas = gerar_multiplas_senhas(
                    quantidade=quantidade,
                    comprimento=comprimento,
                    incluir_maiusculas=incluir_maiusculas,
                    incluir_minusculas=incluir_minusculas,
                    incluir_numeros=incluir_numeros,
                    incluir_simbolos=incluir_simbolos,
                    excluir_ambiguos=excluir_ambiguos
                )
                
                print("Senhas geradas:")
                for i, senha in enumerate(senhas, 1):
                    print(f"{i:2d}. {senha}")
            
            print("\n" + "="*50)
            
            # Perguntar se deseja continuar
            continuar = input("\nGerar mais senhas? (s/N): ").lower() == 's'
            if not continuar:
                break
                
            print()  # Linha em branco para separar as execuções
            
        except ValueError as e:
            print(f"Erro: {e}")
        except KeyboardInterrupt:
            print("\n\nPrograma encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")

# Executar o programa se for chamado diretamente
if __name__ == "__main__":
    main()