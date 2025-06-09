
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class ClientesTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_database()
        self.create_widgets()
        self.load_clients()

    def setup_database(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame de entrada de dados
        input_frame = ttk.LabelFrame(main_frame, text="Cadastro de Cliente")
        input_frame.pack(fill='x', pady=(0, 10))

        # Campos de entrada
        ttk.Label(input_frame, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nome_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.nome_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Telefone:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.telefone_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.telefone_var, width=20).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Email:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Endereço:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.endereco_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.endereco_var, width=40).grid(row=1, column=3, columnspan=2, padx=5, pady=5)

        # Botões
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=5, pady=10)

        ttk.Button(button_frame, text="Adicionar", command=self.add_client).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Atualizar", command=self.update_client).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_client).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_fields).pack(side='left', padx=5)

        # Treeview para listagem
        tree_frame = ttk.LabelFrame(main_frame, text="Lista de Clientes")
        tree_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Nome', 'Telefone', 'Email', 'Endereço', 'Data Cadastro')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.on_item_select)

    def add_client(self):
        if not self.nome_var.get():
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, telefone, email, endereco)
            VALUES (?, ?, ?, ?)
        ''', (self.nome_var.get(), self.telefone_var.get(), 
              self.email_var.get(), self.endereco_var.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
        self.clear_fields()
        self.load_clients()

    def update_client(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um cliente para atualizar!")
            return

        client_id = self.tree.item(selected[0])['values'][0]
        
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE clientes SET nome=?, telefone=?, email=?, endereco=?
            WHERE id=?
        ''', (self.nome_var.get(), self.telefone_var.get(),
              self.email_var.get(), self.endereco_var.get(), client_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        self.clear_fields()
        self.load_clients()

    def delete_client(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um cliente para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este cliente?"):
            client_id = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM clientes WHERE id=?', (client_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            self.load_clients()

    def clear_fields(self):
        self.nome_var.set('')
        self.telefone_var.set('')
        self.email_var.set('')
        self.endereco_var.set('')

    def on_item_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.nome_var.set(values[1])
            self.telefone_var.set(values[2])
            self.email_var.set(values[3])
            self.endereco_var.set(values[4])

    def load_clients(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY nome')
        clients = cursor.fetchall()
        conn.close()

        for client in clients:
            self.tree.insert('', 'end', values=client)
