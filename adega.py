import tkinter as tk
from tkinter import ttk
import json
import os
import tkinter.messagebox as messagebox


class AdegaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Fiado - Adega")
        self.root.geometry("900x500")
        self.root.config(bg="#f4f4f4")

        # Dados
        self.clientes = {}

        # Frames
        self.frame_principal = tk.Frame(root, bg="#f4f4f4")
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        self.frame_cadastro = tk.LabelFrame(self.frame_principal, text="Cadastro de Clientes", padx=10, pady=10, bg="#f4f4f4", font=("Arial", 12, "bold"))
        self.frame_cadastro.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_fiado = tk.LabelFrame(self.frame_principal, text="Registro de Fiados", padx=10, pady=10, bg="#f4f4f4", font=("Arial", 12, "bold"))
        self.frame_fiado.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.frame_pagamento = tk.LabelFrame(self.frame_principal, text="Controle de Pagamentos", padx=10, pady=10, bg="#f4f4f4", font=("Arial", 12, "bold"))
        self.frame_pagamento.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Cadastro de clientes
        tk.Label(self.frame_cadastro, text="Nome do Cliente:", bg="#f4f4f4").grid(row=0, column=0, pady=5)
        self.entry_cliente = tk.Entry(self.frame_cadastro, width=25)
        self.entry_cliente.grid(row=1, column=0, pady=5)

        self.btn_adicionar_cliente = tk.Button(self.frame_cadastro, text="Adicionar Cliente", command=self.adicionar_cliente, bg="#28a745", fg="white", font=("Arial", 10, "bold"))
        self.btn_adicionar_cliente.grid(row=2, column=0, pady=5)

        # Registro de fiados
        tk.Label(self.frame_fiado, text="Selecionar Cliente:", bg="#f4f4f4").grid(row=0, column=0, pady=5)
        
        # Treeview para exibir os clientes ordenados alfabeticamente
        self.treeview_clientes = ttk.Treeview(self.frame_fiado, columns=("Nome"), show="headings")
        self.treeview_clientes.heading("Nome", text="Nome do Cliente")
        self.treeview_clientes.grid(row=1, column=0, pady=5)

        self.treeview_clientes.bind("<<TreeviewSelect>>", self.exibir_produtos_devidos)

        tk.Label(self.frame_fiado, text="Produto Fiado:", bg="#f4f4f4").grid(row=2, column=0, pady=5)
        self.entry_produto = tk.Entry(self.frame_fiado, width=20)
        self.entry_produto.grid(row=3, column=0, pady=5)

        self.btn_adicionar_fiado = tk.Button(self.frame_fiado, text="Adicionar Fiado", command=self.adicionar_fiado, bg="#ffc107", fg="white", font=("Arial", 10, "bold"))
        self.btn_adicionar_fiado.grid(row=4, column=0, pady=5)

        # Controle de pagamentos (usando Treeview agora)
        tk.Label(self.frame_pagamento, text="Selecionar Cliente:", bg="#f4f4f4").grid(row=0, column=0, pady=5)

        # Treeview para selecionar clientes para controle de pagamento
        self.treeview_pagamento = ttk.Treeview(self.frame_pagamento, columns=("Nome"), show="headings")
        self.treeview_pagamento.heading("Nome", text="Nome do Cliente")
        self.treeview_pagamento.grid(row=1, column=0, pady=5)

        self.treeview_pagamento.bind("<<TreeviewSelect>>", self.exibir_produtos_devidos_pagamento)

        self.lista_produtos_devidos = tk.Listbox(self.frame_pagamento, height=6, width=30, bg="#f1f1f1", font=("Arial", 10))
        self.lista_produtos_devidos.grid(row=1, column=1, pady=5, padx=10)

        self.btn_marcar_pago = tk.Button(self.frame_pagamento, text="Marcar como Pago", command=self.marcar_pago, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
        self.btn_marcar_pago.grid(row=2, column=0, pady=5)

        self.btn_mostrar_devedores = tk.Button(self.frame_pagamento, text="Mostrar Devedores", command=self.mostrar_devedores, bg="#dc3545", fg="white", font=("Arial", 10, "bold"))
        self.btn_mostrar_devedores.grid(row=3, column=0, pady=5)

        # Carregar os dados após a criação dos widgets
        self.carregar_dados()

    def salvar_dados(self):
        """Salva os dados em um arquivo JSON."""
        with open("dados_adega.json", "w") as file:
            json.dump(self.clientes, file)

    def carregar_dados(self):
        """Carrega os dados do arquivo JSON, se existir."""
        if os.path.exists("dados_adega.json"):
            with open("dados_adega.json", "r") as file:
                self.clientes = json.load(file)

            # Atualiza as Treeviews com os clientes ordenados alfabeticamente
            for cliente in sorted(self.clientes.keys()):
                self.treeview_clientes.insert("", "end", values=(cliente,))
                self.treeview_pagamento.insert("", "end", values=(cliente,))

    def adicionar_cliente(self):
        nome = self.entry_cliente.get().strip()
        if nome and nome not in self.clientes:
            self.clientes[nome] = []
            self.treeview_clientes.insert("", "end", values=(nome,))
            self.treeview_pagamento.insert("", "end", values=(nome,))
            self.entry_cliente.delete(0, tk.END)
            self.salvar_dados()
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' adicionado com sucesso!")
        elif nome in self.clientes:
            messagebox.showerror("Erro", "Cliente já cadastrado!")
        else:
            messagebox.showerror("Erro", "Nome do cliente não pode ser vazio!")

    def adicionar_fiado(self):
        selecionado = self.treeview_clientes.selection()
        if selecionado:
            cliente = self.treeview_clientes.item(selecionado)["values"][0]
            produto = self.entry_produto.get().strip()
            if produto:
                self.clientes[cliente].append({"produto": produto, "pago": False})
                self.entry_produto.delete(0, tk.END)
                self.salvar_dados()
                messagebox.showinfo("Sucesso", f"Produto '{produto}' adicionado para o cliente '{cliente}'.")
                self.exibir_produtos_devidos(None)
            else:
                messagebox.showerror("Erro", "Nome do produto não pode ser vazio!")
        else:
            messagebox.showerror("Erro", "Selecione um cliente na lista!")

    def exibir_produtos_devidos(self, event):
        """Exibe os produtos devidos para o cliente selecionado na lista de Fiados."""
        selecionado = self.treeview_clientes.selection()
        if selecionado:
            cliente = self.treeview_clientes.item(selecionado)["values"][0]
            self.lista_produtos_devidos.delete(0, tk.END)
            for fiado in self.clientes[cliente]:
                if not fiado["pago"]:
                    self.lista_produtos_devidos.insert(tk.END, fiado["produto"])

    def exibir_produtos_devidos_pagamento(self, event):
        """Exibe os produtos devidos para o cliente selecionado na lista de pagamentos."""
        selecionado = self.treeview_pagamento.selection()
        if selecionado:
            cliente = self.treeview_pagamento.item(selecionado)["values"][0]
            self.lista_produtos_devidos.delete(0, tk.END)
            for fiado in self.clientes[cliente]:
                if not fiado["pago"]:
                    self.lista_produtos_devidos.insert(tk.END, fiado["produto"])

    def marcar_pago(self):
        selecionado = self.treeview_pagamento.selection()
        if selecionado:
            cliente = self.treeview_pagamento.item(selecionado)["values"][0]
            fiados = [f for f in self.clientes[cliente] if not f["pago"]]
            if fiados:
                for fiado in fiados:
                    fiado["pago"] = True
                self.salvar_dados()
                messagebox.showinfo("Sucesso", f"Todas as dívidas de '{cliente}' foram marcadas como pagas.")
                self.exibir_produtos_devidos_pagamento(None)
            else:
                messagebox.showinfo("Aviso", f"'{cliente}' não possui dívidas pendentes.")
        else:
            messagebox.showerror("Erro", "Selecione um cliente na lista!")

    def mostrar_devedores(self):
        devedores = [cliente for cliente, fiados in self.clientes.items() if any(not f["pago"] for f in fiados)]
        if devedores:
            devedores_str = "\n".join(devedores)
            messagebox.showinfo("Devedores", f"Clientes com dívidas pendentes:\n{devedores_str}")
        else:
            messagebox.showinfo("Sem Devedores", "Nenhum cliente possui dívidas pendentes.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdegaApp(root)
    root.mainloop()