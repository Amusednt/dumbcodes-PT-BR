def validar_email(email):
    """
    Verifica se uma string corresponde a um formato de e-mail válido
    usando expressões regulares.
    """
    # Expressão regular para um formato de e-mail comum
    # Esta regex é simplificada e pode não cobrir TODOS os casos,
    # mas é um bom ponto de partida para a maioria das validações.
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(regex, email):
        return True
    else:
        return False

if _name_ == "_main_":
    emails_para_testar = [
        "teste@example.com",
        "usuario.nome@dominio.com.br",
        "email_invalido.com",
        "outro@.com",
        "a@b.c",
        "email@sub.domain.co",
        "nao eh email"
    ]

    print("--- Validação de E-mails ---")
    for email in emails_para_testar:
        if validar_email(email):
            print(f"'{email}': VÁLIDO")
        else:
            print(f"'{email}': INVÁLIDO")
