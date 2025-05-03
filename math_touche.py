import svgwrite

def export_to_svg(file_name, width, height, depth, thickness):
    W = width      # largura da base (X)
    H = height     # altura da base (Y)
    D = depth      # profundidade (altura real das abas)
    T = thickness  # espessura do papelão

    dwg = svgwrite.Drawing(
        file_name,
        size=(f"{W + 2 * D + 2 * T}mm", f"{H + 2 * D + 2 * T}mm"),
        viewBox=f"0 0 {W + 2 * D + 2 * T} {H + 2 * D + 2 * T}"
    )

    x0, y0 = T + D, T + D  # canto inferior esquerdo da base
    x1, y1 = x0 + W, y0 + H
    xL = x0 - D
    D2 = D / 2
    xb = x1 + D

    def add_polyline(points, color):
        dwg.add(dwg.polyline(points, stroke=color, fill='none'))

    # Base (vinco)
    add_polyline([
        (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)
    ], color="red")

    # Aba superior
    add_polyline([
        (x0, y1), (x0 - T, y1), (x0 - T, y1 + D2), (x0, y1 + D2),
        (x0, y1 + D), (x1, y1 + D), (x1, y1 + D2), (x1 + T, y1 + D2),
        (x1 + T, y1), (x1, y1)
    ], color="black")

    # Aba inferior
    add_polyline([
        (x0, y0), (x0 - T, y0), (x0 - T, y0 - D2), (x0, y0 - D2),
        (x0, y0 - D), (x1, y0 - D), (x1, y0 - D2), (x1 + T, y0 - D2),
        (x1 + T, y0), (x1, y0)
    ], color="black")

    # Aba esquerda
    add_polyline([
        (x0, y0), (x0 - D2, y0), (x0 - D2, y0 - T), (xL, y0 - T),
        (xL, y1 + T), (x0 - D2, y1 + T), (x0 - D2, y1), (x0, y1)
    ], color="black")

    # Aba direita
    add_polyline([
        (x1, y0), (xb - D2, y0), (xb - D2, y0 - T), (xb, y0 - T),
        (xb, y1 + T), (xb - D2, y1 + T), (xb - D2, y1), (x1, y1)
    ], color="black")

    dwg.save()


def draw_preview(ax, width, height, depth, thickness, label_largura=None, label_altura=None):
    ax.clear()
    ax.set_aspect('equal')

    W = width
    H = height
    D = depth
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
    ], 'black')

    # Aba inferior
    ax.plot([
        x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1
    ], [
        y0, y0, y0 - D2, y0 - D2, y0 - D, y0 - D, y0 - D2, y0 - D2, y0, y0
    ], 'black')

    # Aba esquerda
    ax.plot([
        x0, x0 - D2, x0 - D2, xL, xL, x0 - D2, x0 - D2, x0
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black')

    # Aba direita
    ax.plot([
        x1, xb - D2, xb - D2, xb, xb, xb - D2, xb - D2, x1
    ], [
        y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1
    ], 'black')

    # Base (vinco)
    ax.plot([
        x0, x1, x1, x0, x0
    ], [
        y0, y0, y1, y1, y0
    ], 'red')

    # Atualiza os labels de dimensão total, se forem fornecidos
    if label_largura and label_altura:
        largura_total = W + 2 * D
        altura_total = H + 2 * D
        label_largura.config(text=f"Largura total: {largura_total} mm")
        label_altura.config(text=f"Altura total: {altura_total} mm")
