import math
import svgwrite

def export_to_svg(file_name, width, height, depth_base, depth_top, thickness):
    W = width * 10
    H = height * 10
    D1 = depth_base * 10
    D2 = depth_top * 10
    T = thickness

    if thickness in (1.90, 2.00):
        folga = 7.0
    elif thickness == 2.50:
        folga = 8.0
    else:
        folga = thickness * 3

    WT = W + folga
    HT = H + folga

    margin = 50

    total_height = (H + 2 * D1 + 2 * T) + (HT + 2 * D2 + 2 * T) + margin
    total_width = max(W + 2 * D1 + 2 * T, WT + 2 * D2 + 2 * T)

    dwg = svgwrite.Drawing(
        file_name,
        profile='full',
        size=(f"{total_width}mm", f"{total_height}mm"),
        viewBox=f"0 0 {total_width} {total_height}"
    )

    def add_vinco(x0, y0, x1, y1):
        dwg.add(dwg.polyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], stroke="red", fill="none", stroke_width='0.1mm'))

    def draw_base(x_offset, y_offset):
        x0, y0 = x_offset + T + D1, y_offset + T + D1
        x1, y1 = x0 + W, y0 + H
        xL = x0 - D1
        D = D1
        D2_local = D / 2
        xb = x1 + D

        add_vinco(x0, y0, x1, y1)

        path = dwg.path(stroke="black", fill="none", stroke_width='0.1mm')

        path.push("M", x0, y1)
        path.push("L", x0 - T, y1, x0 - T, y1 + D2_local, x0, y1 + D2_local, x0, y1 + D,
                  x1, y1 + D, x1, y1 + D2_local, x1 + T, y1 + D2_local, x1 + T, y1, x1, y1)

        path.push("M", x0, y0)
        path.push("L", x0 - T, y0, x0 - T, y0 - D2_local, x0, y0 - D2_local, x0, y0 - D,
                  x1, y0 - D, x1, y0 - D2_local, x1 + T, y0 - D2_local, x1 + T, y0, x1, y0)

        path.push("M", x0, y0)
        path.push("L", x0 - D2_local, y0, x0 - D2_local, y0 - T, xL, y0 - T,
                  xL, y1 + T, x0 - D2_local, y1 + T, x0 - D2_local, y1, x0, y1)

        path.push("M", x1, y0)
        path.push("L", xb - D2_local, y0, xb - D2_local, y0 - T, xb, y0 - T,
                  xb, y1 + T, xb - D2_local, y1 + T, xb - D2_local, y1, x1, y1)

        dwg.add(path)

    def draw_top(x_offset, y_offset):
        x0, y0 = x_offset + T + D2, y_offset + T + D2
        x1, y1 = x0 + WT, y0 + HT
        xL = x0 - D2
        D = D2
        D2_local = D / 2
        xb = x1 + D

        add_vinco(x0, y0, x1, y1)

        path = dwg.path(stroke="black", fill="none", stroke_width='0.1mm')

        path.push("M", x0, y1)
        path.push("L", x0 - T, y1, x0 - T, y1 + D2_local, x0, y1 + D2_local, x0, y1 + D,
                  x1, y1 + D, x1, y1 + D2_local, x1 + T, y1 + D2_local, x1 + T, y1, x1, y1)

        path.push("M", x0, y0)
        path.push("L", x0 - T, y0, x0 - T, y0 - D2_local, x0, y0 - D2_local, x0, y0 - D,
                  x1, y0 - D, x1, y0 - D2_local, x1 + T, y0 - D2_local, x1 + T, y0, x1, y0)

        path.push("M", x0, y0)
        path.push("L", x0 - D2_local, y0, x0 - D2_local, y0 - T, xL, y0 - T,
                  xL, y1 + T, x0 - D2_local, y1 + T, x0 - D2_local, y1, x0, y1)

        path.push("M", x1, y0)
        path.push("L", xb - D2_local, y0, xb - D2_local, y0 - T, xb, y0 - T,
                  xb, y1 + T, xb - D2_local, y1 + T, xb - D2_local, y1, x1, y1)

        dwg.add(path)

    draw_top(0, 0)
    draw_base(0, HT + 2 * D2 + 2 * T + margin)
    dwg.save()

def draw_preview_base(ax, width, height, depth, thickness):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    W = width * 10
    H = height * 10
    D = depth * 10
    T = thickness
    D2 = D / 2

    x0, y0 = 0, 0
    x1, y1 = x0 + W, y0 + H
    xL = x0 - D
    xb = x1 + D

    # Aba superior
    ax.plot([
        x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1
    ], [
        y1, y1, y1 + D2, y1 + D2, y1 + D, y1 + D, y1 + D2, y1 + D2, y1, y1
    ], 'black', linewidth=1)

    # Aba inferior
    ax.plot([
        x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1
    ], [
        y0, y0, y0 - D2, y0 - D2, y0 - D, y0 - D, y0 - D2, y0 - D2, y0, y0
    ], 'black', linewidth=1)

    # Aba esquerda
    ax.plot([
        x0, x0 - D2, x0 - D2, xL, xL, x0 - D2, x0 - D2, x0
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black', linewidth=1)

    # Régua vertical à esquerda da aba esquerda
    regua_x = xL - 10  # um pouco à esquerda da aba
    ax.plot([regua_x, regua_x], [y0, y1], color='blue', linewidth=1)  # linha da régua
    ax.plot([regua_x - 5, regua_x + 5], [y0, y0], color='blue')       # ponta inferior
    ax.plot([regua_x - 5, regua_x + 5], [y1, y1], color='blue')       # ponta superior
    ax.text(regua_x - 8, (y0 + y1) / 2, f"{(H + (2 * T))/10:.1f} cm", fontsize=9, color='blue', ha='right', va='center', rotation=90)

    # Aba direita
    ax.plot([
        x1, xb - D2, xb - D2, xb, xb, xb - D2, xb - D2, x1
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black', linewidth=1)

    # Base (vinco)
    ax.plot([
        x0, x1, x1, x0, x0
    ], [
        y0, y0, y1, y1, y0
    ], 'red', linewidth=1)
    ax.text((x0 + x1) / 2, y0 + 5, f"{W/10:.1f} cm", ha='center', fontsize=8)
    ax.text(x1 - 22, (y0 + y1) / 2, f"{H/10:.1f} cm", rotation=90, va='center', fontsize=8)

    # No final de draw_preview_base(...)
    x_center = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
    y_center = (ax.get_ylim()[0] + ax.get_ylim()[1]) / 2
    ax.text(x_center, y_center, "Base", fontsize=16, color="gray", ha='center', va='center')

    # Desenhar régua horizontal acima da base
    regua_y = y1 + D + 10  # um pouco acima da aba superior
    ax.plot([x0, x1], [regua_y, regua_y], color='blue', linewidth=1)  # linha da régua
    ax.plot([x0, x0], [regua_y - 5, regua_y + 5], color='blue')       # ponta esquerda
    ax.plot([x1, x1], [regua_y - 5, regua_y + 5], color='blue')       # ponta direita

    # Texto com medida
    ax.text((x0 + x1) / 2, regua_y + 8, f"{(W - (2 * T))/10:.1f} cm", ha='center', va='bottom', fontsize=9, color='blue')

    largura_total = W + 2 * D
    x_ext_esq = x0 - D
    x_ext_dir = x1 + D
    y_ref = y0 - D - 25  # abaixo das abas inferiores
    
    # Linha da régua
    ax.plot([x_ext_esq, x_ext_dir], [y_ref + 15, y_ref + 15], color='blue', linewidth=1)
    ax.plot([x_ext_esq, x_ext_esq], [y_ref + 10, y_ref + 20], color='blue')
    ax.plot([x_ext_dir, x_ext_dir], [y_ref + 10, y_ref + 20], color='blue')
    ax.text((x_ext_esq + x_ext_dir) / 2, y_ref - 20, f"{largura_total/10:.1f} cm", ha='center', va='bottom', fontsize=9, color='blue')

    altura_total = H + 2 * D
    y_ext_sup = y1 + D
    y_ext_inf = y0 - D
    x_ref = x1 + D + 15  # ao lado da aba direita
    
    # Linha da régua
    ax.plot([x_ref, x_ref], [y_ext_inf, y_ext_sup], color='blue', linewidth=1)
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_inf, y_ext_inf], color='blue')
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_sup, y_ext_sup], color='blue')
    ax.text(x_ref + 5, (y_ext_inf + y_ext_sup) / 2, f"{altura_total/10:.1f} cm", ha='left', va='center', fontsize=9, color='blue', rotation=90)
    

def draw_preview_top(ax, width, height, depth, thickness):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    if thickness in (1.90, 2.00):
        folga = 7.0
    elif thickness == 2.50:
        folga = 8.0
    else:
        folga = thickness * 3  # fallback para valores fora dos padrões

    W = (width * 10) + folga
    H = (height * 10) + folga
    D = (depth * 10)
    T = thickness
    D2 = D / 2

    x0, y0 = 0, 0
    x1, y1 = x0 + W, y0 + H
    xL = x0 - D
    xb = x1 + D

    # Aba superior
    ax.plot([
        x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1
    ], [
        y1, y1, y1 + D2, y1 + D2, y1 + D, y1 + D, y1 + D2, y1 + D2, y1, y1
    ], 'black', linewidth=1)
    # Régua horizontal acima da aba superior
    regua_y = y1 + D + 10  # um pouco acima da aba
    ax.plot([x0, x1], [regua_y, regua_y], color='blue', linewidth=1)  # linha da régua
    ax.plot([x0, x0], [regua_y - 5, regua_y + 5], color='blue')       # ponta esquerda
    ax.plot([x1, x1], [regua_y - 5, regua_y + 5], color='blue')       # ponta direita
    ax.text((x0 + x1) / 2, regua_y + 8, f"{(W - (2 * T))/10:.1f} cm", fontsize=9, color='blue', ha='center', va='bottom')

    # Aba inferior
    ax.plot([
        x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1
    ], [
        y0, y0, y0 - D2, y0 - D2, y0 - D, y0 - D, y0 - D2, y0 - D2, y0, y0
    ], 'black', linewidth=1)

    # Aba esquerda
    ax.plot([
        x0, x0 - D2, x0 - D2, xL, xL, x0 - D2, x0 - D2, x0
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black', linewidth=1)
    # Régua vertical à esquerda da aba esquerda
    regua_x = xL - 10  # um pouco à esquerda da aba
    ax.plot([regua_x, regua_x], [y0, y1], color='blue', linewidth=1)  # linha da régua
    ax.plot([regua_x - 5, regua_x + 5], [y0, y0], color='blue')       # ponta inferior
    ax.plot([regua_x - 5, regua_x + 5], [y1, y1], color='blue')       # ponta superior
    
    # Texto com medida
    ax.text(regua_x - 8, (y0 + y1) / 2, f"{(H + (2 * T))/10:.1f} cm", fontsize=9, color='blue', ha='right', va='center', rotation=90)

    # Aba direita
    ax.plot([
        x1, xb - D2, xb - D2, xb, xb, xb - D2, xb - D2, x1
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black', linewidth=1)

    # Base da tampa
    ax.plot([
        x0, x1, x1, x0, x0
    ], [
        y0, y0, y1, y1, y0
    ], 'red', linewidth=1)
    ax.text((x0 + x1) / 2, y0 + 5, f"{W/10:.1f} cm", ha='center', fontsize=8)
    ax.text(x1 - 15, (y0 + y1) / 2, f"{H/10:.1f} cm", rotation=90, va='center', fontsize=8)

    x_center = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
    y_center = (ax.get_ylim()[0] + ax.get_ylim()[1]) / 2
    ax.text(x_center, y_center, "Tampa", fontsize=16, color="gray", ha='center', va='center')

    # --- RÉGUA TOTAL HORIZONTAL (largura total com abas) ---
    largura_total = W + 2 * D
    x_ext_esq = xL
    x_ext_dir = xb
    y_ref = y0 - D - 25
    
    ax.plot([x_ext_esq, x_ext_dir], [y_ref, y_ref], color='blue', linewidth=1)
    ax.plot([x_ext_esq, x_ext_esq], [y_ref - 5, y_ref + 5], color='blue')
    ax.plot([x_ext_dir, x_ext_dir], [y_ref - 5, y_ref + 5], color='blue')
    ax.text((x_ext_esq + x_ext_dir) / 2, y_ref - 2, f"{largura_total/10:.1f} cm", color='blue', fontsize=9, ha='center', va='top')

    # --- RÉGUA TOTAL VERTICAL (altura total com abas) ---
    altura_total = H + 2 * D
    y_ext_sup = y1 + D
    y_ext_inf = y0 - D
    x_ref = xb + 20
    
    ax.plot([x_ref, x_ref], [y_ext_inf, y_ext_sup], color='blue', linewidth=1)
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_inf, y_ext_inf], color='blue')
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_sup, y_ext_sup], color='blue')
    ax.text(x_ref + 5, (y_ext_inf + y_ext_sup) / 2, f"{altura_total/10:.1f} cm", ha='left', va='center', fontsize=9, color='blue', rotation=90)
