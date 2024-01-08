import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class RelatorioPedidos(tk.Toplevel):
    def __init__(self, root, conn):
        super().__init__(root)
        self.title("Relatório de Pedidos")
        self.geometry("1000x500")
        self.configure(bg="#f0f0f0")

        self.conn = conn
        self.cursor = self.conn.cursor()

        columns = ("Pedido ID", "Supermercado", "Fornecedor", "Produto", "Quantidade")
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Helvetica", 14), background="#4CAF50", foreground="black")
        estilo.configure("Treeview", font=("Helvetica", 12))

        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(expand=True, fill="both", pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.carregar_dados()

    def carregar_dados(self):
        try:
            self.cursor.execute("""
                SELECT
                    p.id_pedido as pedido_id,
                    s.nome as supermercado,
                    f.nome as fornecedor,
                    pr.nome as produto,
                    p.quantidade as quantidade
                FROM
                    cps.tbSupermercado s
                    JOIN cps.tbPedidos p ON s.id_supermercado = p.id_supermercado
                    JOIN cps.tbProdutosPedido pp ON p.id_pedido = pp.id_pedido
                    JOIN cps.tbProdutos pr ON pp.id_produto = pr.id_produto
                    JOIN cps.tbFornecedor f ON pr.id_fornecedor = f.id_fornecedor;
            """)

            rows = self.cursor.fetchall()

            for row in rows:
                if None in row:
                    messagebox.showwarning("Dados Inconsistentes", "Os dados carregados estão inconsistentes. Verifique a integridade dos dados no banco de dados.")
                    break

                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Erro ao Carregar Dados", f"Falha ao carregar dados: {e}")

def exibir_relatorio():
    try:
        conn = psycopg2.connect(
            dbname="pabd_vespertino",
            user="pabd",
            password="pabd",
            host="178.128.156.229",
            port="5432",
        )

        root = tk.Tk()
        root.configure(bg="#f0f0f0")
        relatorio = RelatorioPedidos(root, conn)
        root.mainloop()

        conn.close()

    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Falha ao conectar ao banco de dados: {e}")

if __name__ == "__main__":
    exibir_relatorio()
