import os
import tkinter as tk
import matplotlib.pyplot as plt

from datetime import datetime
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from math_touche import generate_dxf
from math_touche import draw_preview_top
from math_touche import draw_preview_base

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

root = tk.Tk()
root.title("Touché | Caixa de tampa solta (mm)")
root.geometry("1200x900")

params = {
    'Largura (mm)': tk.IntVar(value=150),
    'Espessura (mm)': tk.IntVar(value=2),
    'Comprimento (mm)': tk.IntVar(value=200),
    'Altura da caixa (mm)': tk.IntVar(value=80),
    'Altura da tampa (mm)': tk.IntVar(value=20),
}

preset_tamanhos = {
    "10cm x 15cm": (100, 150),
    "20cm x 20cm": (200, 200),
    "20cm x 25cm": (200, 250),
    "20cm x 30cm": (200, 300),
    "25cm x 30cm": (250, 300),
    "30cm x 30cm": (300, 300),
    "30cm x 35cm": (300, 350),
}

def update_preview(event=None):
    draw_preview_base(
        ax1,
        params['Comprimento (mm)'].get(),
        params['Largura (mm)'].get(),
        params['Altura da caixa (mm)'].get(),
        params['Espessura (mm)'].get(),
    )
    draw_preview_top(
        ax2,
        params['Comprimento (mm)'].get(),
        params['Largura (mm)'].get(),
        params['Altura da tampa (mm)'].get(),
        params['Espessura (mm)'].get(),
    )
    canvas.draw()

def gerar_pdf():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"tampa-solta_{timestamp}.pdf"
    caminho = asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF", "*.pdf")],
        initialfile=file_name,
        title="Salvar arquivo PDF"
    )
    if caminho:
        fig.savefig(caminho)
        mostrar_alerta_temporario(f"Linha de corte exportada com sucesso.")

def gerar_svg():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"tampa-solta_{timestamp}.svg"
    caminho = asksaveasfilename(
        defaultextension=".svg",
        filetypes=[("Arquivo SVG", "*.svg")],
        initialfile=file_name,
        title="Salvar arquivo SVG"
    )
    if caminho:
        fig.savefig(caminho)
        mostrar_alerta_temporario(f"Linha de corte exportada com sucesso.")

def gerar_dxf():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"tampa-solta_{timestamp}.dxf"
        caminho = asksaveasfilename(
            defaultextension=".dxf",
            filetypes=[("Arquivo DXF", "*.dxf")],
            initialfile=file_name,
            title="Salvar arquivo DXF"
        )
        if caminho:
            generate_dxf(
                caminho,
                params['Comprimento (mm)'].get(),
                params['Largura (mm)'].get(),
                params['Altura da caixa (mm)'].get(),
                params['Espessura (mm)'].get()
            )
            mostrar_alerta_temporario(f"Linha de corte exportada com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def mostrar_alerta_temporario(msg, tempo=3000):
    alerta = tk.Label(root, text=msg, bg='green', fg='white', font=('Arial', 10, 'bold'))
    alerta.place(relx=0.5, rely=0.97, anchor='center')
    root.after(tempo, alerta.destroy)

main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=10, pady=10)

preview_frame = ttk.Frame(main_frame)
preview_frame.pack(side='top', fill='both', expand=True)

titulo_frame = ttk.Frame(preview_frame)
titulo_frame.pack(side='top', fill='x')

ttk.Label(titulo_frame, text="Base", anchor='center', font=('Arial', 30, 'bold')).pack(side='left', expand=True)
ttk.Label(titulo_frame, text="Tampa", anchor='center', font=('Arial', 30, 'bold')).pack(side='right', expand=True)

fig = plt.Figure(figsize=(8, 4), dpi=100)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

canvas = FigureCanvasTkAgg(fig, master=preview_frame)
canvas.get_tk_widget().pack(side='left', fill='both', expand=True)

form_frame = ttk.Frame(main_frame)
form_frame.pack(side='bottom', fill='x', pady=10)

inputs = ttk.LabelFrame(form_frame, padding=15)
inputs.pack(side="left", fill="both", expand=True, padx=10)

def aplicar_preset(event):
    valor = combo_preset.get()
    if valor in preset_tamanhos:
        comp, larg = preset_tamanhos[valor]
        params['Comprimento (mm)'].set(comp)
        params['Largura (mm)'].set(larg)
        
        update_preview()
    if valor in preset_tamanhos:
        comp, larg = preset_tamanhos[valor]
        params['Comprimento (mm)'].set(comp)
        params['Largura (mm)'].set(larg)
        update_preview()

for nome, var in params.items():
    frame = ttk.Frame(inputs)
    frame.pack(fill='x', pady=2)
    ttk.Label(frame, text=nome, width=15).pack(side='left')
    entry = ttk.Entry(frame, textvariable=var, width=10)
    entry.pack(side='right')
    entry.bind("<KeyRelease>", update_preview)

    scale_range = (0, 3) if nome == 'Espessura (mm)' else (0, 600)

    scale = ttk.Scale(
        frame, from_=scale_range[0], to=scale_range[1],
        orient='horizontal', variable=var,
        command=lambda val: update_preview()
    )
    scale.pack(side='left', fill='x', expand=True, padx=5)

combo_preset = ttk.Combobox(inputs, values=list(preset_tamanhos.keys()), state="readonly")
combo_preset.set("Tamanhos padrões")
combo_preset.pack(fill='x', pady=5)
combo_preset.bind("<<ComboboxSelected>>", aplicar_preset)

botoes = ttk.Frame(form_frame)
botoes.pack(side="left", padx=10)

ttk.Button(botoes, text="Gerar .DXF", command=gerar_dxf).pack(pady=2)
ttk.Button(botoes, text="Gerar .PDF", command=gerar_pdf).pack(pady=2)
ttk.Button(botoes, text="Gerar .SVG", command=gerar_svg).pack(pady=2)

update_preview()

root.mainloop()
