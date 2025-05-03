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
VERSAO_ATUAL = "v0.1.0"

root = tk.Tk()
root.title(f"Touché | Caixa de tampa solta – {VERSAO_ATUAL}")
root.geometry("1200x800")

# Parâmetros
params = {
    'Altura da base (cm)': tk.DoubleVar(value=15),
    'Largura da base (cm)': tk.DoubleVar(value=20),
    'Profundidade (cm)': tk.IntVar(value=8),
    'Altura da tampa (cm)': tk.DoubleVar(value=2),
    'Espessura (mm)': tk.DoubleVar(value=1.9),
}

preset_tamanhos = {
    "10cm x 15cm": (10, 15),
    "20cm x 20cm": (20, 20),
    "20cm x 25cm": (20, 25),
    "20cm x 30cm": (20, 30),
    "25cm x 30cm": (25, 30),
    "30cm x 30cm": (30, 30),
    "30cm x 35cm": (30, 35),
    "35cm x 40cm": (35, 40),
}

projetos_anteriores = {
    "[Gabriel Bacelar] Icon": (10, 15),
    "[LFDJ] Dia dos Namorados 2024": (35, 40),
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
        params['Largura da base (cm)'].get(),
        params['Altura da base (cm)'].get(),
        params['Altura da tampa (cm)'].get(),
        params['Espessura (mm)'].get()
    )
    draw_preview_base(
        ax_base,
        params['Largura da base (cm)'].get(),
        params['Altura da base (cm)'].get(),
        params['Profundidade (cm)'].get(),
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
            params['Largura da base (cm)'].get(),
            params['Altura da base (cm)'].get(),
            params['Profundidade (cm)'].get(),
            params['Altura da tampa (cm)'].get(),
            params['Espessura (mm)'].get()
        )
        mostrar_alerta_temporario(f"Linha de corte exportada com sucesso.")

# Alerta temporário
def mostrar_alerta_temporario(msg, tempo=3000):
    alerta = tk.Label(root, text=msg, bg='green', fg='white', font=('Arial', 10, 'bold'))
    alerta.place(relx=0.5, rely=0.97, anchor='center')
    root.after(tempo, alerta.destroy)

def mostrar_changelog():
    changelog = """
Touché | Caixa de tampa solta - v0.1.0

ADICIONADO
- Visualização ao vivo da base e tampa com réguas, etiquetas e medidas dinâmicas
- Cálculo automático de folga da tampa com base na espessura do papelão
- Exportação de linha de corte para SVG unificado (base + tampa)
- Interface gráfica completa em Tkinter com preview interativo via Matplotlib
- Campos de entrada com sliders e Combobox para parâmetros como espessura
- Presets de tamanho com botões organizados em LabelFrame
- Seção de projetos anteriores com Combobox para seleção rápida
- Exibição de etiquetas no centro das imagens ("Base", "Tampa")
- Cálculo e exibição das dimensões totais abertas da caixa
- Layout vertical organizado entre previews e controles

ALTERADO
- Terminologia ajustada: profundidade passou a representar a altura real da aba
- Visualizações separadas da tampa e base foram empilhadas verticalmente
- Substituição de slider para espessura por seleção via Combobox

CORRIGIDO
- Preenchimento incorreto em visualizações SVG
- Sobreposição de textos com limites de imagem ajustados
- Bug de formatação ao calcular medidas com valores do tipo str
"""

    popup = tk.Toplevel(root)
    popup.title("Changelog")
    popup.geometry("600x500")
    popup.resizable(False, False)

    text = tk.Text(popup, wrap='word', padx=10, pady=10)
    text.insert('1.0', changelog)
    text.config(state='disabled')
    text.pack(fill='both', expand=True)


# Aplica tamanhos predefinidos
def aplicar_preset(event):
    valor = combo_preset.get()
    if valor in preset_tamanhos:
        comp, larg = preset_tamanhos[valor]
        params['Altura da base (cm)'].set(comp)
        params['Largura da base (cm)'].set(larg)
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

        scale_range = (0, 30)
        scale = ttk.Scale(
            frame, from_=scale_range[0], to=scale_range[1],
            orient='horizontal', variable=var,
            command=lambda val: update_preview()
        )
        scale.pack(side='left', fill='x', expand=True, padx=5)


# Frame com rótulo "Tamanhos padrões"
preset_group = ttk.LabelFrame(controls_frame, text="Tamanho padrão", padding=10)
preset_group.pack(fill='x', pady=(10, 10))

def aplicar_preset_nome(nome):
    if nome in preset_tamanhos:
        comp, larg = preset_tamanhos[nome]
        params['Altura da base (cm)'].set(comp)
        params['Largura da base (cm)'].set(larg)
        update_preview()

def aplicar_projeto_anterior(event):
    nome = combo_projetos.get()
    if nome in projetos_anteriores:
        altura, largura = projetos_anteriores[nome]
        params['Altura da base (cm)'].set(altura)
        params['Largura da base (cm)'].set(largura)
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
botoes.pack(pady=5, anchor='center')
ttk.Button(botoes, text="Exportar SVG", command=gerar_svg).pack(side='left', padx=5)
ttk.Button(botoes, text="Versionamento", command=mostrar_changelog).pack(side='left', padx=5)

# Inicia preview
update_preview()
root.mainloop()