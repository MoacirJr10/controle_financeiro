import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from utils.icons import ICONES
from data.database import adicionar_transacao, listar_transacoes, deletar_transacao


class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{ICONES['dinheiro']} Controle Financeiro")
        self.geometry("750x500")
        self.resizable(False, False)
        self.build_interface()
        self.filtrar()

    def build_interface(self):
        """Cria e organiza a interface gráfica da aplicação."""

        # Frame de entrada de dados
        entrada_frame = ttk.LabelFrame(self, text=f"{ICONES['entrada']} Nova Transação")
        entrada_frame.pack(padx=10, pady=10, fill='x')

        self.tipo = ttk.Combobox(entrada_frame, values=["Entrada", "Saída"], width=10, state="readonly")
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

        ttk.Button(entrada_frame, text=f"{ICONES['adicionar']} Adicionar", command=self.adicionar).grid(row=0, column=4, padx=5)

        # Filtro por mês e ano
        filtro_frame = tk.Frame(self)
        filtro_frame.pack(pady=5)

        self.mes = ttk.Entry(filtro_frame, width=5)
        self.mes.insert(0, datetime.today().month)
        self.mes.pack(side=tk.LEFT, padx=5)

        self.ano = ttk.Entry(filtro_frame, width=6)
        self.ano.insert(0, datetime.today().year)
        self.ano.pack(side=tk.LEFT, padx=5)

        ttk.Button(filtro_frame, text=f"{ICONES['filtro']} Filtrar", command=self.filtrar).pack(side=tk.LEFT, padx=5)

        # Tabela de transações
        self.tree = ttk.Treeview(self, columns=("ID", "Tipo", "Categoria", "Valor", "Data"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.column("Categoria", width=180)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<Button-3>", self.menu_contexto)

        # Label de saldo
        self.label_saldo = ttk.Label(self, text=f"{ICONES['dinheiro']} Saldo: R$ 0.00", font=("Arial", 12, "bold"))
        self.label_saldo.pack(pady=5)

    def adicionar(self):
        """Adiciona uma nova transação após validação."""
        tipo = self.tipo.get()
        categoria = self.categoria.get().strip()
        valor_str = self.valor.get().replace(",", ".").strip()
        data = self.data.get().strip()

        if not categoria or categoria.lower() == "categoria":
            messagebox.showwarning("Aviso", "Digite uma categoria válida.")
            return

        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico positivo.")
            return

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use o formato YYYY-MM-DD.")
            return

        if adicionar_transacao(tipo, categoria, valor, data):
            self.limpar_campos()
            self.filtrar()
        else:
            messagebox.showerror("Erro", "Erro ao adicionar a transação.")

    def limpar_campos(self):
        """Limpa os campos de entrada após uma transação bem-sucedida."""
        self.valor.delete(0, tk.END)
        self.valor.insert(0, "Valor")
        self.categoria.delete(0, tk.END)
        self.categoria.insert(0, "Categoria")

    def filtrar(self):
        """Filtra e exibe as transações com base no mês e ano inseridos."""
        self.tree.delete(*self.tree.get_children())

        try:
            mes = int(self.mes.get())
            ano = int(self.ano.get())
        except ValueError:
            messagebox.showerror("Erro", "Mês e Ano devem ser numéricos.")
            return

        transacoes = listar_transacoes(mes, ano)
        saldo = 0.0

        for tr in transacoes:
            self.tree.insert("", tk.END, values=tr)
            saldo += tr[3] if tr[1] == "Entrada" else -tr[3]

        self.label_saldo.config(text=f"{ICONES['dinheiro']} Saldo: R$ {saldo:.2f}")

    def menu_contexto(self, event):
        """Exibe o menu de contexto ao clicar com o botão direito na tabela."""
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label=f"{ICONES['excluir']} Excluir", command=lambda: self.excluir(iid))
            menu.post(event.x_root, event.y_root)

    def excluir(self, iid):
        """Exclui uma transação após confirmação do usuário."""
        item = self.tree.item(iid)
        transacao_id = item["values"][0]
        confirmar = messagebox.askyesno("Confirmar Exclusão", "Deseja excluir esta transação?")
        if confirmar:
            if deletar_transacao(transacao_id):
                self.filtrar()
            else:
                messagebox.showerror("Erro", "Erro ao excluir a transação.")
