import os
import subprocess
import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicativo de Abertura de Arquivos")
        self.geometry("1000x500")
        self.configure(bg="#00020F") 

        style = ttk.Style(self)
        style.configure("TButton", font=("Helvetica", 12), padding=10, foreground="#0000C5", background="#000000") 

        frame = tk.Frame(self, bg="#00020F") 
        frame.place(relx=0.5, rely=0.5, anchor="center")

        buttons_data = [
            ("Cadastrar/Consultar Fornecedores", self.abrir_fornecedor),
            ("Fazer Pedidos", self.abrir_main),
            ("Cadastrar Produtos", self.abrir_produtos),
            ("Relatório de Pedidos", self.abrir_relatorio)
        ]

        for text, command in buttons_data:
            button = ttk.Button(frame, text=text, command=command, style="TButton", cursor="hand2") 
            button.pack(pady=10)

    def abrir_fornecedor(self):
        self.abrir_arquivo("fornecedor.py")

    def abrir_produtos(self):
        self.abrir_arquivo("produtos.py")

    def abrir_main(self):
        self.abrir_arquivo("pedidos.py")

    def abrir_relatorio(self):
        self.abrir_arquivo("relatorio.py")

    def abrir_arquivo(self, arquivo):
        try:
            subprocess.Popen(["python", arquivo], cwd=os.path.dirname(os.path.abspath(arquivo)))
        except Exception as e:
            print(f"Erro ao abrir {arquivo}: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
