
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class PedidosTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_database()
        self.create_widgets()
        self.load_orders()

    def setup_database(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                medico_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER,
                valor_total REAL,
                status TEXT DEFAULT 'Pendente',
                data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (medico_id) REFERENCES medicos (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Novo Pedido")
        input_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(input_frame, text="Cliente:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(input_frame, textvariable=self.cliente_var, width=25)
        self.cliente_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Médico:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.medico_var = tk.StringVar()
        self.medico_combo = ttk.Combobox(input_frame, textvariable=self.medico_var, width=25)
        self.medico_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Produto:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.produto_var = tk.StringVar()
        self.produto_combo = ttk.Combobox(input_frame, textvariable=self.produto_var, width=25)
        self.produto_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Quantidade:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.quantidade_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.quantidade_var, width=10).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Status:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.status_var = tk.StringVar(value="Pendente")
        status_combo = ttk.Combobox(input_frame, textvariable=self.status_var, 
                                   values=["Pendente", "Processando", "Concluído", "Cancelado"])
        status_combo.grid(row=2, column=1, padx=5, pady=5)

        # Botões
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Adicionar", command=self.add_order).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Atualizar", command=self.update_order).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_order).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_fields).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Atualizar Listas", command=self.update_combos).pack(side='left', padx=5)

        # Treeview
        tree_frame = ttk.LabelFrame(main_frame, text="Lista de Pedidos")
        tree_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Cliente', 'Médico', 'Produto', 'Quantidade', 'Valor Total', 'Status', 'Data')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.on_item_select)
        self.update_combos()

    def update_combos(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        # Clientes
        cursor.execute('SELECT id, nome FROM clientes ORDER BY nome')
        clientes = cursor.fetchall()
        self.cliente_combo['values'] = [f"{c[0]} - {c[1]}" for c in clientes]

        # Médicos
        cursor.execute('SELECT id, nome FROM medicos ORDER BY nome')
        medicos = cursor.fetchall()
        self.medico_combo['values'] = [f"{m[0]} - {m[1]}" for m in medicos]

        # Produtos
        cursor.execute('SELECT id, nome, preco FROM produtos ORDER BY nome')
        produtos = cursor.fetchall()
        self.produto_combo['values'] = [f"{p[0]} - {p[1]} (R$ {p[2]:.2f})" for p in produtos]

        conn.close()

    def add_order(self):
        if not all([self.cliente_var.get(), self.produto_var.get(), self.quantidade_var.get()]):
            messagebox.showerror("Erro", "Cliente, produto e quantidade são obrigatórios!")
            return

        try:
            cliente_id = int(self.cliente_var.get().split(' - ')[0])
            produto_id = int(self.produto_var.get().split(' - ')[0])
            medico_id = int(self.medico_var.get().split(' - ')[0]) if self.medico_var.get() else None
            quantidade = int(self.quantidade_var.get())
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Dados inválidos!")
            return

        # Calcular valor total
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('SELECT preco FROM produtos WHERE id=?', (produto_id,))
        preco = cursor.fetchone()[0]
        valor_total = preco * quantidade

        cursor.execute('''
            INSERT INTO pedidos (cliente_id, medico_id, produto_id, quantidade, valor_total, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cliente_id, medico_id, produto_id, quantidade, valor_total, self.status_var.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Pedido adicionado com sucesso!")
        self.clear_fields()
        self.load_orders()

    def update_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um pedido para atualizar!")
            return

        order_id = self.tree.item(selected[0])['values'][0]
        
        try:
            cliente_id = int(self.cliente_var.get().split(' - ')[0])
            produto_id = int(self.produto_var.get().split(' - ')[0])
            medico_id = int(self.medico_var.get().split(' - ')[0]) if self.medico_var.get() else None
            quantidade = int(self.quantidade_var.get())
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Dados inválidos!")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('SELECT preco FROM produtos WHERE id=?', (produto_id,))
        preco = cursor.fetchone()[0]
        valor_total = preco * quantidade

        cursor.execute('''
            UPDATE pedidos SET cliente_id=?, medico_id=?, produto_id=?, 
            quantidade=?, valor_total=?, status=? WHERE id=?
        ''', (cliente_id, medico_id, produto_id, quantidade, 
              valor_total, self.status_var.get(), order_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Pedido atualizado com sucesso!")
        self.clear_fields()
        self.load_orders()

    def delete_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um pedido para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este pedido?"):
            order_id = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM pedidos WHERE id=?', (order_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Pedido excluído com sucesso!")
            self.load_orders()

    def clear_fields(self):
        self.cliente_var.set('')
        self.medico_var.set('')
        self.produto_var.set('')
        self.quantidade_var.set('')
        self.status_var.set('Pendente')

    def on_item_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            # Implementar seleção dos valores nos combos seria mais complexo
            # Por simplicidade, deixamos apenas a quantidade e status
            self.quantidade_var.set(values[4])
            self.status_var.set(values[6])

    def load_orders(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, c.nome, m.nome, pr.nome, p.quantidade, 
                   p.valor_total, p.status, p.data_pedido
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN medicos m ON p.medico_id = m.id
            JOIN produtos pr ON p.produto_id = pr.id
            ORDER BY p.data_pedido DESC
        ''')
        orders = cursor.fetchall()
        conn.close()

        for order in orders:
            self.tree.insert('', 'end', values=order)
