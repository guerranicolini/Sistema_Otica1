
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ProdutosTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_database()
        self.create_widgets()
        self.load_products()

    def setup_database(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                categoria TEXT,
                preco REAL,
                estoque INTEGER DEFAULT 0,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Cadastro de Produto")
        input_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(input_frame, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nome_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.nome_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Categoria:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.categoria_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.categoria_var, width=20).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Preço:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.preco_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.preco_var, width=15).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Estoque:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.estoque_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.estoque_var, width=10).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Descrição:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.descricao_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.descricao_var, width=60).grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        # Botões
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Adicionar", command=self.add_product).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Atualizar", command=self.update_product).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_product).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_fields).pack(side='left', padx=5)

        # Treeview
        tree_frame = ttk.LabelFrame(main_frame, text="Lista de Produtos")
        tree_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Nome', 'Categoria', 'Preço', 'Estoque', 'Descrição')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.on_item_select)

    def add_product(self):
        if not self.nome_var.get():
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return

        try:
            preco = float(self.preco_var.get() or 0)
            estoque = int(self.estoque_var.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos!")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, categoria, preco, estoque)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.nome_var.get(), self.descricao_var.get(),
              self.categoria_var.get(), preco, estoque))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        self.clear_fields()
        self.load_products()

    def update_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um produto para atualizar!")
            return

        try:
            preco = float(self.preco_var.get() or 0)
            estoque = int(self.estoque_var.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos!")
            return

        product_id = self.tree.item(selected[0])['values'][0]
        
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produtos SET nome=?, descricao=?, categoria=?, preco=?, estoque=?
            WHERE id=?
        ''', (self.nome_var.get(), self.descricao_var.get(),
              self.categoria_var.get(), preco, estoque, product_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        self.clear_fields()
        self.load_products()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um produto para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este produto?"):
            product_id = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM produtos WHERE id=?', (product_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            self.load_products()

    def clear_fields(self):
        self.nome_var.set('')
        self.descricao_var.set('')
        self.categoria_var.set('')
        self.preco_var.set('')
        self.estoque_var.set('')

    def on_item_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.nome_var.set(values[1])
            self.categoria_var.set(values[2])
            self.preco_var.set(values[3])
            self.estoque_var.set(values[4])
            self.descricao_var.set(values[5])

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos ORDER BY nome')
        products = cursor.fetchall()
        conn.close()

        for product in products:
            self.tree.insert('', 'end', values=product)
