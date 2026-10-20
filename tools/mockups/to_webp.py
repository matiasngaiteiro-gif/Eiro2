# PNG de los mockups → img/mockups/<nombre>-1200.webp y -600.webp
import os, glob
from PIL import Image
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out = os.path.join(root, "img", "mockups"); os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(os.path.join(root, "tools", "mockups", "png", "*.png"))):
    n = os.path.basename(f)[:-4]
    im = Image.open(f).convert("RGB")
    for w in (1200, 600):
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(os.path.join(out, f"{n}-{w}.webp"), "WEBP", quality=82, method=6)
    print("ok", n)
