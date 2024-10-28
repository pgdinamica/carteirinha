from PIL import Image
import os

IMG_DIR = "assets"

def process_input(args):
    user_info = {}
    name = []
    for part in args:
        if part.startswith("@"):
            user_info['username'] = part[1:]
        elif part.isnumeric():
            user_info['subscribed_since'] = part
        else:
            name.append(part)
    user_info['name'] = ' '.join(name)
    return user_info

def crop_circle(img):
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
    return img

def limit_img_size(img:Image, limit=1024):
    width, height = img.size
    if max(width, height) < limit:
        limit = max(width, height)
    left = (width - limit) // 2
    top = (height - limit) // 2
    right = (width + limit) // 2
    bottom = (height + limit) // 2
    # Corta o centro da imagem
    img = img.crop((left, top, right, bottom))
    return img

if __name__ == '__main__':
    img = Image.open(os.path.join(IMG_DIR, "avatar.jpg"))
    cropped = crop_circle(img)
    cropped.save(os.path.join(IMG_DIR, "cropped.png"))