from reportlab.lib import colors
from reportlab.graphics.shapes import (Drawing, Rect,
                                       Circle, String)
import json
import os

OUT_DIR = "grafica"
DATA_DIR = "data"

WIDTH = 640
HEIGHT = 360
BOLDFACE_MODE = 6

PG_COLORS = {
    "blue": colors.HexColor("#062846"),
    "green": colors.HexColor("#109395"),
}
# rgb(16 147 149), (6, 40, 70)

def draw_background(drawing, 
                    margin=(16, 16), 
                    radius=64):
    outer_rect = Rect(0, 0, WIDTH, HEIGHT, 
            fillColor=PG_COLORS["green"])
    drawing.add(outer_rect)

    xmargin = margin[0]
    ymargin = margin[1]
    inner_rect = Rect(xmargin, 
                      ymargin, 
                      WIDTH - 2 * xmargin, 
                      HEIGHT - 2 * ymargin,
                      radius, radius, 
            fillColor=PG_COLORS["blue"],
            strokeColor=PG_COLORS["blue"])
    drawing.add(inner_rect)
    return inner_rect.getBounds()

def draw_profile_picture(drawing: Drawing):
    w = drawing.width
    h = drawing.height
    cx = w // 4
    cy = h // 2
    r = h // 4 + 8
    circ_frame = Circle(cx, cy, r, 
           strokeColor=PG_COLORS["green"],
           fillColor=PG_COLORS["green"])
    drawing.add(circ_frame)
    # TODO: adicionar foto
    return circ_frame.getBounds()

def draw_name_and_username(drawing: Drawing, 
                           x, y, 
                           margin=(16, 32)):
    with open(os.path.join(DATA_DIR, "user.json"), "r") as userfile:
        content = userfile.read()
        user = json.loads(content)
    
    xmargin = margin[0]
    ymargin = margin[1]
    name = String(x + xmargin, y - ymargin, 
                  user['name'], 
                  fontSize=28,
                  textRenderMode=BOLDFACE_MODE,
                  fillColor=colors.white,
                  strokeColor=colors.white)
    y = name.getBounds()[1]
    username = String(x + xmargin, y - ymargin, 
                  "@" + user['username'], 
                  fontSize=28,
                  fillColor=colors.white,
                  strokeColor=colors.white)

    y = username.getBounds()[1]
    msg = f"Sou fã de carteirinha do\nProgramação Dinâmica\ndesde {user['subscribed_since']}."
    lines = msg.split("\n")
    texts = []
    for line in lines:
        mul = 0.8 if texts else 2
        since = String(x + xmargin,
                    y - int(mul * ymargin),
                    line,
                    fontSize=24,
                    textRenderMode=BOLDFACE_MODE,
                    fillColor=colors.white,
                    strokeColor=colors.white)
        y = since.getBounds()[1]
        texts.append(since)

    drawing.add(name)
    drawing.add(username)
    for elem in texts:
        drawing.add(elem)
    
    return texts[-1].getBounds()

# def draw_fan_text(drawing: Drawing,
#                   x, y, 
#                   margin=(16, 32)):
    


if __name__ == '__main__':
    drawing = Drawing(WIDTH, HEIGHT)
    # desenha o fundo
    draw_background(drawing)
    # desenha foto do fã
    bbox = draw_profile_picture(drawing)
    # adiciona nome e nick
    draw_name_and_username(drawing, bbox[2], bbox[3])
    # adiciona 'desde de...'

    # salva
    drawing.save(formats=['pdf', 'png'], 
                outDir=OUT_DIR, fnRoot="carteirinha")