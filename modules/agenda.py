
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date
from tkinter import messagebox
import calendar

class AgendaTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_database()
        self.create_widgets()
        self.load_appointments()

    def setup_database(self):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agenda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                medico_id INTEGER,
                data_hora DATETIME,
                descricao TEXT,
                status TEXT DEFAULT 'Agendado',
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (medico_id) REFERENCES medicos (id)
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Novo Agendamento")
        input_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(input_frame, text="Cliente:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(input_frame, textvariable=self.cliente_var, width=25)
        self.cliente_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Médico:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.medico_var = tk.StringVar()
        self.medico_combo = ttk.Combobox(input_frame, textvariable=self.medico_var, width=25)
        self.medico_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Data:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.data_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.data_var, width=12).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Hora:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.hora_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.hora_var, width=10).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Status:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.status_var = tk.StringVar(value="Agendado")
        status_combo = ttk.Combobox(input_frame, textvariable=self.status_var,
                                   values=["Agendado", "Confirmado", "Realizado", "Cancelado"])
        status_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Descrição:").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.descricao_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.descricao_var, width=40).grid(row=2, column=3, padx=5, pady=5)

        # Labels de exemplo
        ttk.Label(input_frame, text="(dd/mm/aaaa)", font=('Arial', 8)).grid(row=1, column=1, sticky='s')
        ttk.Label(input_frame, text="(hh:mm)", font=('Arial', 8)).grid(row=1, column=3, sticky='s')

        # Botões
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Agendar", command=self.add_appointment).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Atualizar", command=self.update_appointment).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_appointment).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_fields).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Atualizar Listas", command=self.update_combos).pack(side='left', padx=5)

        # Treeview
        tree_frame = ttk.LabelFrame(main_frame, text="Agenda")
        tree_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Cliente', 'Médico', 'Data/Hora', 'Status', 'Descrição')
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

        conn.close()

    def add_appointment(self):
        if not all([self.cliente_var.get(), self.medico_var.get(), self.data_var.get(), self.hora_var.get()]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        try:
            cliente_id = int(self.cliente_var.get().split(' - ')[0])
            medico_id = int(self.medico_var.get().split(' - ')[0])
            
            # Converter data e hora
            data_str = self.data_var.get()
            hora_str = self.hora_var.get()
            data_hora = datetime.strptime(f"{data_str} {hora_str}", "%d/%m/%Y %H:%M")
            
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Formato de data/hora inválido! Use dd/mm/aaaa e hh:mm")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO agenda (cliente_id, medico_id, data_hora, descricao, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (cliente_id, medico_id, data_hora, self.descricao_var.get(), self.status_var.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Agendamento criado com sucesso!")
        self.clear_fields()
        self.load_appointments()

    def update_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um agendamento para atualizar!")
            return

        appointment_id = self.tree.item(selected[0])['values'][0]
        
        try:
            cliente_id = int(self.cliente_var.get().split(' - ')[0])
            medico_id = int(self.medico_var.get().split(' - ')[0])
            data_str = self.data_var.get()
            hora_str = self.hora_var.get()
            data_hora = datetime.strptime(f"{data_str} {hora_str}", "%d/%m/%Y %H:%M")
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Dados inválidos!")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE agenda SET cliente_id=?, medico_id=?, data_hora=?, descricao=?, status=?
            WHERE id=?
        ''', (cliente_id, medico_id, data_hora, self.descricao_var.get(), 
              self.status_var.get(), appointment_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")
        self.clear_fields()
        self.load_appointments()

    def delete_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um agendamento para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este agendamento?"):
            appointment_id = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM agenda WHERE id=?', (appointment_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso!")
            self.load_appointments()

    def clear_fields(self):
        self.cliente_var.set('')
        self.medico_var.set('')
        self.data_var.set('')
        self.hora_var.set('')
        self.descricao_var.set('')
        self.status_var.set('Agendado')

    def on_item_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            try:
                data_hora = datetime.strptime(values[3], "%Y-%m-%d %H:%M:%S")
                self.data_var.set(data_hora.strftime("%d/%m/%Y"))
                self.hora_var.set(data_hora.strftime("%H:%M"))
                self.status_var.set(values[4])
                self.descricao_var.set(values[5])
            except:
                pass

    def load_appointments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

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
            self.tree.insert('', 'end', values=appointment)
