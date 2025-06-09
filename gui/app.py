import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from data.database import adicionar_transacao, listar_transacoes, deletar_transacao

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controle Financeiro")
        self.geometry("750x500")
        self.resizable(False, False)
        self.build_interface()
        self.filtrar()

    def build_interface(self):
        # Entrada de dados
        entrada_frame = tk.LabelFrame(self, text="Nova Transação")
        entrada_frame.pack(padx=10, pady=10, fill='x')

        self.tipo = ttk.Combobox(entrada_frame, values=["Entrada", "Saída"], width=10)
        self.tipo.set("Entrada")
        self.tipo.grid(row=0, column=0, padx=5, pady=5)

        self.categoria = ttk.Entry(entrada_frame, width=25)
        self.categoria.insert(0, "Categoria")
        self.categoria.grid(row=0, column=1, padx=5)

        self.valor = ttk.Entry(entrada_frame, width=10)
        self.valor.insert(0, "Valor")
        self.valor.grid(row=0, column=2, padx=5)

        self.data = ttk.Entry(entrada_frame, width=12)
        self.data.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.data.grid(row=0, column=3, padx=5)

        ttk.Button(entrada_frame, text="Adicionar", command=self.adicionar).grid(row=0, column=4, padx=5)

        # Filtros
        filtro_frame = tk.Frame(self)
        filtro_frame.pack(pady=5)

        self.mes = ttk.Entry(filtro_frame, width=5)
        self.mes.insert(0, datetime.today().month)
        self.mes.pack(side=tk.LEFT, padx=5)

        self.ano = ttk.Entry(filtro_frame, width=6)
        self.ano.insert(0, datetime.today().year)
        self.ano.pack(side=tk.LEFT, padx=5)

        ttk.Button(filtro_frame, text="Filtrar", command=self.filtrar).pack(side=tk.LEFT, padx=5)

        # Tabela de transações
        self.tree = ttk.Treeview(self, columns=("ID", "Tipo", "Categoria", "Valor", "Data"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<Button-3>", self.menu_contexto)

        # Saldo
        self.label_saldo = ttk.Label(self, text="Saldo: R$ 0.00", font=("Arial", 12, "bold"))
        self.label_saldo.pack(pady=5)

    def adicionar(self):
        try:
            valor = float(self.valor.get())
            adicionar_transacao(self.tipo.get(), self.categoria.get(), valor, self.data.get())
            self.filtrar()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")

    def filtrar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        transacoes = listar_transacoes(self.mes.get(), self.ano.get())
        saldo = 0
        for tr in transacoes:
            self.tree.insert("", tk.END, values=tr)
            if tr[1] == "Entrada":
                saldo += tr[3]
            else:
                saldo -= tr[3]
        self.label_saldo.config(text=f"Saldo: R$ {saldo:.2f}")

    def menu_contexto(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Excluir", command=lambda: self.excluir(iid))
            menu.post(event.x_root, event.y_root)

    def excluir(self, iid):
        item = self.tree.item(iid)
        transacao_id = item['values'][0]
        deletar_transacao(transacao_id)
        self.filtrar()