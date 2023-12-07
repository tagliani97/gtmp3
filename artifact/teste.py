import tkinter as tk
from tkinter import filedialog

def selecionar_diretorio():
    diretorio_selecionado = filedialog.askdirectory()
    if diretorio_selecionado:
        label_diretorio.config(text=f'Diretório selecionado: {diretorio_selecionado}')

# Configuração da janela principal
root = tk.Tk()
root.title("Selecionar Diretório")

# Cria um botão para abrir o diálogo de seleção de diretório
botao_selecionar = tk.Button(root, text="Selecionar Diretório", command=selecionar_diretorio)
botao_selecionar.pack(pady=20)

# Rótulo para exibir o diretório selecionado
label_diretorio = tk.Label(root, text="")
label_diretorio.pack()

# Inicia a janela principal
root.mainloop()
