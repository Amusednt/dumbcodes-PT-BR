#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicativo de Compartilhamento de Arquivos - SERVIDOR
Permite o compartilhamento de arquivos através da rede local
"""

import socket
import threading
import os
import json
import time
from pathlib import Path
import hashlib

class FileServer:
    def __init__(self, host='localhost', port=8888):
        """
        Inicializa o servidor de arquivos
        
        Args:
            host (str): Endereço IP do servidor
            port (int): Porta do servidor
        """
        self.host = host
        self.port = port
        self.socket = None
        self.clients = []  # Lista de clientes conectados
        self.shared_folder = Path("shared_files")  # Pasta de arquivos compartilhados
        self.running = False
        
        # Cria a pasta compartilhada se não existir
        self.shared_folder.mkdir(exist_ok=True)
        
    def start_server(self):
        """Inicia o servidor e fica aguardando conexões"""
        try:
            # Cria o socket do servidor
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Vincula o socket ao endereço e porta
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)  # Permite até 5 conexões pendentes
            
            self.running = True
            print(f"🚀 Servidor iniciado em {self.host}:{self.port}")
            print(f"📁 Pasta compartilhada: {self.shared_folder.absolute()}")
            print("⏳ Aguardando conexões...")
            
            while self.running:
                try:
                    # Aceita conexões de clientes
                    client_socket, client_address = self.socket.accept()
                    print(f"👤 Cliente conectado: {client_address}")
                    
                    # Adiciona cliente à lista
                    self.clients.append(client_socket)
                    
                    # Cria uma thread para cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error:
                    if self.running:
                        print("❌ Erro ao aceitar conexão")
                        
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")
            
    def handle_client(self, client_socket, client_address):
        """
        Manipula as requisições de um cliente específico
        
        Args:
            client_socket: Socket do cliente
            client_address: Endereço do cliente
        """
        try:
            while self.running:
                # Recebe dados do cliente
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                # Processa a requisição
                request = json.loads(data)
                response = self.process_request(request, client_socket)
                
                # Envia resposta (se não for download de arquivo)
                if response:
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    
        except Exception as e:
            print(f"❌ Erro ao manipular cliente {client_address}: {e}")
        finally:
            # Remove cliente da lista e fecha conexão
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"👋 Cliente desconectado: {client_address}")
            
    def process_request(self, request, client_socket):
        """
        Processa diferentes tipos de requisições do cliente
        
        Args:
            request (dict): Requisição do cliente
            client_socket: Socket do cliente
            
        Returns:
            dict: Resposta para o cliente
        """
        action = request.get('action')
        
        if action == 'list_files':
            # Lista arquivos disponíveis
            return self.list_files()
            
        elif action == 'upload_file':
            # Upload de arquivo
            return self.receive_file(request, client_socket)
            
        elif action == 'download_file':
            # Download de arquivo
            self.send_file(request, client_socket)
            return None
            
        elif action == 'delete_file':
            # Deletar arquivo
            return self.delete_file(request)
            
        else:
            return {'status': 'error', 'message': 'Ação não reconhecida'}
            
    def list_files(self):
        """
        Lista todos os arquivos na pasta compartilhada
        
        Returns:
            dict: Lista de arquivos com informações
        """
        try:
            files = []
            for file_path in self.shared_folder.iterdir():
                if file_path.is_file():
                    # Obtém informações do arquivo
                    stat = file_path.stat()
                    files.append({
                        'name': file_path.name,
                        'size': stat.st_size,
                        'modified': time.ctime(stat.st_mtime)
                    })
                    
            return {
                'status': 'success',
                'files': files
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao listar arquivos: {e}'
            }
            
    def receive_file(self, request, client_socket):
        """
        Recebe um arquivo enviado pelo cliente
        
        Args:
            request (dict): Informações do arquivo
            client_socket: Socket do cliente
            
        Returns:
            dict: Status do upload
        """
        try:
            filename = request['filename']
            filesize = request['filesize']
            
            # Caminho completo do arquivo
            file_path = self.shared_folder / filename
            
            print(f"📥 Recebendo arquivo: {filename} ({filesize} bytes)")
            
            # Recebe o arquivo em chunks
            with open(file_path, 'wb') as f:
                bytes_received = 0
                while bytes_received < filesize:
                    chunk = client_socket.recv(min(4096, filesize - bytes_received))
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
                    
            print(f"✅ Arquivo recebido: {filename}")
            return {
                'status': 'success',
                'message': f'Arquivo {filename} enviado com sucesso'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao receber arquivo: {e}'
            }
            
    def send_file(self, request, client_socket):
        """
        Envia um arquivo para o cliente
        
        Args:
            request (dict): Nome do arquivo solicitado
            client_socket: Socket do cliente
        """
        try:
            filename = request['filename']
            file_path = self.shared_folder / filename
            
            if not file_path.exists():
                # Arquivo não encontrado
                response = {
                    'status': 'error',
                    'message': 'Arquivo não encontrado'
                }
                client_socket.send(json.dumps(response).encode('utf-8'))
                return
                
            # Envia informações do arquivo
            filesize = file_path.stat().st_size
            response = {
                'status': 'success',
                'filename': filename,
                'filesize': filesize
            }
            client_socket.send(json.dumps(response).encode('utf-8'))
            
            # Aguarda confirmação do cliente
            client_socket.recv(1024)
            
            print(f"📤 Enviando arquivo: {filename} ({filesize} bytes)")
            
            # Envia o arquivo em chunks
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    client_socket.send(chunk)
                    
            print(f"✅ Arquivo enviado: {filename}")
            
        except Exception as e:
            print(f"❌ Erro ao enviar arquivo: {e}")
            
    def delete_file(self, request):
        """
        Deleta um arquivo da pasta compartilhada
        
        Args:
            request (dict): Nome do arquivo a ser deletado
            
        Returns:
            dict: Status da operação
        """
        try:
            filename = request['filename']
            file_path = self.shared_folder / filename
            
            if not file_path.exists():
                return {
                    'status': 'error',
                    'message': 'Arquivo não encontrado'
                }
                
            file_path.unlink()  # Deleta o arquivo
            print(f"🗑️ Arquivo deletado: {filename}")
            
            return {
                'status': 'success',
                'message': f'Arquivo {filename} deletado com sucesso'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao deletar arquivo: {e}'
            }
            
    def stop_server(self):
        """Para o servidor e fecha todas as conexões"""
        print("\n🛑 Parando servidor...")
        self.running = False
        
        # Fecha conexões com clientes
        for client in self.clients:
            try:
                client.close()
            except:
                pass
                
        # Fecha socket do servidor
        if self.socket:
            self.socket.close()
            
        print("✅ Servidor parado")

def main():
    """Função principal do servidor"""
    print("=" * 50)
    print("🚀 SERVIDOR DE COMPARTILHAMENTO DE ARQUIVOS")
    print("=" * 50)
    
    # Configurações do servidor
    host = input("Digite o IP do servidor (Enter para localhost): ").strip()
    if not host:
        host = 'localhost'
        
    try:
        port = input("Digite a porta (Enter para 8888): ").strip()
        port = int(port) if port else 8888
    except ValueError:
        port = 8888
        
    # Cria e inicia o servidor
    server = FileServer(host, port)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop_server()

if __name__ == "__main__":
    main()