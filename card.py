from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.graphics.shapes import (Drawing, Rect,
                                       Circle, String,
                                       Image)

from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import json
import os


registerFont(TTFont("FiraSans", "assets/FiraSans-Regular.ttf"))

registerFont(TTFont("FiraSans-Bold", "assets/FiraSans-Bold.ttf"))



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

def draw_profile_frame(drawing: Drawing):
    w = drawing.width
    h = drawing.height
    cx = w // 4
    cy = h // 2
    r = h // 4 + 8
    circ_frame = Circle(cx, cy, r, 
           strokeColor=PG_COLORS["green"],
           fillColor=PG_COLORS["green"])
    drawing.add(circ_frame)

    return circ_frame.getBounds()

def draw_name_and_username(drawing: Drawing, user,
                           x, y, 
                           margin=(16, 32)):
    
    
    xmargin = margin[0]
    ymargin = margin[1]
    name = String(x + xmargin, y - ymargin, 
                  user['name'], 
                  fontSize=28,
                  fontName="FiraSans-Bold",
                #   textRenderMode=BOLDFACE_MODE,
                  fillColor=colors.white,
                  strokeColor=colors.white)
    y = name.getBounds()[1]
    username = String(x + xmargin, y - ymargin, 
                  "@" + user['username'], 
                  fontSize=28,
                  fontName="FiraSans",
                  fillColor=colors.white,
                  strokeColor=colors.white)

    y = username.getBounds()[1]
    msg = f"Sou fã de carteirinha do\nProgramação Dinâmica\ndesde {user['subscribed_since']}."
    lines = msg.split("\n")
    texts = []
    for line in lines:
        mul = 0.8 if texts else 1.8
        since = String(x + xmargin,
                    y - int(mul * ymargin),
                    line,
                    fontSize=24,
                    fontName="FiraSans-Bold",
                    # textRenderMode=BOLDFACE_MODE,
                    fillColor=colors.white,
                    strokeColor=colors.white)
        y = since.getBounds()[1]
        texts.append(since)

    drawing.add(name)
    drawing.add(username)
    for elem in texts:
        drawing.add(elem)
    
    return texts[-1].getBounds()
    
def draw_profile_picture(image, mycanva: canvas.Canvas, 
                         framebb, margin=16):
    mycanva.drawImage(image,#"assets/avatar_cropped.png", 
                      framebb[0] + margin // 2, 
                      framebb[1] + margin // 2, 
                      framebb[2] - framebb[0] - margin, 
                      framebb[3] - framebb[1] - margin, 
                      mask=(0, 1, 0, 1, 0, 1))
    
    mycanva.drawImage("assets/logo_cropped.png", 
                      framebb[2] - 4 * margin, 
                      framebb[1], 
                      64, 
                      64, 
                      mask=(0, 1, 0, 1, 0, 1))
    
def make_carteirinha(user, image, fileoutput):
    mycanva = canvas.Canvas(fileoutput, (WIDTH, HEIGHT))
    drawing = Drawing(WIDTH, HEIGHT)
    # desenha o fundo
    draw_background(drawing)
    # desenha o quadro cirular para foto
    bbox = draw_profile_frame(drawing)
    # adiciona nome e nick
    draw_name_and_username(drawing, user, bbox[2], bbox[3])
    # coloca todos os elementos de drawing no PDF
    renderPDF.draw(drawing, mycanva, 0, 0)
    # adiciona a foto
    draw_profile_picture(image, mycanva, bbox)
    
    mycanva.save()
    if isinstance(fileoutput, BytesIO):
        fileoutput.seek(0)
    return fileoutput
    

if __name__ == '__main__':
    with open(os.path.join(DATA_DIR, "user.json"), "r") as userfile:
        content = userfile.read()
        user = json.loads(content)
    img = ImageReader(PILImage.open("assets/avatar_cropped.png"))
    make_carteirinha(user, img, os.path.join(OUT_DIR, "teste.pdf"))

    # mycanva = canvas.Canvas(
    #     os.path.join(OUT_DIR, "carteirinha.pdf"),
    #     (WIDTH, HEIGHT))
    # drawing = Drawing(WIDTH, HEIGHT)
    # # desenha o fundo
    # draw_background(drawing)
    # # desenha o quadro cirular para foto
    # bbox = draw_profile_frame(drawing)
    # # adiciona nome e nick
    # with open(os.path.join(DATA_DIR, "user.json"), "r") as userfile:
    #     content = userfile.read()
    #     user = json.loads(content)
    # draw_name_and_username(drawing, user, bbox[2], bbox[3])
    # # coloca todos os elementos de drawing no PDF
    # renderPDF.draw(drawing, mycanva, 0, 0)
    # # adiciona a foto
    # draw_profile_picture(mycanva, bbox)
    
    # # salva
    # # drawing.save(formats=['pdf', 'png'], 
    #             # outDir=OUT_DIR, fnRoot="carteirinha")
    # mycanva.save()
    # print("Carteirinha gerada com sucesso!")