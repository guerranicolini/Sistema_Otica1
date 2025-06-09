
import tkinter as tk
from tkinter import ttk
from modules import clientes, medicos, produtos, pedidos, agenda, relatorios

class SistemaGestao:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestão Médica")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Maximizar janela no Windows
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_layout()

    def create_layout(self):
        # Menu principal
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
        
        # Notebook principal
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Definir as abas
        tabs = {
            'Clientes': clientes.ClientesTab,
            'Médicos': medicos.MedicosTab,
            'Produtos': produtos.ProdutosTab,
            'Pedidos': pedidos.PedidosTab,
            'Agenda': agenda.AgendaTab,
            'Relatórios': relatorios.RelatoriosTab
        }

        # Criar as abas
        for name, tab_class in tabs.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=name)
            tab_class(frame)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre")
        about_window.geometry("400x200")
        about_window.resizable(False, False)
        
        tk.Label(about_window, text="Sistema de Gestão Médica", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        tk.Label(about_window, text="Versão 1.0").pack()
        tk.Label(about_window, text="Sistema completo para gestão médica").pack(pady=10)
        tk.Button(about_window, text="Fechar", 
                 command=about_window.destroy).pack(pady=20)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SistemaGestao()
    app.run()
