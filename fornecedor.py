import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class CadastroFornecedor(tk.Toplevel):
    def __init__(self, root, conn):
        super().__init__(root)
        self.title("Cadastro de Fornecedor")
        self.geometry("1000x500")
        self.configure(bg="#00020F")  # Fundo azul escuro

        self.conn = conn
        self.cursor = self.conn.cursor()

        self.nome_fornecedor = tk.StringVar()
        self.contato_fornecedor = tk.StringVar()

        self.label_nome = ttk.Label(self, text="Nome do Fornecedor:", background="#00020F", foreground="#87CEEB")  # Background e foreground ajustados
        self.entry_nome = ttk.Entry(self, textvariable=self.nome_fornecedor, style="TEntry")

        self.label_contato = ttk.Label(self, text="Contato do Fornecedor:", background="#00020F", foreground="#87CEEB")  # Background e foreground ajustados
        self.entry_contato = ttk.Entry(self, textvariable=self.contato_fornecedor, style="TEntry")

        self.button_cadastrar = ttk.Button(self, text="Cadastrar", command=self.cadastrar_fornecedor, style="TButton")

        self.label_nome.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_contato.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_contato.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.button_cadastrar.grid(row=2, column=0, columnspan=2, pady=10)

    def cadastrar_fornecedor(self):
        nome = self.nome_fornecedor.get()
        contato = self.contato_fornecedor.get()

        if not nome or not contato:
            messagebox.showerror("Campos Incompletos", "Por favor, preencha todos os campos.")
            return

        try:
            self.cursor.execute("INSERT INTO cps.tbFornecedor (nome, contato) VALUES (%s, %s) RETURNING id_fornecedor;", (nome, contato))
            fornecedor_id = self.cursor.fetchone()[0]
            messagebox.showinfo("Fornecedor Cadastrado", f"Fornecedor '{nome}' cadastrado com sucesso! (ID: {fornecedor_id})")
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Erro ao Cadastrar Fornecedor", f"Falha ao cadastrar fornecedor: {e}")

class PesquisaFornecedor(tk.Toplevel):
    def __init__(self, root, conn):
        super().__init__(root)
        self.title("Pesquisa de Fornecedor")
        self.geometry("1000x500")
        self.configure(bg="#00020F")  

        self.conn = conn
        self.cursor = self.conn.cursor()

        self.nome_produto_pesquisa = tk.StringVar()

        self.label_nome_produto = ttk.Label(self, text="Nome do Produto:", background="#00020F", foreground="#87CEEB")  # Background e foreground ajustados
        self.entry_nome_produto = ttk.Entry(self, textvariable=self.nome_produto_pesquisa, style="TEntry")

        self.button_pesquisar = ttk.Button(self, text="Pesquisar", command=self.pesquisar_fornecedor, style="TButton")

        self.label_nome_produto.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nome_produto.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.button_pesquisar.grid(row=1, column=0, columnspan=2, pady=10)

    def pesquisar_fornecedor(self):
        nome_produto = self.nome_produto_pesquisa.get()

        if not nome_produto:
            messagebox.showerror("Campo Incompleto", "Por favor, preencha o campo de nome do produto.")
            return

        try:
            self.cursor.execute("""
                SELECT f.nome
                FROM cps.tbFornecedor f
                JOIN cps.tbProdutos p ON f.id_fornecedor = p.id_fornecedor
                WHERE p.nome = %s;
            """, (nome_produto,))
            fornecedores = self.cursor.fetchall()

            if not fornecedores:
                messagebox.showinfo("Resultado da Pesquisa", f"Nenhum fornecedor encontrado para o produto '{nome_produto}'.")
            else:
                nomes_fornecedores = ", ".join([f[0] for f in fornecedores])
                messagebox.showinfo("Resultado da Pesquisa", f"Fornecedores para o produto '{nome_produto}': {nomes_fornecedores}")
        except Exception as e:
            messagebox.showerror("Erro na Pesquisa", f"Falha ao pesquisar fornecedor: {e}")

def main():
    try:
        conn = psycopg2.connect(
            dbname="pabd_vespertino",
            user="pabd",
            password="pabd",
            host="178.128.156.229",
            port="5432",
        )

        root = tk.Tk()
        root.title("Sistema de Gerenciamento de Fornecedores")
        root.geometry("1000x500")
        root.configure(bg="#00020F")  

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10, foreground="#0000C5", background="#000000")  
        style.configure("TEntry", font=("Helvetica", 12), padding=6, foreground="#0000C5", background="#000000") 

        button_cadastro = ttk.Button(root, text="Cadastrar Fornecedor", command=lambda: CadastroFornecedor(root, conn), style="TButton")
        button_pesquisa = ttk.Button(root, text="Pesquisar Fornecedor por Produto", command=lambda: PesquisaFornecedor(root, conn), style="TButton")

        button_cadastro.pack(pady=10)
        button_pesquisa.pack(pady=10)

        root.mainloop()

        conn.close()

    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Falha ao conectar ao banco de dados: {e}")

if __name__ == "__main__":
    main()
