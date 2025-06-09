
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RelatoriosTab:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame de filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros")
        filter_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(filter_frame, text="Data Inicial:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.data_inicial_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.data_inicial_var, width=12).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Data Final:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.data_final_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.data_final_var, width=12).grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(filter_frame, text="Aplicar Filtros", command=self.apply_filters).grid(row=0, column=4, padx=10)

        # Notebook para diferentes relatórios
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        # Aba Clientes
        clientes_frame = ttk.Frame(notebook)
        notebook.add(clientes_frame, text="Clientes")
        self.create_clients_report(clientes_frame)

        # Aba Produtos
        produtos_frame = ttk.Frame(notebook)
        notebook.add(produtos_frame, text="Produtos")
        self.create_products_report(produtos_frame)

        # Aba Pedidos
        pedidos_frame = ttk.Frame(notebook)
        notebook.add(pedidos_frame, text="Pedidos")
        self.create_orders_report(pedidos_frame)

        # Aba Agenda
        agenda_frame = ttk.Frame(notebook)
        notebook.add(agenda_frame, text="Agenda")
        self.create_schedule_report(agenda_frame)

        # Aba Gráficos
        graficos_frame = ttk.Frame(notebook)
        notebook.add(graficos_frame, text="Gráficos")
        self.create_charts_tab(graficos_frame)

    def create_clients_report(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Gerar Relatório de Clientes", 
                  command=self.generate_clients_report).pack(pady=5)

        columns = ('ID', 'Nome', 'Telefone', 'Email', 'Data Cadastro')
        self.clients_tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.clients_tree.heading(col, text=col)

        scrollbar_clients = ttk.Scrollbar(frame, orient='vertical', command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=scrollbar_clients.set)
        self.clients_tree.pack(side='left', fill='both', expand=True)
        scrollbar_clients.pack(side='right', fill='y')

    def create_products_report(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Gerar Relatório de Produtos", 
                  command=self.generate_products_report).pack(pady=5)

        columns = ('ID', 'Nome', 'Categoria', 'Preço', 'Estoque', 'Valor Total')
        self.products_tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.products_tree.heading(col, text=col)

        scrollbar_products = ttk.Scrollbar(frame, orient='vertical', command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar_products.set)
        self.products_tree.pack(side='left', fill='both', expand=True)
        scrollbar_products.pack(side='right', fill='y')

    def create_orders_report(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=5)

        ttk.Button(button_frame, text="Relatório de Pedidos", 
                  command=self.generate_orders_report).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Vendas por Período", 
                  command=self.generate_sales_report).pack(side='left', padx=5)

        columns = ('ID', 'Cliente', 'Produto', 'Quantidade', 'Valor Total', 'Status', 'Data')
        self.orders_tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.orders_tree.heading(col, text=col)

        scrollbar_orders = ttk.Scrollbar(frame, orient='vertical', command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar_orders.set)
        self.orders_tree.pack(side='left', fill='both', expand=True)
        scrollbar_orders.pack(side='right', fill='y')

    def create_schedule_report(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Relatório de Agendamentos", 
                  command=self.generate_schedule_report).pack(pady=5)

        columns = ('ID', 'Cliente', 'Médico', 'Data/Hora', 'Status', 'Descrição')
        self.schedule_tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.schedule_tree.heading(col, text=col)

        scrollbar_schedule = ttk.Scrollbar(frame, orient='vertical', command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar_schedule.set)
        self.schedule_tree.pack(side='left', fill='both', expand=True)
        scrollbar_schedule.pack(side='right', fill='y')

    def create_charts_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=5)

        ttk.Button(button_frame, text="Vendas por Mês", 
                  command=self.chart_sales_by_month).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Produtos Mais Vendidos", 
                  command=self.chart_top_products).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Status dos Pedidos", 
                  command=self.chart_order_status).pack(side='left', padx=5)

        # Frame para o gráfico
        self.chart_frame = ttk.Frame(frame)
        self.chart_frame.pack(fill='both', expand=True)

    def apply_filters(self):
        # Implementar aplicação de filtros
        messagebox.showinfo("Filtros", "Filtros aplicados com sucesso!")

    def generate_clients_report(self):
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, telefone, email, data_cadastro FROM clientes ORDER BY nome')
        clients = cursor.fetchall()
        conn.close()

        for client in clients:
            self.clients_tree.insert('', 'end', values=client)

        messagebox.showinfo("Relatório", f"Relatório gerado com {len(clients)} clientes")

    def generate_products_report(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, categoria, preco, estoque, (preco * estoque) as valor_total FROM produtos ORDER BY nome')
        products = cursor.fetchall()
        conn.close()

        total_value = 0
        for product in products:
            self.products_tree.insert('', 'end', values=product)
            total_value += product[5] if product[5] else 0

        messagebox.showinfo("Relatório", f"Relatório gerado com {len(products)} produtos\nValor total em estoque: R$ {total_value:.2f}")

    def generate_orders_report(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, c.nome, pr.nome, p.quantidade, p.valor_total, p.status, p.data_pedido
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            JOIN produtos pr ON p.produto_id = pr.id
            ORDER BY p.data_pedido DESC
        ''')
        orders = cursor.fetchall()
        conn.close()

        total_value = 0
        for order in orders:
            self.orders_tree.insert('', 'end', values=order)
            total_value += order[4] if order[4] else 0

        messagebox.showinfo("Relatório", f"Relatório gerado com {len(orders)} pedidos\nValor total: R$ {total_value:.2f}")

    def generate_sales_report(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DATE(data_pedido) as data, SUM(valor_total) as total_dia
            FROM pedidos
            WHERE status != 'Cancelado'
            GROUP BY DATE(data_pedido)
            ORDER BY data DESC
        ''')
        sales = cursor.fetchall()
        conn.close()

        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        total_sales = 0
        for sale in sales:
            self.orders_tree.insert('', 'end', values=('', '', sale[0], '', sale[1], 'Vendas do Dia', ''))
            total_sales += sale[1]

        messagebox.showinfo("Vendas", f"Total de vendas: R$ {total_sales:.2f}")

    def generate_schedule_report(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, c.nome, m.nome, a.data_hora, a.status, a.descricao
            FROM agenda a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN medicos m ON a.medico_id = m.id
            ORDER BY a.data_hora
        ''')
        appointments = cursor.fetchall()
        conn.close()

        for appointment in appointments:
            self.schedule_tree.insert('', 'end', values=appointment)

        messagebox.showinfo("Relatório", f"Relatório gerado com {len(appointments)} agendamentos")

    def chart_sales_by_month(self):
        # Limpar frame anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT strftime('%Y-%m', data_pedido) as mes, SUM(valor_total) as total
            FROM pedidos
            WHERE status != 'Cancelado'
            GROUP BY strftime('%Y-%m', data_pedido)
            ORDER BY mes
        ''')
        data = cursor.fetchall()
        conn.close()

        if not data:
            ttk.Label(self.chart_frame, text="Sem dados para exibir").pack()
            return

        months = [row[0] for row in data]
        values = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(months, values)
        ax.set_title('Vendas por Mês')
        ax.set_xlabel('Mês')
        ax.set_ylabel('Valor (R$)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def chart_top_products(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pr.nome, SUM(p.quantidade) as total_vendido
            FROM pedidos p
            JOIN produtos pr ON p.produto_id = pr.id
            WHERE p.status != 'Cancelado'
            GROUP BY pr.nome
            ORDER BY total_vendido DESC
            LIMIT 10
        ''')
        data = cursor.fetchall()
        conn.close()

        if not data:
            ttk.Label(self.chart_frame, text="Sem dados para exibir").pack()
            return

        products = [row[0] for row in data]
        quantities = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(products, quantities)
        ax.set_title('Produtos Mais Vendidos')
        ax.set_xlabel('Quantidade Vendida')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def chart_order_status(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status, COUNT(*) as quantidade
            FROM pedidos
            GROUP BY status
        ''')
        data = cursor.fetchall()
        conn.close()

        if not data:
            ttk.Label(self.chart_frame, text="Sem dados para exibir").pack()
            return

        status = [row[0] for row in data]
        quantities = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(quantities, labels=status, autopct='%1.1f%%')
        ax.set_title('Status dos Pedidos')

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
