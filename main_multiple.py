import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from math_touche import export_to_svg, draw_preview_base, draw_preview_top

# Caminho Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Janela principal
root = tk.Tk()
root.title("Touché | Caixa de tampa solta")
root.geometry("1200x800")

# Parâmetros
params = {
    'Altura da base (mm)': tk.IntVar(value=150),
    'Largura da base (mm)': tk.IntVar(value=150),
    'Profundidade (mm)': tk.IntVar(value=80),
    'Altura da tampa (mm)': tk.DoubleVar(value=20),
    'Espessura (mm)': tk.DoubleVar(value=1.9),
}

preset_tamanhos = {
    "10cm x 15cm": (100, 150),
    "20cm x 20cm": (200, 200),
    "20cm x 25cm": (200, 250),
    "20cm x 30cm": (200, 300),
    "25cm x 30cm": (250, 300),
    "30cm x 30cm": (300, 300),
    "30cm x 35cm": (300, 350),
    "35cm x 40cm": (350, 400),
}

projetos_anteriores = {
    "[Gabriel Bacelar] Icon": (100, 150),
    "[LFDJ] Dia dos Namorados 2024": (350, 400),
}

espessuras_disponiveis = [
    1.50, 
    1.90, 
    2.00, 
    2.55
]

# Atualiza preview
def update_preview(event=None):
    draw_preview_top(
        ax_top,
        params['Largura da base (mm)'].get(),
        params['Altura da base (mm)'].get(),
        params['Altura da tampa (mm)'].get(),
        params['Espessura (mm)'].get()
    )
    draw_preview_base(
        ax_base,
        params['Largura da base (mm)'].get(),
        params['Altura da base (mm)'].get(),
        params['Profundidade (mm)'].get(),
        params['Espessura (mm)'].get(),
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
            params['Altura da tampa (mm)'].get(),
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

fig = plt.Figure(figsize=(2, 8), dpi=120)
ax_top = fig.add_subplot(211)
ax_base = fig.add_subplot(212)

canvas = FigureCanvasTkAgg(fig, master=preview_frame)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X, expand=False)
canvas.get_tk_widget().configure(width=400, height=1000)

# Frame direito (controles)
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(side='left', fill='y')

inputs = ttk.LabelFrame(controls_frame, text="Parâmetros", padding=15)
inputs.pack(fill="x")

for nome, var in params.items():
    frame = ttk.Frame(inputs)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=20).pack(side='left')

    if nome == 'Espessura (mm)':
        radiobutton_frame = ttk.Frame(frame)
        radiobutton_frame.pack(side='right', fill='x', expand=True)

        for valor in espessuras_disponiveis:
            ttk.Radiobutton(
                radiobutton_frame,
                text=f"{valor}",
                value=valor,
                variable=var,
                command=update_preview
            ).pack(side='left', padx=10)
    else:
        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side='right')
        entry.bind("<KeyRelease>", update_preview)

        scale_range = (0, 600)
        scale = ttk.Scale(
            frame, from_=scale_range[0], to=scale_range[1],
            orient='horizontal', variable=var,
            command=lambda val: update_preview()
        )
        scale.pack(side='left', fill='x', expand=True, padx=5)


# Frame com rótulo "Tamanhos padrões"
preset_group = ttk.LabelFrame(controls_frame, text="Tamanhos padrões", padding=10)
preset_group.pack(fill='x', pady=(10, 10))

def aplicar_preset_nome(nome):
    if nome in preset_tamanhos:
        comp, larg = preset_tamanhos[nome]
        params['Altura da base (mm)'].set(comp)
        params['Largura da base (mm)'].set(larg)
        update_preview()

def aplicar_projeto_anterior(event):
    nome = combo_projetos.get()
    if nome in projetos_anteriores:
        altura, largura = projetos_anteriores[nome]
        params['Altura da base (mm)'].set(altura)
        params['Largura da base (mm)'].set(largura)
        update_preview()

# Container em grade para botões
preset_frame = ttk.Frame(preset_group)
preset_frame.pack(fill='x')

# Cria botões em duas colunas
colunas = 2
for i, nome in enumerate(preset_tamanhos):
    row = i // colunas
    col = i % colunas
    btn = ttk.Button(preset_frame, text=nome, width=18, command=lambda n=nome: aplicar_preset_nome(n))
    btn.grid(row=row, column=col, padx=5, pady=4, sticky='ew')

# Frame com rótulo "Projetos anteriores"
previous_group = ttk.LabelFrame(controls_frame, text="Projetos anteriores", padding=10)
previous_group.pack(fill='x', pady=(10, 10))

# Container para projetos anteriores
previous_frame = ttk.Frame(previous_group)
previous_frame.pack(fill='x')

# Combobox dentro do grupo "Projetos anteriores"
combo_projetos = ttk.Combobox(previous_frame, values=list(projetos_anteriores.keys()), state="readonly")
combo_projetos.set("Selecione um projeto")
combo_projetos.pack(fill='x', pady=5)
combo_projetos.bind("<<ComboboxSelected>>", aplicar_projeto_anterior)

# Botões
botoes = ttk.Frame(controls_frame)
botoes.pack(pady=5, fill='x')
ttk.Button(botoes, text="Exportar SVG", command=gerar_svg).pack(fill='x')

# Inicia preview
update_preview()
root.mainloop()
