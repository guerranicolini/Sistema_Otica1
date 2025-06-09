
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class MedicosTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_database()
        self.create_widgets()
        self.load_doctors()

    def setup_database(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                especialidade TEXT,
                crm TEXT UNIQUE,
                telefone TEXT,
                email TEXT,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Cadastro de Médico")
        input_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(input_frame, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nome_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.nome_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Especialidade:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.especialidade_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.especialidade_var, width=25).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="CRM:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.crm_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.crm_var, width=15).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Telefone:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.telefone_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.telefone_var, width=20).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Email:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.email_var, width=40).grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        # Botões
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Adicionar", command=self.add_doctor).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Atualizar", command=self.update_doctor).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_doctor).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_fields).pack(side='left', padx=5)

        # Treeview
        tree_frame = ttk.LabelFrame(main_frame, text="Lista de Médicos")
        tree_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Nome', 'Especialidade', 'CRM', 'Telefone', 'Email')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.on_item_select)

    def add_doctor(self):
        if not self.nome_var.get():
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO medicos (nome, especialidade, crm, telefone, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.nome_var.get(), self.especialidade_var.get(),
                  self.crm_var.get(), self.telefone_var.get(), self.email_var.get()))
            conn.commit()
            messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!")
            self.clear_fields()
            self.load_doctors()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CRM já cadastrado!")
        finally:
            conn.close()

    def update_doctor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um médico para atualizar!")
            return

        doctor_id = self.tree.item(selected[0])['values'][0]
        
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE medicos SET nome=?, especialidade=?, crm=?, telefone=?, email=?
            WHERE id=?
        ''', (self.nome_var.get(), self.especialidade_var.get(),
              self.crm_var.get(), self.telefone_var.get(), 
              self.email_var.get(), doctor_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!")
        self.clear_fields()
        self.load_doctors()

    def delete_doctor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um médico para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este médico?"):
            doctor_id = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM medicos WHERE id=?', (doctor_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Médico excluído com sucesso!")
            self.load_doctors()

    def clear_fields(self):
        self.nome_var.set('')
        self.especialidade_var.set('')
        self.crm_var.set('')
        self.telefone_var.set('')
        self.email_var.set('')

    def on_item_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.nome_var.set(values[1])
            self.especialidade_var.set(values[2])
            self.crm_var.set(values[3])
            self.telefone_var.set(values[4])
            self.email_var.set(values[5])

    def load_doctors(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM medicos ORDER BY nome')
        doctors = cursor.fetchall()
        conn.close()

        for doctor in doctors:
            self.tree.insert('', 'end', values=doctor)
