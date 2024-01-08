import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class AplicativoEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

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

        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Helvetica", 14))
        estilo.configure("Treeview", font=("Helvetica", 12))

        frame_principal = tk.Frame(root, bg="#f0f0f0")
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

        self.treeview_estoque = ttk.Treeview(frame_principal, columns=("Quantidade", "Nome do Produto", "ID do Fornecedor"), show="headings", selectmode="browse")

        self.treeview_estoque.heading("Quantidade", text="Quantidade")
        self.treeview_estoque.heading("Nome do Produto", text="Nome do Produto")
        self.treeview_estoque.heading("ID do Fornecedor", text="ID do Fornecedor")

        self.treeview_estoque.column("Quantidade", width=100)
        self.treeview_estoque.column("Nome do Produto", width=300)
        self.treeview_estoque.column("ID do Fornecedor", width=300)

        self.treeview_estoque.pack(expand=True, fill="both")

        self.carregar_estoque()

    def carregar_estoque(self):
        try:
            query = """
                SELECT estoque, nome, 
                    (SELECT nome FROM cps.tbFornecedor WHERE id_fornecedor = tbProdutos.id_fornecedor) as nome_fornecedor
                FROM cps.tbProdutos
            """
            self.cursor.execute(query)
            produtos = self.cursor.fetchall()

            for produto in produtos:
                produto_with_nome_fornecedor = produto[:2] + (produto[2],)
                self.treeview_estoque.insert("", "end", values=produto_with_nome_fornecedor)
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Estoque", f"Falha ao carregar estoque: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoEstoque(root)
    root.mainloop()
