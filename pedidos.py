import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class AplicacaoCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação Cliente")
        self.root.geometry("1200x1000")

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

        self.novo_supermercado_nome = tk.StringVar()
        self.novo_supermercado_contato = tk.StringVar()
        self.novo_supermercado_endereco = tk.StringVar()
        self.escolha_supermercado = tk.StringVar()
        self.escolha_supermercado.set("existente")
        self.id_supermercado = None

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=15)

        self.root.configure(bg="#f0f0f0")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        self.label_escolha_supermercado = ttk.Label(main_frame, text="Escolha uma opção:", font=("Helvetica", 16))
        self.radio_existente = ttk.Radiobutton(main_frame, text="Supermercado Existente", variable=self.escolha_supermercado, value="existente", command=self.atualizar_combobox_supermercados)
        self.radio_novo = ttk.Radiobutton(main_frame, text="Novo Supermercado", variable=self.escolha_supermercado, value="novo", command=self.habilitar_entradas_novo_supermercado)

        self.label_supermercado = ttk.Label(main_frame, text="Selecione o Supermercado:", font=("Helvetica", 16))
        self.combo_supermercado = ttk.Combobox(main_frame, state="readonly", font=("Helvetica", 14))

        self.label_categoria = ttk.Label(main_frame, text="Selecione a Categoria:", font=("Helvetica", 16))
        self.combo_categoria = ttk.Combobox(main_frame, values=self.obter_categorias(), font=("Helvetica", 14))
        self.combo_categoria.bind("<<ComboboxSelected>>", self.carregar_produtos_por_categoria)

        self.label_produto = ttk.Label(main_frame, text="Selecione o Produto:", font=("Helvetica", 16))
        self.combo_produto = ttk.Combobox(main_frame, state="readonly", font=("Helvetica", 14))

        self.label_quantidade = ttk.Label(main_frame, text="Quantidade:", font=("Helvetica", 16))
        self.entry_quantidade = ttk.Entry(main_frame, font=("Helvetica", 14))

        self.label_nome_novo_supermercado = ttk.Label(main_frame, text="Nome do Supermercado:", font=("Helvetica", 16))
        self.entry_nome_novo_supermercado = ttk.Entry(main_frame, textvariable=self.novo_supermercado_nome, state="disabled", font=("Helvetica", 14))

        self.label_contato_novo_supermercado = ttk.Label(main_frame, text="Contato do Supermercado:", font=("Helvetica", 16))
        self.entry_contato_novo_supermercado = ttk.Entry(main_frame, textvariable=self.novo_supermercado_contato, state="disabled", font=("Helvetica", 14))

        self.label_endereco_novo_supermercado = ttk.Label(main_frame, text="Endereço do Supermercado:", font=("Helvetica", 16))
        self.entry_endereco_novo_supermercado = ttk.Entry(main_frame, textvariable=self.novo_supermercado_endereco, state="disabled", font=("Helvetica", 14))

        self.button_enviar_pedido = ttk.Button(main_frame, text="Enviar Pedido", command=self.enviar_pedido)
        self.button_cadastrar_supermercado = ttk.Button(main_frame, text="Cadastrar Supermercado", command=self.cadastrar_supermercado)
        self.button_atualizar_supermercados = ttk.Button(main_frame, text="Atualizar Supermercados", command=self.atualizar_combobox_supermercados)

        row_counter = 0

        self.label_escolha_supermercado.grid(row=row_counter, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.radio_existente.grid(row=row_counter, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.radio_novo.grid(row=row_counter, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.label_supermercado.grid(row=row_counter, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.combo_supermercado.grid(row=row_counter, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.label_categoria.grid(row=row_counter, column=0, pady=(0, 20), sticky="nsew")
        self.combo_categoria.grid(row=row_counter, column=1, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.label_produto.grid(row=row_counter, column=0, pady=(0, 20), sticky="nsew")
        self.combo_produto.grid(row=row_counter, column=1, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.label_quantidade.grid(row=row_counter, column=0, pady=(0, 20), sticky="nsew")
        self.entry_quantidade.grid(row=row_counter, column=1, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.label_nome_novo_supermercado.grid(row=row_counter, column=0, pady=(0, 20), sticky="nsew")
        self.entry_nome_novo_supermercado.grid(row=row_counter, column=1, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.label_contato_novo_supermercado.grid(row=row_counter, column=0, pady=(0, 20), sticky="nsew")
        self.entry_contato_novo_supermercado.grid(row=row_counter, column=1, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.label_endereco_novo_supermercado.grid(row=row_counter, column=0, pady=(0, 20), sticky="nsew")
        self.entry_endereco_novo_supermercado.grid(row=row_counter, column=1, pady=(0, 20), sticky="nsew")
        row_counter += 1

        self.button_enviar_pedido.grid(row=row_counter, column=0, columnspan=2, pady=(20, 0), sticky="nsew")
        row_counter += 1

        self.button_atualizar_supermercados.grid(row=row_counter, column=0, columnspan=2, pady=(20, 0), sticky="nsew")
        row_counter += 1

        self.atualizar_combobox_supermercados()
        self.button_cadastrar_supermercado.grid(row=row_counter, column=0, columnspan=2, pady=(20, 0), sticky="nsew")

        
        for r in range(row_counter + 1):
            main_frame.grid_rowconfigure(r, weight=1)
            main_frame.grid_columnconfigure(0, weight=1)
            main_frame.grid_columnconfigure(1, weight=1)

    def obter_categorias(self):
        try:
            self.cursor.execute("SELECT nome FROM cps.tbCategoria")
            categorias = self.cursor.fetchall()
            return categorias
        except Exception as e:
            messagebox.showerror("Erro ao Obter Categorias", f"Falha ao obter categorias: {e}")
            return []

    def carregar_produtos_por_categoria(self, event):
        categoria_selecionada = self.combo_categoria.get()

        if not categoria_selecionada:
            return

        try:
            self.cursor.execute("SELECT nome FROM cps.tbProdutos WHERE id_categoria = (SELECT id_categoria FROM cps.tbCategoria WHERE nome = %s)", (categoria_selecionada,))
            produtos = self.cursor.fetchall()
            self.combo_produto["values"] = produtos
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Produtos", f"Falha ao carregar produtos: {e}")

    def atualizar_combobox_supermercados(self):
        if self.escolha_supermercado.get() == "existente":
            try:
                self.cursor.execute("SELECT nome FROM cps.tbSupermercado")
                supermercados = self.cursor.fetchall()
                self.combo_supermercado["values"] = supermercados
                self.combo_supermercado["state"] = "readonly"
            except Exception as e:
                messagebox.showerror("Erro ao Carregar Supermercados", f"Falha ao carregar supermercados: {e}")
        else:
            self.combo_supermercado.set("")
            self.combo_supermercado["state"] = "disabled"

    def habilitar_entradas_novo_supermercado(self):
        if self.escolha_supermercado.get() == "novo":
            self.entry_nome_novo_supermercado["state"] = "normal"
            self.entry_contato_novo_supermercado["state"] = "normal"
            self.entry_endereco_novo_supermercado["state"] = "normal"
        else:
            self.entry_nome_novo_supermercado["state"] = "disabled"
            self.entry_contato_novo_supermercado["state"] = "disabled"
            self.entry_endereco_novo_supermercado["state"] = "disabled"

    def cadastrar_supermercado(self):
        nome = self.novo_supermercado_nome.get()
        contato = self.novo_supermercado_contato.get()
        endereco = self.novo_supermercado_endereco.get()

        if not nome or not contato or not endereco:
            messagebox.showerror("Campos Incompletos", "Por favor, preencha todos os campos para cadastrar o novo supermercado.")
            return

        try:
            self.cursor.execute("INSERT INTO cps.tbSupermercado (nome, contato, endereco) VALUES (%s, %s, %s) RETURNING id_supermercado;",
                                (nome, contato, endereco))
            self.id_supermercado = self.cursor.fetchone()[0]
            messagebox.showinfo("Supermercado Cadastrado", f"Supermercado '{nome}' cadastrado com sucesso! (ID: {self.id_supermercado})")

            self.atualizar_combobox_supermercados()

        except Exception as e:
            messagebox.showerror("Erro ao Cadastrar Supermercado", f"Falha ao cadastrar supermercado: {e}")

    def enviar_pedido(self):
        try:
            if self.escolha_supermercado.get() == "existente":
                supermercado = self.combo_supermercado.get()
                self.cursor.execute("SELECT id_supermercado FROM cps.tbSupermercado WHERE nome = %s", (supermercado,))
                result = self.cursor.fetchone()

                if result:
                    self.id_supermercado = result[0]
                else:
                    messagebox.showerror("Supermercado Não Encontrado", "Supermercado não encontrado. Selecione um supermercado existente.")
                    return
            else:
                supermercado = self.entry_nome_novo_supermercado.get()

                if not supermercado or not self.novo_supermercado_contato.get() or not self.novo_supermercado_endereco.get():
                    messagebox.showerror("Campos Incompletos", "Por favor, preencha todos os campos para o novo supermercado.")
                    return

                self.cursor.execute("SELECT id_supermercado FROM cps.tbSupermercado WHERE nome = %s", (supermercado,))
                result = self.cursor.fetchone()

                if result:
                    self.id_supermercado = result[0]
                else:
                    self.cursor.execute("INSERT INTO cps.tbSupermercado (nome, contato, endereco) VALUES (%s, %s, %s) RETURNING id_supermercado;",
                                        (supermercado, self.novo_supermercado_contato.get(), self.novo_supermercado_endereco.get()))
                    self.id_supermercado = self.cursor.fetchone()[0]

            produto = self.combo_produto.get()
            quantidade = self.entry_quantidade.get()

            if not produto or not quantidade:
                messagebox.showerror("Campos Incompletos", "Por favor, preencha todos os campos.")
                return

            self.cursor.execute("INSERT INTO cps.tbPedidos (quantidade, id_supermercado) VALUES (%s, %s) RETURNING id_pedido;",
                                (quantidade, self.id_supermercado))
            pedido_id = self.cursor.fetchone()[0]

            self.cursor.execute("INSERT INTO cps.tbProdutosPedido (id_produto, id_pedido) VALUES ((SELECT id_produto FROM cps.tbProdutos WHERE nome = %s), %s);", (produto, pedido_id))

            self.conn.commit()

            messagebox.showinfo("Pedido Enviado", "Pedido enviado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao Enviar Pedido", f"Falha ao enviar pedido: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoCliente(root)
    root.mainloop()
