import ezdxf
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def gerar_dxf_com_cores_recuos_completos(nome_arquivo, comprimento, largura, altura, recuo):
    C = comprimento
    L = largura
    H = altura

    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    doc.layers.new("corte", dxfattribs={"color": 7})
    doc.layers.new("vinco", dxfattribs={"color": 1})

    x0, y0 = 0, 0
    x1, y1 = x0 + C, y0 + L
    xL = x0 - H
    H2 = H / 2
    xb = x1 + H

    msp.add_lwpolyline([
        (x0, y1), (x0 - recuo, y1), (x0 - recuo, y1 + H/2), (x0, y1 + H/2),
        (x0, y1 + H), (x1, y1 + H), (x1, y1 + H/2), (x1 + recuo, y1 + H/2),
        (x1 + recuo, y1), (x0, y1)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x0, y1), (x1, y1), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x0, y0), (x0 - recuo, y0), (x0 - recuo, y0 - H/2), (x0, y0 - H/2),
        (x0, y0 - H), (x1, y0 - H), (x1, y0 - H/2), (x1 + recuo, y0 - H/2),
        (x1 + recuo, y0), (x0, y0)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x0, y0), (x1, y0), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x0, y0), (x0 - H2, y0), (x0 - H2, y0 - recuo), (xL, y0 - recuo),
        (xL, y1 + recuo), (x0 - H2, y1 + recuo), (x0 - H2, y1), (x0, y1)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x0, y0), (x0, y1), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x1, y0), (xb - H2, y0), (xb - H2, y0 - recuo), (xb, y0 - recuo),
        (xb, y1 + recuo), (xb - H2, y1 + recuo), (xb - H2, y1), (x1, y1)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x1, y0), (x1, y1), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x0, y0), (x1, y0), (x1, y1), (x0, y1)
    ], close=True, dxfattribs={"layer": "vinco"})

    doc.saveas(nome_arquivo)

def desenhar_preview(ax, comprimento, largura, altura, recuo):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    C = comprimento
    L = largura
    H = altura
    H2 = H / 2
    x0, y0 = 0, 0
    x1, y1 = x0 + C, y0 + L
    xL = x0 - H
    xb = x1 + H

    ax.plot([x0, x0 - recuo, x0 - recuo, x0, x0, x1, x1, x1 + recuo, x1 + recuo, x0],
            [y1, y1, y1 + H2, y1 + H2, y1 + H, y1 + H, y1 + H2, y1 + H2, y1, y1], 'black')
    
    ax.plot([x0, x0 - recuo, x0 - recuo, x0, x0, x1, x1, x1 + recuo, x1 + recuo, x0],
            [y0, y0, y0 - H2, y0 - H2, y0 - H, y0 - H, y0 - H2, y0 - H2, y0, y0], 'black')
    
    ax.plot([x0, x0 - H2, x0 - H2, xL, xL, x0 - H2, x0 - H2, x0],
            [y0, y0, y0 - recuo, y0 - recuo, y1 + recuo, y1 + recuo, y1, y1], 'black')
    
    ax.plot([x1, xb - H2, xb - H2, xb, xb, xb - H2, xb - H2, x1],
            [y0, y0, y0 - recuo, y0 - recuo, y1 + recuo, y1 + recuo, y1, y1], 'black')
    
    ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], color='red')

    # Adiciona legenda (após todos os plots)
    ax.plot([], [], color='black', label='Corte')
    ax.plot([], [], color='red', label='Vinco')
    ax.legend(loc='upper right', fontsize=8)

def criar_gui():
    root = tk.Tk()
    root.title("Touché | Caixa de tampa solta (mm)")

    params = {
        'Comprimento': tk.DoubleVar(value=350),
        'Largura': tk.DoubleVar(value=100),
        'Altura': tk.DoubleVar(value=80),
        'Espessura': tk.DoubleVar(value=1.9),
    }

    def atualizar_preview(*args):
        desenhar_preview(ax,
            params['Comprimento'].get(),
            params['Largura'].get(),
            params['Altura'].get(),
            params['Espessura'].get()
        )
        canvas.draw()

    def gerar_dxf():
        try:
            gerar_dxf_com_cores_recuos_completos(
                "caixa_recuo_gerada.dxf",
                params['Comprimento'].get(),
                params['Largura'].get(),
                params['Altura'].get(),
                params['Espessura'].get()
            )
            messagebox.showinfo("Sucesso", "Arquivo 'caixa_recuo_gerada.dxf' salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    top_frame = ttk.Frame(root)
    top_frame.pack(fill='both', expand=True)

    fig = plt.Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=top_frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(fill='x', padx=20, pady=10)

    for nome, var in params.items():
        frame = ttk.Frame(bottom_frame)
        frame.pack(fill='x', pady=4)

        ttk.Label(frame, text=nome + " (mm)", width=14).pack(side='left')
        entry = ttk.Entry(frame, textvariable=var, width=8)
        entry.pack(side='right', padx=5)
        entry.bind('<KeyRelease>', atualizar_preview)

        scale_range = (0, 3) if nome == 'Espessura' else (0, 1000)

        scale = ttk.Scale(
            frame, from_=scale_range[0], to=scale_range[1],
            orient='horizontal', variable=var,
            command=lambda val: atualizar_preview()
        )
        scale.pack(side='left', fill='x', expand=True, padx=5)

    # Botões alinhados horizontalmente
    button_frame = ttk.Frame(bottom_frame)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Exportar DXF", command=gerar_dxf).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Exportar PDF", command=lambda: fig.savefig("preview_caixa.pdf")).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Exportar SVG", command=lambda: fig.savefig("preview_caixa.svg")).pack(side="left", padx=5)

    atualizar_preview()
    root.mainloop()

criar_gui()