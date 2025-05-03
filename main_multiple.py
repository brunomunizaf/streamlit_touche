import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from math_touche import export_to_svg, draw_preview

# Caminho Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Janela principal
root = tk.Tk()
root.title("Touché | Caixa de tampa solta")
root.geometry("1000x600")

# Parâmetros
params = {
    'Altura da base (mm)': tk.IntVar(value=150),
    'Largura da base (mm)': tk.IntVar(value=150),
    'Espessura (mm)': tk.DoubleVar(value=1.9),
    'Profundidade (mm)': tk.IntVar(value=80),
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

# Labels globais para exibir dimensões
label_largura_total = None
label_altura_total = None

# Atualiza preview
def update_preview(event=None):
    draw_preview(
        ax,
        params['Largura da base (mm)'].get(),
        params['Altura da base (mm)'].get(),
        params['Profundidade (mm)'].get(),
        params['Espessura (mm)'].get(),
        label_largura_total,
        label_altura_total
    )
    canvas.draw()

# Exporta SVG
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
        export_to_svg(
            caminho,
            params['Largura da base (mm)'].get(),
            params['Altura da base (mm)'].get(),
            params['Profundidade (mm)'].get(),
            params['Espessura (mm)'].get()
        )
        mostrar_alerta_temporario(f"Linha de corte exportada com sucesso.")

# Alerta temporário
def mostrar_alerta_temporario(msg, tempo=3000):
    alerta = tk.Label(root, text=msg, bg='green', fg='white', font=('Arial', 10, 'bold'))
    alerta.place(relx=0.5, rely=0.97, anchor='center')
    root.after(tempo, alerta.destroy)

# Aplica tamanhos predefinidos
def aplicar_preset(event):
    valor = combo_preset.get()
    if valor in preset_tamanhos:
        comp, larg = preset_tamanhos[valor]
        params['Altura da base (mm)'].set(comp)
        params['Largura da base (mm)'].set(larg)
        update_preview()

# Frame principal
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Frame esquerdo (preview)
preview_frame = ttk.Frame(main_frame)
preview_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))

fig = plt.Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=preview_frame)
canvas.get_tk_widget().pack(fill='both', expand=True)

# Frame direito (controles)
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(side='left', fill='y')

inputs = ttk.LabelFrame(controls_frame, text="Parâmetros", padding=15)
inputs.pack(fill="x")

for nome, var in params.items():
    frame = ttk.Frame(inputs)
    frame.pack(fill='x', pady=4)
    ttk.Label(frame, text=nome, width=20).pack(side='left')
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

# Presets
combo_preset = ttk.Combobox(controls_frame, values=list(preset_tamanhos.keys()), state="readonly")
combo_preset.set("Tamanhos padrões")
combo_preset.pack(fill='x', pady=(10, 0))
combo_preset.bind("<<ComboboxSelected>>", aplicar_preset)

# Labels de tamanho total
dimensoes_frame = ttk.Frame(controls_frame)
dimensoes_frame.pack(pady=10)

label_largura_total = ttk.Label(dimensoes_frame, text="Largura total: — mm")
label_altura_total = ttk.Label(dimensoes_frame, text="Altura total: — mm")
label_largura_total.pack()
label_altura_total.pack()

# Botões
botoes = ttk.Frame(controls_frame)
botoes.pack(pady=5, fill='x')
ttk.Button(botoes, text="Exportar SVG", command=gerar_svg).pack(fill='x')

# Inicia preview
update_preview()
root.mainloop()
