from reportlab.graphics.shapes import Drawing


OUT_DIR = "grafica"

WIDTH = 640
HEIGHT = 360

drawing = Drawing(WIDTH, HEIGHT)
# save
drawing.save(formats=['pdf', 'png'], 
             outDir=OUT_DIR, fnRoot="carteirinha")