import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from math_touche import export_to_svg, draw_preview_base, draw_preview_top

VERSAO_ATUAL = "v0.2.0"

root = tk.Tk()
root.title(f"Touché | Caixa de tampa solta – {VERSAO_ATUAL}")
root.geometry("850x800")

# Parâmetros
params_tampa = {
    'Folga (mm)': tk.DoubleVar(value=6),
    'Profundidade (cm)': tk.DoubleVar(value=2),
}

usar_folga_personalizada = tk.BooleanVar(value=False)

params_caixa = {
    'Largura (cm)': tk.DoubleVar(value=20),
    'Comprimento (cm)': tk.DoubleVar(value=15),
    'Profundidade (cm)': tk.DoubleVar(value=8),
}

params_geral = {
    'Espessura (mm)': tk.DoubleVar(value=1.9)
}

espessuras_disponiveis = [
    1.50, 
    1.90, 
    2.00, 
    2.55
]

folga = None

# Atualiza preview
def update_preview(event=None):
    if usar_folga_personalizada.get():
        folga_valor = params_tampa['Folga (mm)'].get()
    else:
        folga_valor = None

    draw_preview_top(
        ax_top,
        params_caixa['Largura (cm)'].get(),
        params_caixa['Comprimento (cm)'].get(),
        params_tampa['Profundidade (cm)'].get(),
        params_geral['Espessura (mm)'].get(),
        folga_valor,
        params_tampa['Folga (mm)'] if not usar_folga_personalizada.get() else None
    )
    draw_preview_base(
        ax_base,
        params_caixa['Largura (cm)'].get(),
        params_caixa['Comprimento (cm)'].get(),
        params_caixa['Profundidade (cm)'].get(),
        params_geral['Espessura (mm)'].get(),
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

    # Definir folga com base no checkbutton
    if usar_folga_personalizada.get():
        folga_valor = params_tampa['Folga (mm)'].get()
    else:
        folga_valor = None

    if caminho:
        export_to_svg(
            caminho,
            params_caixa['Largura (cm)'].get(),
            params_caixa['Comprimento (cm)'].get(),
            params_caixa['Profundidade (cm)'].get(),
            params_tampa['Profundidade (cm)'].get(),
            params_geral['Espessura (mm)'].get(),
            folga_valor
        )
        mostrar_alerta_temporario(f"Linha de corte exportada com sucesso.")

# Alerta temporário
def mostrar_alerta_temporario(msg, tempo=3000):
    alerta = tk.Label(root, text=msg, bg='green', fg='white', font=('Arial', 10, 'bold'))
    alerta.place(relx=0.5, rely=0.97, anchor='center')
    root.after(tempo, alerta.destroy)

# Frame principal
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Frame esquerdo (preview)
preview_frame = ttk.Frame(main_frame)
preview_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

fig = plt.Figure(figsize=(2, 8), dpi=120)
ax_top = fig.add_subplot(211)
ax_base = fig.add_subplot(212)

canvas = FigureCanvasTkAgg(fig, master=preview_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X)
canvas.get_tk_widget().configure(width=400, height=1000)

# Frame direito (controles)
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(side='left', fill='y')

# Parâmetros da tampa
inputs_tampa = ttk.LabelFrame(controls_frame, text="Parâmetros da tampa", padding=15)
inputs_tampa.pack(fill="x")

for nome, var in params_tampa.items():
    frame = ttk.Frame(inputs_tampa)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=15).pack(side='left')

    if nome == 'Folga (mm)':
        # Subframe para checkbox + entry colados
        folga_frame = ttk.Frame(frame)
        folga_frame.pack(side='right')

        chk = ttk.Checkbutton(folga_frame, variable=usar_folga_personalizada, text="🔓", command=update_preview)
        chk.pack(side='left')

        entry = ttk.Entry(folga_frame, textvariable=var, width=5)
        entry.pack(side='right', padx=(0, 0))
        entry.bind("<KeyRelease>", update_preview)
    else:
        entry = ttk.Entry(frame, textvariable=var, width=5)
        entry.pack(side='right')
        entry.bind("<KeyRelease>", update_preview)

        scale_range = (0, 10)
        scale = ttk.Scale(
            frame, from_=scale_range[0], to=scale_range[1],
            orient='horizontal', variable=var,
            command=lambda val: update_preview()
        )
        scale.pack(side='left', fill='x', expand=True, padx=5)

# Parâmetros da caixa
inputs_caixa = ttk.LabelFrame(controls_frame, text="Parâmetros da caixa", padding=15)
inputs_caixa.pack(fill="x", pady=10)

for nome, var in params_caixa.items():
    frame = ttk.Frame(inputs_caixa)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=15).pack(side='left')

    entry = ttk.Entry(frame, textvariable=var, width=5)
    entry.pack(side='right')
    entry.bind("<KeyRelease>", update_preview)

    scale_range = (0, 30)
    scale = ttk.Scale(
        frame, from_=scale_range[0], to=scale_range[1],
        orient='horizontal', variable=var,
        command=lambda val: update_preview()
    )
    scale.pack(side='left', fill='x', expand=True, padx=5)

# Parâmetros da gerais
inputs_geral = ttk.LabelFrame(controls_frame, text="Parâmetros gerais", padding=15)
inputs_geral.pack(fill="x")

for nome, var in params_geral.items():
    frame = ttk.Frame(inputs_geral)
    frame.pack(fill='x', pady=4)

    ttk.Label(frame, text=nome, width=12).pack(side='left')

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

        scale_range = (0, 5)
        scale = ttk.Scale(
            frame, from_=scale_range[0], to=scale_range[1],
            orient='horizontal', variable=var,
            command=lambda val: update_preview()
        )
        scale.pack(side='left', fill='x', expand=True, padx=5)

# Botões
botoes = ttk.Frame(controls_frame)
botoes.pack(pady=5, anchor='center')
ttk.Button(botoes, text="Exportar SVG", command=gerar_svg).pack(side='left', padx=5)

# Inicia preview
update_preview()
root.mainloop()
