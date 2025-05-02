import sys
import os
import tkinter as tk
import matplotlib.pyplot as plt

from datetime import datetime
from tkinter import ttk, messagebox
from cx_base import generate_dxf as dxf_base
from cx_tampa import generate_dxf as dxf_tampa
from cx_base import draw_preview as draw_preview_base
from cx_tampa import draw_preview as draw_preview_tampa
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("Touché | Caixa de tampa solta (mm)")

params_base = {
    'Comprimento': tk.IntVar(value=150),
    'Largura': tk.IntVar(value=150),
    'Altura': tk.IntVar(value=80),
    'Espessura': tk.DoubleVar(value=1.9),
}

preset_base_sizes = {
    "10x15": (100, 150),
    "20x20": (200, 200),
    "20x25": (200, 250),
    "20x30": (200, 300),
    "25x30": (250, 300),
    "30x30": (300, 300),
    "30x35": (300, 350),
}

params_tampa = {
    'Comprimento': tk.IntVar(value=350),
    'Largura': tk.IntVar(value=100),
    'Altura': tk.IntVar(value=80),
    'Espessura': tk.DoubleVar(value=1.9),
}

def apply_preset_base_size(event):
    value = combo_preset.get()
    if value in preset_base_sizes:
        comp, larg = preset_base_sizes[value]
        params_base['Comprimento'].set(comp)
        params_base['Largura'].set(larg)
        update_preview_base()

def generate_dxf_base():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f'cx_tampa_solta-base__{timestamp}.dxf'
        dxf_base(
            file_name,
            params_base['Comprimento'].get(),
            params_base['Largura'].get(),
            params_base['Altura'].get(),
            params_base['Espessura'].get()
        )
        alerta = tk.Label(
            root, 
            text=f'Criado: {file_name}',
            bg='green', 
            fg='white', 
            font=('Arial', 15, 'bold')
        )
        alerta.place(relx=0.5, rely=0.96, anchor='c')
        root.after(2000, alerta.destroy)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def generate_dxf_tampa():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f'cx_tampa_solta-tampa__{timestamp}.dxf'
        dxf_tampa(
            file_name,
            params_tampa['Comprimento'].get(),
            params_tampa['Largura'].get(),
            params_tampa['Altura'].get(),
            params_tampa['Espessura'].get()
        )
        alerta = tk.Label(
            root, 
            text=f'Criado: {file_name}',
            bg='green', 
            fg='white', 
            font=('Arial', 15, 'bold')
        )
        alerta.place(relx=0.5, rely=0.96, anchor='c')
        root.after(2000, alerta.destroy)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# --- Atualização dos previews ---
def update_preview_base(event=None):
    ax_base.clear()
    ax_base.set_aspect('equal')
    ax_base.set_title("Base da Caixa")
    draw_preview_base(
        ax_base,
        length=params_base['Comprimento'].get(),
        width=params_base['Largura'].get(),
        height=params_base['Altura'].get(),
        thickness=params_base['Espessura'].get()
    )
    canvas_base.draw()

def update_preview_tampa(event=None):
    ax_tampa.clear()
    ax_tampa.set_aspect('equal')
    ax_tampa.set_title("Tampa da Caixa")
    draw_preview_tampa(
        ax_tampa,
        length=params_tampa['Comprimento'].get(),
        width=params_tampa['Largura'].get(),
        height=params_tampa['Altura'].get(),
        thickness=params_tampa['Espessura'].get()
    )
    canvas_tampa.draw()

# --- Notebook com abas ---
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# ---------------- BASE ----------------
frame_base = ttk.Frame(notebook)
notebook.add(frame_base, text="Base")

top_base = ttk.Frame(frame_base)
top_base.pack(side='top', fill='both', expand=True)

fig_base = plt.Figure(figsize=(5, 5), dpi=100)
ax_base = fig_base.add_subplot(111)
canvas_base = FigureCanvasTkAgg(fig_base, master=top_base)
canvas_base.get_tk_widget().pack(side='top', fill='both', expand=True)

bottom_base = ttk.Frame(frame_base)
bottom_base.pack(side='bottom', fill='x', padx=20, pady=10)

for name, var in params_base.items():
    frame = ttk.Frame(bottom_base)
    frame.pack(fill='x', pady=2)
    ttk.Label(frame, text=name + " (mm)", width=14).pack(side='left')
    entry = ttk.Entry(frame, textvariable=var, width=10)
    entry.pack(side='right', padx=5)
    entry.bind('<KeyRelease>', update_preview_base())

    scale_range = (0, 3) if name == 'Espessura' else (0, 600)

    scale = ttk.Scale(
        frame, from_=scale_range[0], to=scale_range[1],
        orient='horizontal', variable=var,
        command=lambda val: update_preview_base()
    )
    scale.pack(side='left', fill='x', expand=True, padx=5)

combo_preset = ttk.Combobox(bottom_base, values=list(preset_base_sizes.keys()), state="readonly")
combo_preset.set("Tamanhos pré-definidos")
combo_preset.pack(pady=5)
combo_preset.bind("<<ComboboxSelected>>", apply_preset_base_size)

button_frame = ttk.Frame(bottom_base)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Exportar DXF", command=generate_dxf_base).pack(side="left", padx=5)
ttk.Button(button_frame, text="Exportar PDF", command=lambda: fig_base.savefig("cx_tampa_solta-base.pdf")).pack(side="left", padx=5)
ttk.Button(button_frame, text="Exportar SVG", command=lambda: fig_base.savefig("cx_tampa_solta-base.svg")).pack(side="left", padx=5)

# ---------------- TAMPA ----------------
frame_tampa = ttk.Frame(notebook)
notebook.add(frame_tampa, text="Tampa")

top_tampa = ttk.Frame(frame_tampa)
top_tampa.pack(side='top', fill='both', expand=True)

fig_tampa = plt.Figure(figsize=(5, 5), dpi=100)
ax_tampa = fig_tampa.add_subplot(111)
canvas_tampa = FigureCanvasTkAgg(fig_tampa, master=top_tampa)
canvas_tampa.get_tk_widget().pack(side='top', fill='both', expand=True)

bottom_tampa = ttk.Frame(frame_tampa)
bottom_tampa.pack(side='bottom', fill='x', padx=20, pady=10)

for name, var in params_tampa.items():
    frame = ttk.Frame(bottom_tampa)
    frame.pack(fill='x', pady=2)
    ttk.Label(frame, text=name + " (mm)", width=14).pack(side='left')
    entry = ttk.Entry(frame, textvariable=var, width=10)
    entry.pack(side='right', padx=5)
    entry.bind('<KeyRelease>', update_preview_tampa())

    scale_range = (0, 3) if name == 'Espessura' else (0, 1000)

    scale = ttk.Scale(
        frame, from_=scale_range[0], to=scale_range[1],
        orient='horizontal', variable=var,
        command=lambda val: update_preview_tampa()
    )
    scale.pack(side='left', fill='x', expand=True, padx=5)

button_frame = ttk.Frame(bottom_tampa)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Exportar DXF", command=generate_dxf_tampa).pack(side="left", padx=5)
ttk.Button(button_frame, text="Exportar PDF", command=lambda: fig_tampa.savefig("cx_tampa_solta-tampa.pdf")).pack(side="left", padx=5)
ttk.Button(button_frame, text="Exportar SVG", command=lambda: fig_tampa.savefig("cx_tampa_solta-tampa.svg")).pack(side="left", padx=5)

# Gatilho inicial
update_preview_base()
update_preview_tampa()

root.mainloop()
