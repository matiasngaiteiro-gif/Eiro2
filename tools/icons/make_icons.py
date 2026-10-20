# A partir de tools/icons/g-big.png arma favicon.ico, apple-touch-icon.png, img/icon-192/512.png
# y el avatar para redes (img/avatar-eiro.png, 1080×1080): G color papel (#F5F6F1) centrada sobre verde bosque (#0E3A31).
import os
from PIL import Image, ImageOps
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
g = Image.open(os.path.join(root, "tools/icons/g-big.png")).convert("L")
g = g.crop(g.point(lambda v: 255 if v > 40 else 0).getbbox())  # recorta a la letra
def icon(size, frac):
    im = Image.new("RGB", (size, size), "#0E3A31")
    s = frac * size / max(g.size)
    gl = g.resize((max(1, round(g.width * s)), max(1, round(g.height * s))), Image.LANCZOS)
    white = Image.new("RGB", gl.size, "#F5F6F1")
    im.paste(white, ((size - gl.width) // 2, (size - gl.height) // 2), gl)
    return im
icon(512, .64).save(os.path.join(root, "img/icon-512.png"))
icon(192, .64).save(os.path.join(root, "img/icon-192.png"))
icon(180, .62).save(os.path.join(root, "apple-touch-icon.png"))
icon(1080, .5).save(os.path.join(root, "img/avatar-eiro.png"))   # entra en el recorte circular de Instagram
favs = [icon(s, .8) for s in (48, 32, 16)]
favs[0].save(os.path.join(root, "favicon.ico"), sizes=[(48, 48), (32, 32), (16, 16)], append_images=favs[1:])
print("ok")
