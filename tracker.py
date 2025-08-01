import json
import os
from datetime import datetime

class TrackerApp:
    def __init__(self, filename="tracker_data.json"):
        """
        Inicializa o aplicativo rastreador.
        Carrega os dados existentes do arquivo ou inicia com uma lista vazia.
        """
        self.filename = filename
        self.items = self.load_data()
        self.next_id = max([item['id'] for item in self.items] + [0]) + 1

    def load_data(self):
        """
        Carrega os itens e comentários do arquivo JSON.
        Se o arquivo não existir, retorna uma lista vazia.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Lida com o caso de um arquivo JSON vazio ou corrompido
                    return []
        return []

    def save_data(self):
        """
        Salva os itens e comentários atuais no arquivo JSON.
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, indent=4, ensure_ascii=False)

    def add_item(self, description):
        """
        Adiciona um novo item ao rastreador.
        Cada item tem um ID único, descrição, status e uma lista de comentários.
        """
        item = {
            'id': self.next_id,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'comments': []
        }
        self.items.append(item)
        self.next_id += 1
        self.save_data()
        print(f"Item '{description}' (ID: {item['id']}) adicionado com sucesso.")

    def view_items(self):
        """
        Exibe todos os itens rastreados, incluindo seus status e comentários.
        """
        if not self.items:
            print("Nenhum item para exibir. Adicione um novo item primeiro.")
            return

        print("\n--- Seus Itens Rastreados ---")
        for item in self.items:
            status = "Concluído" if item['completed'] else "Pendente"
            print(f"ID: {item['id']}")
            print(f"  Descrição: {item['description']}")
            print(f"  Status: {status}")
            print(f"  Criado em: {item['created_at']}")
            if item['comments']:
                print("  Comentários:")
                for comment in item['comments']:
                    print(f"    - [{comment['timestamp']}] {comment['text']}")
            else:
                print("  Nenhum comentário.")
            print("-" * 30)
        print("----------------------------")

    def add_comment(self, item_id, comment_text):
        """
        Adiciona um comentário a um item existente.
        """
        for item in self.items:
            if item['id'] == item_id:
                comment = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'text': comment_text
                }
                item['comments'].append(comment)
                self.save_data()
                print(f"Comentário adicionado ao item ID {item_id}.")
                return
        print(f"Erro: Item com ID {item_id} não encontrado.")

    def mark_completed(self, item_id, completed=True):
        """
        Marca um item como concluído ou pendente.
        """
        for item in self.items:
            if item['id'] == item_id:
                item['completed'] = completed
                self.save_data()
                status = "concluído" if completed else "pendente"
                print(f"Item ID {item_id} marcado como {status}.")
                return
        print(f"Erro: Item com ID {item_id} não encontrado.")

    def delete_item(self, item_id):
        """
        Exclui um item do rastreador.
        """
        initial_len = len(self.items)
        self.items = [item for item in self.items if item['id'] != item_id]
        if len(self.items) < initial_len:
            self.save_data()
            print(f"Item ID {item_id} excluído com sucesso.")
        else:
            print(f"Erro: Item com ID {item_id} não encontrado.")

    def display_menu(self):
        """
        Exibe o menu de opções para o usuário.
        """
        print("\n--- Menu do Aplicativo Rastreador ---")
        print("1. Adicionar novo item")
        print("2. Ver todos os itens")
        print("3. Adicionar comentário a um item")
        print("4. Marcar item como concluído/pendente")
        print("5. Excluir item")
        print("6. Sair")
        print("------------------------------------")

    def run(self):
        """
        Executa o loop principal do aplicativo, lidando com a entrada do usuário.
        """
        while True:
            self.display_menu()
            choice = input("Escolha uma opção: ")

            if choice == '1':
                description = input("Digite a descrição do novo item: ")
                self.add_item(description)
            elif choice == '2':
                self.view_items()
            elif choice == '3':
                try:
                    item_id = int(input("Digite o ID do item para comentar: "))
                    comment_text = input("Digite seu comentário: ")
                    self.add_comment(item_id, comment_text)
                except ValueError:
                    print("ID inválido. Por favor, digite um número.")
            elif choice == '4':
                try:
                    item_id = int(input("Digite o ID do item para marcar: "))
                    status_choice = input("Marcar como (c)oncluído ou (p)endente? (c/p): ").lower()
                    if status_choice == 'c':
                        self.mark_completed(item_id, True)
                    elif status_choice == 'p':
                        self.mark_completed(item_id, False)
                    else:
                        print("Opção inválida. Por favor, digite 'c' ou 'p'.")
                except ValueError:
                    print("ID inválido. Por favor, digite um número.")
            elif choice == '5':
                try:
                    item_id = int(input("Digite o ID do item para excluir: "))
                    self.delete_item(item_id)
                except ValueError:
                    print("ID inválido. Por favor, digite um número.")
            elif choice == '6':
                print("Saindo do aplicativo. Até mais!")
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    app = TrackerApp()
    app.run()
