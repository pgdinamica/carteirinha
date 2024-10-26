from PIL import Image
import os

IMG_DIR = "assets"

def crop_circle(filename):
    filepath = os.path.join(IMG_DIR, filename)
    img = Image.open(filepath)
    img = img.convert("RGBA")
    # assumi que a imagem é quadrada
    cx = img.width // 2
    cy = img.height // 2
    r = img.width // 2
    # pixels = img.getdata()
    for i in range(img.width):
        for j in range(img.height):
            if (i - cx)**2 + (j - cy)**2 - r**2 > 0:
                value = img.getpixel((i, j)) #pixels[i][j]
                # value[-1] = 0
                img.putpixel((i, j), (0, 0, 0, 0))
    img.save(os.path.join(IMG_DIR, "cropped.png"))
    
if __name__ == '__main__':
    crop_circle("avatar.jpg")