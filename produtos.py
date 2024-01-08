import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class AplicacaoCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação Cliente")
        self.root.geometry("1200x700")

        try:
            self.conn = psycopg2.connect(
                dbname="pabd_vespertino",
                user="pabd",
                password="pabd",
                host="178.128.156.229",
                port="5432",
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Falha ao conectar ao banco de dados: {e}")
            root.destroy()
            return

        self.estoque = tk.StringVar()
        self.nome_produto = tk.StringVar()
        self.valor = tk.StringVar()
        self.fornecedor = tk.StringVar()
        self.categoria = tk.StringVar()

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)

        self.root.configure(bg="#f0f0f0")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        self.label_estoque = ttk.Label(main_frame, text="Estoque:", font=("Helvetica", 16))
        self.entry_estoque = ttk.Entry(main_frame, textvariable=self.estoque)

        self.label_nome_produto = ttk.Label(main_frame, text="Nome do Produto:", font=("Helvetica", 16))
        self.entry_nome_produto = ttk.Entry(main_frame, textvariable=self.nome_produto)

        self.label_valor = ttk.Label(main_frame, text="Valor:", font=("Helvetica", 16))
        self.entry_valor = ttk.Entry(main_frame, textvariable=self.valor)

        self.label_fornecedor = ttk.Label(main_frame, text="Fornecedor:", font=("Helvetica", 16))
        self.combo_fornecedor = ttk.Combobox(main_frame, state="readonly", textvariable=self.fornecedor)

        self.label_categoria = ttk.Label(main_frame, text="Categoria:", font=("Helvetica", 16))
        self.combo_categoria = ttk.Combobox(main_frame, state="readonly", textvariable=self.categoria)

        self.button_cadastrar_produto = ttk.Button(main_frame, text="Cadastrar Produto", command=self.cadastrar_produto)

        row_counter = 0

        self.label_estoque.grid(row=row_counter, column=0, pady=(0, 10))
        self.entry_estoque.grid(row=row_counter, column=1, pady=(0, 10))
        row_counter += 1

        self.label_nome_produto.grid(row=row_counter, column=0, pady=(0, 10))
        self.entry_nome_produto.grid(row=row_counter, column=1, pady=(0, 10))
        row_counter += 1

        self.label_valor.grid(row=row_counter, column=0, pady=(0, 10))
        self.entry_valor.grid(row=row_counter, column=1, pady=(0, 10))
        row_counter += 1

        self.label_fornecedor.grid(row=row_counter, column=0, pady=(0, 10))
        self.combo_fornecedor.grid(row=row_counter, column=1, pady=(0, 10))
        row_counter += 1

        self.label_categoria.grid(row=row_counter, column=0, pady=(0, 10))
        self.combo_categoria.grid(row=row_counter, column=1, pady=(0, 10))
        row_counter += 1

        self.button_cadastrar_produto.grid(row=row_counter, column=0, columnspan=2, pady=(10, 0))

        self.obter_opcoes_fornecedor_categoria()

    def obter_opcoes_fornecedor_categoria(self):
        try:
            self.cursor.execute("SELECT nome FROM cps.tbFornecedor")
            fornecedores = self.cursor.fetchall()
            self.combo_fornecedor["values"] = [fornecedor[0] for fornecedor in fornecedores]

            self.cursor.execute("SELECT nome FROM cps.tbCategoria")
            categorias = self.cursor.fetchall()
            self.combo_categoria["values"] = [categoria[0] for categoria in categorias]
        except Exception as e:
            messagebox.showerror("Erro ao Obter Opções", f"Falha ao obter opções: {e}")

    def cadastrar_produto(self):
        estoque = self.estoque.get()
        nome_produto = self.nome_produto.get()
        valor = self.valor.get()
        nome_fornecedor = self.fornecedor.get()

        if not estoque or not nome_produto or not valor or not nome_fornecedor or not self.categoria.get():
            messagebox.showerror("Campos Incompletos", "Por favor, preencha todos os campos para cadastrar o novo produto.")
            return

        try:
            self.cursor.execute("SELECT id_fornecedor FROM cps.tbFornecedor WHERE nome = %s", (nome_fornecedor,))
            result = self.cursor.fetchone()

            if result:
                id_fornecedor = result[0]
            else:
                messagebox.showerror("Fornecedor Não Encontrado", "Fornecedor não encontrado. Selecione um fornecedor existente.")
                return

            self.cursor.execute("SELECT id_categoria FROM cps.tbCategoria WHERE nome = %s", (self.categoria.get(),))
            result_categoria = self.cursor.fetchone()

            if result_categoria:
                id_categoria = result_categoria[0]
            else:
                messagebox.showerror("Categoria Não Encontrada", "Categoria não encontrada. Selecione uma categoria existente.")
                return

            self.cursor.execute("INSERT INTO cps.tbProdutos (estoque, nome, valor, id_fornecedor, id_categoria) VALUES (%s, %s, %s, %s, %s);",
                                (estoque, nome_produto, valor, id_fornecedor, id_categoria))
            self.conn.commit()
            messagebox.showinfo("Produto Cadastrado", "Produto cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao Cadastrar Produto", f"Falha ao cadastrar produto: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoCliente(root)
    root.mainloop()
