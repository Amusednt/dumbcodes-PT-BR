#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicativo de Compartilhamento de Arquivos - CLIENTE
Interface gráfica para conectar ao servidor e gerenciar arquivos
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import socket
import json
import os
import threading
from pathlib import Path

class FileClient:
    def __init__(self, root):
        """
        Inicializa o cliente com interface gráfica
        
        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.socket = None
        self.connected = False
        
        # Configuração da janela principal
        self.root.title("📁 File Sharing Client")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variáveis para configuração
        self.host_var = tk.StringVar(value="localhost")
        self.port_var = tk.StringVar(value="8888")
        
        # Cria a interface
        self.create_interface()
        
    def create_interface(self):
        """Cria todos os elementos da interface gráfica"""
        
        # === FRAME DE CONEXÃO ===
        connection_frame = ttk.LabelFrame(self.root, text="🔌 Conexão", padding=10)
        connection_frame.pack(fill="x", padx=10, pady=5)
        
        # Campos de host e porta
        ttk.Label(connection_frame, text="Servidor:").grid(row=0, column=0, sticky="w", padx=5)
        host_entry = ttk.Entry(connection_frame, textvariable=self.host_var, width=20)
        host_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(connection_frame, text="Porta:").grid(row=0, column=2, sticky="w", padx=5)
        port_entry = ttk.Entry(connection_frame, textvariable=self.port_var, width=10)
        port_entry.grid(row=0, column=3, padx=5)
        
        # Botões de conexão
        self.connect_btn = ttk.Button(
            connection_frame, 
            text="🔗 Conectar", 
            command=self.connect_to_server
        )
        self.connect_btn.grid(row=0, column=4, padx=10)
        
        self.disconnect_btn = ttk.Button(
            connection_frame, 
            text="❌ Desconectar", 
            command=self.disconnect_from_server,
            state="disabled"
        )
        self.disconnect_btn.grid(row=0, column=5, padx=5)
        
        # Status da conexão
        self.status_var = tk.StringVar(value="❌ Desconectado")
        status_label = ttk.Label(connection_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, columnspan=6, pady=5)
        
        # === FRAME DE ARQUIVOS ===
        files_frame = ttk.LabelFrame(self.root, text="📂 Arquivos no Servidor", padding=10)
        files_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Lista de arquivos com scrollbar
        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill="both", expand=True)
        
        # Configuração do Treeview para lista de arquivos
        columns = ("Nome", "Tamanho", "Modificado")
        self.files_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configuração das colunas
        self.files_tree.heading("Nome", text="📄 Nome do Arquivo")
        self.files_tree.heading("Tamanho", text="📊 Tamanho")
        self.files_tree.heading("Modificado", text="📅 Última Modificação")
        
        self.files_tree.column("Nome", width=300)
        self.files_tree.column("Tamanho", width=100, anchor="center")
        self.files_tree.column("Modificado", width=200, anchor="center")
        
        # Scrollbars para a lista
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.files_tree.xview)
        
        self.files_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Posicionamento da lista e scrollbars
        self.files_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # === FRAME DE AÇÕES ===
        actions_frame = ttk.LabelFrame(self.root, text="⚡ Ações", padding=10)
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        # Botões de ação
        ttk.Button(
            actions_frame, 
            text="🔄 Atualizar Lista", 
            command=self.refresh_files
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            actions_frame, 
            text="📤 Enviar Arquivo", 
            command=self.upload_file
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            actions_frame, 
            text="📥 Baixar Arquivo", 
            command=self.download_file
        ).grid(row=0, column=2, padx=5)
        
        ttk.Button(
            actions_frame, 
            text="🗑️ Deletar Arquivo", 
            command=self.delete_file
        ).grid(row=0, column=3, padx=5)
        
        # === FRAME DE LOG ===
        log_frame = ttk.LabelFrame(self.root, text="📋 Log de Atividades", padding=10)
        log_frame.pack(fill="x", padx=10, pady=5)
        
        # Área de texto para log
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, wrap=tk.WORD)
        self.log_text.pack(fill="both", expand=True)
        
        # Log inicial
        self.log("🚀 Cliente iniciado. Conecte-se a um servidor para começar.")
        
    def log(self, message):
        """
        Adiciona uma mensagem ao log
        
        Args:
            message (str): Mensagem para adicionar ao log
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)  # Scroll automático para a última linha
        self.root.update()  # Atualiza a interface
        
    def connect_to_server(self):
        """Conecta ao servidor de arquivos"""
        try:
            host = self.host_var.get().strip()
            port = int(self.port_var.get().strip())
            
            if not host:
                messagebox.showerror("Erro", "Digite o endereço do servidor")
                return
                
            self.log(f"🔗 Conectando a {host}:{port}...")
            
            # Cria socket e conecta
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # Timeout de 10 segundos
            self.socket.connect((host, port))
            
            self.connected = True
            self.status_var.set(f"✅ Conectado a {host}:{port}")
            
            # Atualiza interface
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            
            self.log("✅ Conectado com sucesso!")
            
            # Carrega lista de arquivos
            self.refresh_files()
            
        except ValueError:
            messagebox.showerror("Erro", "Porta deve ser um número")
        except socket.timeout:
            messagebox.showerror("Erro", "Timeout: Servidor não responde")
            self.log("❌ Timeout: Servidor não responde")
        except ConnectionRefusedError:
            messagebox.showerror("Erro", "Conexão recusada. Verifique se o servidor está executando.")
            self.log("❌ Conexão recusada")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar: {e}")
            self.log(f"❌ Erro ao conectar: {e}")
            
    def disconnect_from_server(self):
        """Desconecta do servidor"""
        try:
            if self.socket:
                self.socket.close()
                self.socket = None
                
            self.connected = False
            self.status_var.set("❌ Desconectado")
            
            # Atualiza interface
            self.connect_btn.config(state="normal")
            self.disconnect_btn.config(state="disabled")
            
            # Limpa lista de arquivos
            for item in self.files_tree.get_children():
                self.files_tree.delete(item)
                
            self.log("👋 Desconectado do servidor")
            
        except Exception as e:
            self.log(f"❌ Erro ao desconectar: {e}")
            
    def send_request(self, request):
        """
        Envia uma requisição para o servidor
        
        Args:
            request (dict): Requisição a ser enviada
            
        Returns:
            dict: Resposta do servidor ou None em caso de erro
        """
        try:
            if not self.connected or not self.socket:
                messagebox.showerror("Erro", "Não conectado ao servidor")
                return None
                
            # Envia requisição
            self.socket.send(json.dumps(request).encode('utf-8'))
            
            # Recebe resposta
            response = self.socket.recv(4096).decode('utf-8')
            return json.loads(response)
            
        except Exception as e:
            self.log(f"❌ Erro na comunicação: {e}")
            messagebox.showerror("Erro", f"Erro na comunicação: {e}")
            return None
            
    def refresh_files(self):
        """Atualiza a lista de arquivos do servidor"""
        if not self.connected:
            messagebox.showwarning("Aviso", "Conecte-se ao servidor primeiro")
            return
            
        self.log("🔄 Atualizando lista de arquivos...")
        
        # Solicita lista de arquivos
        response = self.send_request({'action': 'list_files'})
        
        if response and response.get('status') == 'success':
            # Limpa lista atual
            for item in self.files_tree.get_children():
                self.files_tree.delete(item)
                
            # Adiciona arquivos à lista
            files = response.get('files', [])
            for file_info in files:
                # Formata tamanho do arquivo
                size = file_info['size']
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):.1f} MB"
                    
                # Adiciona à lista
                self.files_tree.insert("", "end", values=(
                    file_info['name'],
                    size_str,
                    file_info['modified']
                ))
                
            self.log(f"✅ {len(files)} arquivo(s) encontrado(s)")
        else:
            error_msg = response.get('message', 'Erro desconhecido') if response else 'Sem resposta'
            self.log(f"❌ Erro ao listar arquivos: {error_msg}")
            
    def upload_file(self):
        """Envia um arquivo para o servidor"""
        if not self.connected:
            messagebox.showwarning("Aviso", "Conecte-se ao servidor primeiro")
            return
            
        # Seleciona arquivo para enviar
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo para enviar",
            filetypes=[("Todos os arquivos", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            file_path = Path(file_path)
            filename = file_path.name
            filesize = file_path.stat().st_size
            
            self.log(f"📤 Enviando arquivo: {filename} ({filesize} bytes)")
            
            # Envia informações do arquivo
            request = {
                'action': 'upload_file',
                'filename': filename,
                'filesize': filesize
            }
            
            self.socket.send(json.dumps(request).encode('utf-8'))
            
            # Envia o arquivo em chunks
            with open(file_path, 'rb') as f:
                bytes_sent = 0
                while bytes_sent < filesize:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    self.socket.send(chunk)
                    bytes_sent += len(chunk)
                    
            # Recebe confirmação
            response = self.socket.recv(1024).decode('utf-8')
            response = json.loads(response)
            
            if response.get('status') == 'success':
                self.log("✅ Arquivo enviado com sucesso!")
                messagebox.showinfo("Sucesso", f"Arquivo {filename} enviado com sucesso!")
                self.refresh_files()  # Atualiza lista
            else:
                error_msg = response.get('message', 'Erro desconhecido')
                self.log(f"❌ Erro ao enviar arquivo: {error_msg}")
                messagebox.showerror("Erro", f"Erro ao enviar arquivo: {error_msg}")
                
        except Exception as e:
            self.log(f"❌ Erro ao enviar arquivo: {e}")
            messagebox.showerror("Erro", f"Erro ao enviar arquivo: {e}")
            
    def download_file(self):
        """Baixa um arquivo do servidor"""
        if not self.connected:
            messagebox.showwarning("Aviso", "Conecte-se ao servidor primeiro")
            return
            
        # Verifica se um arquivo foi selecionado
        selection = self.files_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um arquivo para baixar")
            return
            
        # Obtém nome do arquivo selecionado
        item = self.files_tree.item(selection[0])
        filename = item['values'][0]
        
        # Seleciona pasta para salvar
        save_path = filedialog.asksaveasfilename(
            title="Salvar arquivo como",
            initialvalue=filename,
            filetypes=[("Todos os arquivos", "*.*")]
        )
        
        if not save_path:
            return
            
        try:
            self.log(f"📥 Baixando arquivo: {filename}")
            
            # Solicita arquivo
            request = {
                'action': 'download_file',
                'filename': filename
            }
            
            response = self.send_request(request)
            
            if response and response.get('status') == 'success':
                filesize = response['filesize']
                
                # Confirma recebimento
                self.socket.send(b'OK')
                
                # Recebe arquivo em chunks
                with open(save_path, 'wb') as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        chunk = self.socket.recv(min(4096, filesize - bytes_received))
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_received += len(chunk)
                        
                self.log("✅ Arquivo baixado com sucesso!")
                messagebox.showinfo("Sucesso", f"Arquivo salvo em: {save_path}")
                
            else:
                error_msg = response.get('message', 'Erro desconhecido') if response else 'Sem resposta'
                self.log(f"❌ Erro ao baixar arquivo: {error_msg}")
                messagebox.showerror("Erro", f"Erro ao baixar arquivo: {error_msg}")
                
        except Exception as e:
            self.log(f"❌ Erro ao baixar arquivo: {e}")
            messagebox.showerror("Erro", f"Erro ao baixar arquivo: {e}")
            
    def delete_file(self):
        """Deleta um arquivo do servidor"""
        if not self.connected:
            messagebox.showwarning("Aviso", "Conecte-se ao servidor primeiro")
            return
            
        # Verifica se um arquivo foi selecionado
        selection = self.files_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um arquivo para deletar")
            return
            
        # Obtém nome do arquivo selecionado
        item = self.files_tree.item(selection[0])
        filename = item['values'][0]
        
        # Confirma deleção
        if not messagebox.askyesno("Confirmar", f"Deseja realmente deletar o arquivo '{filename}'?"):
            return
            
        try:
            self.log(f"🗑️ Deletando arquivo: {filename}")
            
            # Solicita deleção
            request = {
                'action': 'delete_file',
                'filename': filename
            }
            
            response = self.send_request(request)
            
            if response and response.get('status') == 'success':
                self.log("✅ Arquivo deletado com sucesso!")
                messagebox.showinfo("Sucesso", f"Arquivo {filename} deletado com sucesso!")
                self.refresh_files()  # Atualiza lista
            else:
                error_msg = response.get('message', 'Erro desconhecido') if response else 'Sem resposta'
                self.log(f"❌ Erro ao deletar arquivo: {error_msg}")
                messagebox.showerror("Erro", f"Erro ao deletar arquivo: {error_msg}")
                
        except Exception as e:
            self.log(f"❌ Erro ao deletar arquivo: {e}")
            messagebox.showerror("Erro", f"Erro ao deletar arquivo: {e}")
            
    def on_closing(self):
        """Função chamada quando a janela está sendo fechada"""
        if self.connected:
            self.disconnect_from_server()
        self.root.destroy()

def main():
    """Função principal do cliente"""
    # Cria janela principal
    root = tk.Tk()
    
    # Cria cliente
    client = FileClient(root)
    
    # Configura evento de fechamento
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    
    # Inicia loop da interface
    root.mainloop()

if __name__ == "__main__":
    main()