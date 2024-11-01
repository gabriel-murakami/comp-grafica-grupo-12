import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import open3d as o3d

def listar_arquivos_ply():
    return [f for f in os.listdir('.') if f.endswith('.ply')]

def renderizar_ply():
    arquivo_selecionado = combo.get()
    if not arquivo_selecionado:
        messagebox.showwarning("Atenção", "Nenhum arquivo .ply selecionado!")
        return

    try:
        mesh = o3d.io.read_triangle_mesh(arquivo_selecionado)
        if not mesh.is_empty():
            o3d.visualization.draw_geometries([mesh])
        else:
            messagebox.showerror("Erro", f"O arquivo {arquivo_selecionado} está vazio ou inválido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar o arquivo {arquivo_selecionado}: {str(e)}")

root = tk.Tk()
root.title("Renderizador de Arquivos PLY")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

label = ttk.Label(frame, text="Selecione um arquivo .ply:")
label.grid(row=0, column=0, sticky=tk.W)

combo = ttk.Combobox(frame, state="readonly", values=listar_arquivos_ply())
combo.grid(row=0, column=1, sticky=(tk.W, tk.E))

botao = ttk.Button(frame, text="Renderizar", command=renderizar_ply)
botao.grid(row=0, column=2, sticky=tk.W)

root.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

root.mainloop()
