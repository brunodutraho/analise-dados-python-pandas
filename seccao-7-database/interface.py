import tkinter as tk
from tkinter import messagebox
import orm


def limpar_campos():
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_ano.delete(0, tk.END)
    entry_nota.delete(0, tk.END)


def adicionar_filme():
    nome = entry_nome.get()
    ano = entry_ano.get()
    nota = entry_nota.get()

    if not nome or not ano or not nota:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    try:
        ano = int(ano)
        nota = float(nota)

        filme_id = orm.adiciona_filme(nome, ano, nota)
        messagebox.showinfo("Sucesso", f"Filme adicionado com ID {filme_id}")
        limpar_campos()

    except ValueError:
        messagebox.showerror(
            "Erro", "Ano deve ser inteiro e Nota deve ser decimal."
        )


def atualizar_filme():
    id = entry_id.get()

    if not id:
        messagebox.showerror("Erro", "Informe o ID para atualizar.")
        return

    try:
        id = int(id)
        nome = entry_nome.get() or None
        ano = int(entry_ano.get()) if entry_ano.get() else None
        nota = float(entry_nota.get()) if entry_nota.get() else None

        if orm.atualiza_filme(id, nome, ano, nota):
            messagebox.showinfo("Sucesso", "Filme atualizado com sucesso!")
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Filme não encontrado.")

    except ValueError:
        messagebox.showerror(
            "Erro", "ID e Ano devem ser inteiros. Nota deve ser decimal."
        )


def deletar_filme():
    id = entry_id.get()

    if not id:
        messagebox.showerror("Erro", "Informe o ID para deletar.")
        return

    try:
        id = int(id)

        if orm.deleta_filme(id):
            messagebox.showinfo("Sucesso", "Filme deletado com sucesso!")
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Filme não encontrado.")

    except ValueError:
        messagebox.showerror("Erro", "ID deve ser inteiro.")


# 🔹 Interface gráfica
root = tk.Tk()
root.title("Gerenciador de Filmes")

# Campos
tk.Label(root, text="ID:").grid(row=0, column=0)
entry_id = tk.Entry(root, width=40)
entry_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nome:").grid(row=1, column=0)
entry_nome = tk.Entry(root, width=40)
entry_nome.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Ano:").grid(row=2, column=0)
entry_ano = tk.Entry(root, width=40)
entry_ano.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Nota:").grid(row=3, column=0)
entry_nota = tk.Entry(root, width=40)
entry_nota.grid(row=3, column=1, padx=10, pady=5)

# Botões
tk.Button(root, text="Adicionar", command=adicionar_filme).grid(row=4, column=0, pady=10)
tk.Button(root, text="Atualizar", command=atualizar_filme).grid(row=4, column=1)
tk.Button(root, text="Deletar", command=deletar_filme).grid(row=4, column=2)

root.mainloop()