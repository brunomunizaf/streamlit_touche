import ezdxf

def generate_dxf(file_name, length, width, height, thickness):
    C = length
    L = width
    H = height

    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    doc.layers.new(
        "corte", 
        dxfattribs={"color": 7}
    )
    doc.layers.new(
        "vinco", 
        dxfattribs={"color": 1}
    )

    x0, y0 = 0, 0
    x1, y1 = x0 + C, y0 + L
    xL = x0 - H
    H2 = H / 2
    xb = x1 + H

    msp.add_lwpolyline([
        (x0, y1), (x0 - thickness, y1), (x0 - thickness, y1 + H/2), (x0, y1 + H/2),
        (x0, y1 + H), (x1, y1 + H), (x1, y1 + H/2), (x1 + thickness, y1 + H/2),
        (x1 + thickness, y1), (x0, y1)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x0, y1), (x1, y1), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x0, y0), (x0 - thickness, y0), (x0 - thickness, y0 - H/2), (x0, y0 - H/2),
        (x0, y0 - H), (x1, y0 - H), (x1, y0 - H/2), (x1 + thickness, y0 - H/2),
        (x1 + thickness, y0), (x0, y0)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x0, y0), (x1, y0), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x0, y0), (x0 - H2, y0), (x0 - H2, y0 - thickness), (xL, y0 - thickness),
        (xL, y1 + thickness), (x0 - H2, y1 + thickness), (x0 - H2, y1), (x0, y1)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x0, y0), (x0, y1), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x1, y0), (xb - H2, y0), (xb - H2, y0 - thickness), (xb, y0 - thickness),
        (xb, y1 + thickness), (xb - H2, y1 + thickness), (xb - H2, y1), (x1, y1)
    ], close=True, dxfattribs={"layer": "corte"})
    msp.add_line((x1, y0), (x1, y1), dxfattribs={"layer": "corte"})

    msp.add_lwpolyline([
        (x0, y0), (x1, y0), (x1, y1), (x0, y1)
    ], close=True, dxfattribs={"layer": "vinco"})

    doc.saveas(file_name)

def draw_preview(ax, length, width, height, thickness):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    C = length
    L = width
    H = height
    H2 = H / 2
    x0, y0 = 0, 0
    x1, y1 = x0 + C, y0 + L
    xL = x0 - H
    xb = x1 + H

    ax.plot([
        x0, x0 - thickness, 
        x0 - thickness, x0, 
        x0, x1, 
        x1, x1 + thickness, 
        x1 + thickness, x0
    ], [
        y1, y1, 
        y1 + H2, 
        y1 + H2, 
        y1 + H, y1 + H, 
        y1 + H2, y1 + H2, 
        y1, y1
    ], 'black')
    
    ax.plot([
        x0, x0 - thickness, 
        x0 - thickness, x0, 
        x0, x1, 
        x1, x1 + thickness, 
        x1 + thickness, x0
    ], [
        y0, y0, 
        y0 - H2, y0 - H2, 
        y0 - H, y0 - H, 
        y0 - H2, y0 - H2, 
        y0, y0
    ], 'black')
    
    ax.plot([
        x0, x0 - H2, 
        x0 - H2, xL, 
        xL, x0 - H2, 
        x0 - H2, x0
    ], [
        y0, y0, 
        y0 - thickness, y0 - thickness, 
        y1 + thickness, y1 + thickness, 
        y1, y1
    ], 'black')
    
    ax.plot([
        x1, xb - H2, 
        xb - H2, xb, 
        xb, xb - H2, 
        xb - H2, x1
    ], [
        y0, y0, 
        y0 - thickness, y0 - thickness, 
        y1 + thickness, y1 + thickness, 
        y1, y1
    ], 'black')
    
    ax.plot(
        [x0, x1, x1, x0, x0], 
        [y0, y0, y1, y1, y0], 
        color='red')

    ax.plot([], [], color='black', label='Corte')
    ax.plot([], [], color='red', label='Vinco')
    ax.legend(loc='upper right', fontsize=8)