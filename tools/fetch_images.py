"""Usado por .github/workflows/fetch-images.yml: baja las imágenes de tools/fetch-images.txt
("nombre url" por línea) y guarda en img/gen/ un JPG de 1800 px y WebP de 900 y 1800 px."""
import io, os, sys, urllib.request
from PIL import Image

os.makedirs("img/gen", exist_ok=True)
log = []
for line in open("tools/fetch-images.txt", encoding="utf-8"):
    parts = line.split()
    if len(parts) != 2:
        continue
    name, url = parts
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        im = Image.open(io.BytesIO(data)).convert("RGB")
        big = im.copy(); big.thumbnail((1800, 1800), Image.LANCZOS)
        big.save(f"img/gen/{name}.jpg", quality=86, optimize=True, progressive=True)
        big.save(f"img/gen/{name}-1800.webp", quality=80, method=6)
        sm = im.copy(); sm.thumbnail((900, 900), Image.LANCZOS)
        sm.save(f"img/gen/{name}-900.webp", quality=80, method=6)
        log.append(f"ok {name} {im.size}")
    except Exception as e:
        log.append(f"error {name}: {e}")
open("img/gen/_log.txt", "w").write("\n".join(log) + "\n")
print("\n".join(log))
