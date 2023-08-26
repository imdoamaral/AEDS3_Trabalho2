import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def exibir_mensagem(titulo, mensagem):
    """
    Exibe uma mensagem para o usuário.

    Args:
    - titulo (str): Título da mensagem.
    - mensagem (str): Conteúdo da mensagem.
    """
    messagebox.showinfo(titulo, mensagem)

def coletar_inputs():
    """
    Coleta as entradas do usuário via interface gráfica.

    Retorna:
    - dict: Dicionário contendo as entradas do usuário.
    """
    def on_ok():
        dados['ano'] = ano_var.get()
        dados['partidos'] = [p.strip() for p in partidos_var.get().split(",")] if partidos_var.get() else []
        dados['threshold'] = float(threshold_var.get())
        janela.quit()

    def to_uppercase(*args):
        partidos_var.set(partidos_var.get().upper())

    dados = {}

    janela = tk.Tk()
    janela.title("Análise de Proximidade na Câmara de Deputados")

    # Ano
    ttk.Label(janela, text="Ano da análise:\nEx: 2023").grid(column=0, row=0, padx=20, pady=10, sticky=tk.W)
    ano_var = ttk.Entry(janela)
    ano_var.grid(column=1, row=0, padx=20, pady=10, sticky=tk.W)

    # Partidos
    ttk.Label(janela, text="Partidos (separados por vírgula):\nEx: PT, PL, PSOL").grid(column=0, row=1, padx=20, pady=10, sticky=tk.W)
    partidos_var = tk.StringVar()
    partidos_var.trace_add('write', to_uppercase)
    ttk.Entry(janela, textvariable=partidos_var).grid(column=1, row=1, padx=20, pady=10, sticky=tk.W)

    # Threshold
    ttk.Label(janela, text="Threshold das ligações:").grid(column=0, row=2, padx=20, pady=10, sticky=tk.W)
    threshold_var = ttk.Entry(janela)
    threshold_var.insert(0, "0.9")  # Definindo valor padrão
    threshold_var.grid(column=1, row=2, padx=20, pady=10, sticky=tk.W)

    # Botão PROCESSAR
    ttk.Button(janela, text="Processar", command=on_ok).grid(column=1, row=3, padx=20, pady=40, sticky=tk.E)

    janela.mainloop()
    janela.destroy()

    return dados
