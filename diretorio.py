import os
import shutil

def organizar_arquivos(diretorio_origem):
    """
    Organiza arquivos em um diretório, movendo-os para subpastas
    baseadas em suas extensões.

    Args:
        diretorio_origem (str): O caminho do diretório a ser organizado.
    """
    if not os.path.isdir(diretorio_origem):
        print(f"Erro: O diretório '{diretorio_origem}' não existe.")
        return

    print(f"Iniciando organização em: {diretorio_origem}\n")

    for nome_arquivo in os.listdir(diretorio_origem):
        caminho_completo_arquivo = os.path.join(diretorio_origem, nome_arquivo)

        # Ignorar diretórios
        if os.path.isdir(caminho_completo_arquivo):
            continue

        # Obter a extensão do arquivo
        _, extensao = os.path.splitext(nome_arquivo)
        extensao = extensao.lower() # Converter para minúsculas para padronização

        if not extensao: # Ignorar arquivos sem extensão (ou diretórios)
            continue

        # Remover o ponto da extensão para usar como nome da pasta
        nome_pasta = extensao[1:] if extensao.startswith('.') else "outros"

        caminho_pasta_destino = os.path.join(diretorio_origem, nome_pasta)

        # Criar a pasta de destino se ela não existir
        if not os.path.exists(caminho_pasta_destino):
            os.makedirs(caminho_pasta_destino)
            print(f"Criada pasta: {caminho_pasta_destino}")

        # Mover o arquivo
        try:
            shutil.move(caminho_completo_arquivo, caminho_pasta_destino)
            print(f"Movido: '{nome_arquivo}' para '{nome_pasta}/'")
        except shutil.Error as e:
            print(f"Erro ao mover '{nome_arquivo}': {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao mover '{nome_arquivo}': {e}")

    print("\nOrganização concluída!")

if _name_ == "_main_":
    # Exemplo de uso:
    # Crie uma pasta 'meus_arquivos_baguncados' e coloque alguns arquivos de teste lá.
    # Por exemplo: imagem.jpg, documento.pdf, script.py, texto.txt, etc.
    
    # Para testar, você pode criar uma pasta temporária com alguns arquivos
    # antes de rodar o script.
    
    # Caminho do diretório que você quer organizar.
    # ATENÇÃO: MUDAR PARA O DIRETÓRIO CORRETO ANTES DE EXECUTAR!
    diretorio_para_organizar = "C:\\Users\\SeuUsuario\\Documentos\\MeusArquivosBaguncados" 
    # ou "./MeusArquivosBaguncados" se for um diretório na mesma pasta do script
    
    organizar_arquivos(diretorio_para_organizar)

    # Dica: Você pode descomentar as linhas abaixo para criar alguns arquivos de teste
    # e um diretório temporário para experimentar o script sem afetar seus arquivos reais.
    """
    # Exemplo de criação de arquivos de teste (descomente para usar)
    test_dir = "./teste_organizacao"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        
    with open(os.path.join(test_dir, "documento.pdf"), "w") as f: f.write("pdf")
    with open(os.path.join(test_dir, "imagem.jpg"), "w") as f: f.write("jpg")
    with open(os.path.join(test_dir, "script.py"), "w") as f: f.write("python")
    with open(os.path.join(test_dir, "relatorio.docx"), "w") as f: f.write("word")
    with open(os.path.join(test_dir, "dados.xlsx"), "w") as f: f.write("excel")
    with open(os.path.join(test_dir, "musica.mp3"), "w") as f: f.write("mp3")
    with open(os.path.join(test_dir, "arquivo_sem_extensao"), "w") as f: f.write("sem_extensao")

    print(f"\nArquivos de teste criados em: {test_dir}")
    print("Execute o script com 'diretorio_para_organizar = \"./teste_organizacao\"' para testar.")
    # organizar_arquivos(test_dir) # Descomente para rodar direto nos arquivos de teste
    """