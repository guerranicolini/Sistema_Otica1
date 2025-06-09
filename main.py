import tkinter as tk
from tkinter import ttk
from modules import clientes, medicos, produtos, pedidos, agenda, relatorios

class Layout:
    def __init__(self, root):
        self.root = root
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        tabs = {
            'Clientes': clientes.ClientesTab,
            'Médicos': medicos.MedicosTab,
            'Produtos': produtos.ProdutosTab,
            'Pedidos': pedidos.PedidosTab,
            'Agenda': agenda.AgendaTab,
            'Relatórios': relatorios.RelatoriosTab
        }

        for name, tab_class in tabs.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=name)
            tab_class(frame)