#!/usr/bin/env python3
"""Genera las páginas de eirostudio.com.

Todas las páginas comparten barra, menú, clave de acceso y pie; por eso se arman desde acá
en lugar de copiarse a mano. Uso: python3 tools/build.py (desde la raíz del repositorio).
Los estilos están en assets/eiro.css y el comportamiento en assets/eiro.js.
"""
import hashlib, json, os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://eirostudio.com/"
KIT = "oqj6tze"  # kit de Adobe Fonts: Neue Haas Grotesk, Roboto Mono, Neulis Cursive
WA = "https://wa.me/5491134850669"
WA_PROJ = WA + "?text=%C2%A1Hola!%20Tengo%20un%20proyecto%3A%20"
TEL = "tel:+5491134850669"
TEL_TXT = "+54 9 11 3485-0669"
SR_WA = '<span class="sr"> (se abre WhatsApp)</span>'

def _ver(*names):
    """Huella del contenido de los estilos y el script: cambia sola cuando cambian, así nadie ve una versión vieja guardada en caché."""
    h = hashlib.md5()
    for n in names:
        with open(os.path.join(ROOT, n), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()[:8]


VER = _ver("assets/eiro.css", "assets/eiro.js")

NAV = [("trabajos", "Trabajos"), ("servicios", "Servicios"), ("estudio", "Estudio"), ("contacto", "Contacto")]


def logo(p, cls="logo", label=None):
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    return f'<svg class="{cls}" viewBox="0 0 3850 1351" {a}><use href="{p}img/sprite.svg#i-logo"/></svg>'


def pic(p, name, sizes, alt, w, h, style="", eager=False):
    srcs = {"el-calenton": (800, 1400), "crisger": (600, 928), "estudio": (600, 928)}[name]
    srcset = ", ".join(f"{p}img/{name}-{s}.webp {s}w" for s in srcs)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    st = f' style="{style}"' if style else ""
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="{p}img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load} decoding="async"{st}></picture>')


# ---------- proyectos ----------
PROJECTS = [
    dict(slug="el-calenton", name="El Calentón", sub="Cada line up, un estreno.", tags="Eventos · Identidad y video",
         img=("el-calenton", "Fiesta al aire libre con DJ al atardecer en El Calentón", 1800, 1013, ""),
         meta=[("Cliente", "El Calentón"), ("Rubro", "Eventos · Música latina"), ("Servicios", "Identidad, video y gráfica")],
         lead='Una fiesta que se anuncia como un estreno. <span class="gray">Identidad y teasers de video para cada edición de El Calentón, una fiesta de música latina.</span>',
         challenge='Cada fin de semana hay decenas de fiestas peleando por la misma atención.',
         did='Armamos una identidad con calor propio: color, tipografía y ritmo.',
         deliver=["Identidad visual", "Teasers de line up", "Piezas para redes", "Gráfica del evento"],
         zoom=("calenton-pantalla", "Pantalla LED detrás del DJ con gráfica en movimiento, al atardecer"),
         gallery=[("calenton-afiches", "Afiches del evento pegados en una pared de la ciudad"), ("calenton-historias", "Celular con una historia que anuncia el line up"), ("calenton-fiesta", "Gente bailando al atardecer con papel picado")]),
    dict(slug="crisger", name="Crisger", sub="Una marca, igual en todos lados.", tags="Industria · Manual de marca",
         img=("crisger", "Operario con casco y chaleco en una planta industrial", 928, 1152, "object-position:center 28%"),
         meta=[("Cliente", "Crisger"), ("Rubro", "Seguridad industrial"), ("Servicios", "Branding y manual de marca")],
         lead='Una marca que se ve igual en todos lados. <span class="gray">Manual de marca interactivo para Crisger, empresa de seguridad industrial.</span>',
         challenge='La marca se usaba distinto en la planta, en la oficina y en la web.',
         did='Ordenamos el sistema y lo llevamos a un manual interactivo.',
         deliver=["Manual de marca interactivo", "Sistema de color y tipografía", "Aplicaciones en planta y oficina", "Plantillas"],
         zoom=("crisger-manual", "Manual de marca impreso abierto sobre un escritorio, con muestras de color"),
         gallery=[("crisger-color", "Muestras de color y especimen tipográfico"), ("crisger-planta", "Casco y chaleco con el emblema en una planta"), ("crisger-web", "Laptop con la versión web del manual")]),
    dict(slug="extracto-importado", name="Extracto Importado", sub="Cada fragancia, su historia.", tags="Perfumería · Contenido",
         img=None,
         meta=[("Cliente", "Extracto Importado"), ("Rubro", "Perfumería"), ("Servicios", "Contenido con creadoras")],
         lead='Cada fragancia, su propia historia. <span class="gray">Contenido con creadoras para cada lanzamiento de Extracto Importado, marca de perfumes.</span>',
         challenge='En perfumería no se puede oler a través de la pantalla.',
         did='Escribimos guiones y produjimos videos con creadoras para cada lanzamiento.',
         deliver=["Videos con creadoras", "Guiones", "Piezas para redes", "Calendario de lanzamientos"],
         zoom=("extracto-creadora", "Creadora de contenido grabándose con un perfume en la mano"),
         gallery=[("extracto-producto", "Frasco de perfume sobre piedra con luz de atardecer"), ("extracto-guion", "Storyboard y guion impresos sobre el escritorio"), ("extracto-historias", "Tres celulares con historias del lanzamiento")]),
]

SERVICES = [
    ("estrategia", "Estrategia", "Entendemos antes de diseñar.", ["Posicionamiento", "Naming", "Tono de voz"]),
    ("identidad", "Identidad", "Marcas que se reconocen a una cuadra.", ["Identidad visual", "Manual de marca", "Packaging"]),
    ("digital", "Digital", "Tu marca, donde está tu público.", ["Diseño web", "E-commerce", "Motion"]),
    ("contenido", "Contenido", "Qué decir, cuándo y cómo.", ["Estrategia de contenido", "Gestión de redes", "Foto y video"]),
    ("eventos", "Eventos", "Para que se hable antes, durante y después.", ["Identidad de eventos", "Teasers de line up", "Visuales para pantallas"]),
    ("acompanamiento", "Acompañamiento", "Un equipo creativo, sin armarlo adentro.", ["Dirección creativa externa", "Diseño mensual", "Gestión de marketing"]),
]

STEPS = [("Escuchamos", "Arrancamos con un café. Tu negocio, tu gente y lo que te quita el sueño."),
         ("Entendemos", "Miramos el mercado, la competencia y a tu público. Ahí aparece la idea."),
         ("Hacemos", "Diseñamos, producimos y probamos, con avances seguidos y decisiones compartidas."),
         ("Acompañamos", "Lanzamos con vos y seguimos cerca para que la marca crezca bien.")]

VALUES = [("Optimismo", "Creemos en tu marca antes de que el mundo la conozca."),
          ("Equipo", "Tu ritmo, tus prioridades, nuestro proceso."),
          ("Oficio", "Cuidamos el detalle donde nadie mira.")]

FAQ = [("¿Cuánto tarda un proyecto?", "Depende del alcance. Antes de arrancar te pasamos un calendario."),
       ("¿Cómo se cobra?", "Por proyecto, con presupuesto cerrado, o con un fee mensual si te acompañamos todo el año."),
       ("¿Puedo pedir una sola pieza?", "Sí. Podés sumar una sola pieza o armar el equipo completo.")]


# ---------- piezas comunes ----------
def head(p, title, desc, path):
    url = SITE + path
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url, "inLanguage": "es-AR",
          "isPartOf": {"@type": "WebSite", "name": "Eiro Studio", "url": SITE}}
    return f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0A0A0A">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Eiro Studio">
<meta property="og:locale" content="es_AR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}img/og-eiro.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" sizes="192x192" href="{p}img/icon-192.png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
{{LD}}
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('eiro-acceso')==='1')document.documentElement.classList.add('unlocked')}}catch(e){{}}</script>
<link rel="preconnect" href="https://use.typekit.net" crossorigin>
<link rel="preconnect" href="https://p.typekit.net" crossorigin>
<link rel="stylesheet" href="https://use.typekit.net/{KIT}.css">
<link rel="stylesheet" href="{p}assets/eiro.css?v={VER}">
</head>'''.replace("{LD}", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')


def chrome(p, page, where):
    items = "".join(
        f'<li><a href="{p}{slug}/"{" aria-current=\"true\"" if slug == page else ""}><span class="mono">0{i+1}</span>{name}</a></li>'
        for i, (slug, name) in enumerate(NAV))
    return f'''
<body>
<a class="skip" href="#top">Saltar al contenido</a>
<div class="gate" id="gate" role="dialog" aria-modal="true" aria-label="Acceso a Eiro">
  <div class="gate-box">
    {logo(p, label="Eiro")}
    <form id="gateForm" autocomplete="off">
      <label for="gateKey" class="sr">Clave</label>
      <input id="gateKey" name="gateKey" type="password" inputmode="numeric" maxlength="4" placeholder="Clave" enterkeyhint="go">
      <button type="submit" aria-label="Entrar">→</button>
    </form>
    <p class="gate-note mono">Estamos terminando algo bueno</p>
  </div>
</div>

<header class="bar" id="barra">
  <div class="pod">
    <a class="brand" href="{p or './'}" aria-label="Eiro Studio, ir al inicio">{logo(p)}</a>
    <span class="where mono" id="where" aria-hidden="true">{where}</span>
    <span class="dot" aria-hidden="true"></span>
  </div>
  <div class="bar-right">
    <a class="btn accent" href="{p}contacto/">Hablemos</a>
    <span class="clock mono" id="clock" aria-hidden="true">--:-- BUE</span>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú"><svg viewBox="0 0 14 14" aria-hidden="true"><circle cx="3" cy="3" r="1.6" fill="currentColor"/><circle cx="11" cy="3" r="1.6" fill="currentColor"/><circle cx="3" cy="11" r="1.6" fill="currentColor"/><circle cx="11" cy="11" r="1.6" fill="currentColor"/></svg></button>
  </div>
</header>

<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menú" hidden>
  <div class="menu-top">
    <a href="{p or './'}" aria-label="Ir al inicio">{logo(p)}</a>
    <button class="menu-btn" id="menuClose" type="button" aria-label="Cerrar menú"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.6"/></svg></button>
  </div>
  <nav aria-label="Principal"><ul>{items}</ul></nav>
  <div class="menu-foot mono">
    <span>Buenos Aires, Argentina</span>
    <a class="btn accent" href="{WA_PROJ}" target="_blank" rel="noopener">Escribinos por WhatsApp{SR_WA}</a>
  </div>
</div>
'''


def footer(p):
    pages = "".join(f'<a href="{p}{s}/">{n}</a>' for s, n in NAV)
    return f'''
<footer>
  <div class="foot-nav">
    <div><span class="mono">Eiro Studio™</span><p>Estudio creativo en Buenos Aires.</p></div>
    <div><span class="mono">Páginas</span><a href="{p or './'}">Inicio</a>{pages}</div>
    <div><span class="mono">Hablemos</span><a href="{WA_PROJ}" target="_blank" rel="noopener">WhatsApp{SR_WA}</a><a href="{TEL}">{TEL_TXT}</a><span class="gray" style="min-height:32px;display:flex;align-items:center">Buenos Aires, Argentina</span></div>
  </div>
  <div class="foot-logo" aria-hidden="true">{logo(p)}</div>
  <div class="foot-bottom mono">
    <span>© {date.today().year} Eiro Studio™</span>
    <span>Hecho en Buenos Aires</span>
    <a href="#top">Volver arriba ↑</a>
  </div>
</footer>
<script src="{p}assets/eiro.js?v={VER}" defer></script>
</body>
</html>
'''


def page_head(p, crumb, title_a, title_b, lead=None, extra=""):
    lead_html = f'<p class="page-lead" data-reveal>{lead}</p>' if lead else ""
    return f'''
  <section class="page-head grid pad" aria-labelledby="t-page">
    <p class="crumb mono" data-reveal><a href="{p or './'}">Eiro</a><span aria-hidden="true">/</span>{crumb}</p>
    <h1 class="page-title" id="t-page" data-reveal><span>{title_a}</span><span class="gray">{title_b}</span></h1>
    {lead_html}{extra}
  </section>'''


def work_card(p, pr, sizes="(max-width:820px) 100vw, 50vw"):
    if pr["img"]:
        n, alt, w, h, st = pr["img"]
        media = f'<figure class="media" data-reveal>{pic(p, n, sizes, alt, w, h, st)}</figure>'
    else:
        media = f'<div class="media type-block green" data-reveal aria-hidden="true"><span>{pr["name"]}</span></div>'
    return f'''<a class="wcard" href="{p}trabajos/{pr["slug"]}/">
        {media}
        <div><h3 class="wcard-name">{pr["name"]}</h3><p class="wcard-sub">{pr["sub"]}</p><p class="mono">{pr["tags"]}</p></div>
      </a>'''


def free_card(p):
    return f'''<a class="wcard" href="{p}contacto/">
        <div class="media type-block dark" data-reveal aria-hidden="true"><span>Tu marca</span></div>
        <div><h3 class="wcard-name">Tu marca</h3><p class="wcard-sub">Este lugar está libre.</p><p class="mono">Hablemos →</p></div>
      </a>'''


def rows_services(with_ids=True):
    out = []
    for i, (sid, name, line, items) in enumerate(SERVICES):
        lis = "".join(f"<li>{x}</li>" for x in items)
        idattr = f' id="{sid}"' if with_ids else ""
        out.append(f'<article class="row"{idattr} data-reveal><h3><span class="num mono">0{i+1}</span>{name}</h3><div class="row-body"><p>{line}</p><ul>{lis}</ul></div></article>')
    return "\n      ".join(out)


def steps_html():
    return "\n      ".join(f'<li class="step" data-reveal><span class="mono">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS))


def values_html():
    return "\n      ".join(f'<article class="value" data-reveal><h3>{t}</h3><p>{d}</p></article>' for t, d in VALUES)


def cta_band(p, title="¿Tenés un proyecto? Hablemos."):
    return f'''
  <section class="pad sec" aria-label="Contacto">
    <div class="cta-band" data-reveal><h2>{title}</h2><a class="btn" href="{WA_PROJ}" target="_blank" rel="noopener">Escribinos por WhatsApp{SR_WA}</a></div>
  </section>'''


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


# ---------- páginas ----------
def home():
    p = ""
    cards = "\n      ".join(work_card(p, pr) for pr in PROJECTS) + "\n      " + free_card(p)
    svc = "".join(f'<a href="servicios/#{sid}" data-reveal>{name}<span class="mono">0{i+1}</span></a>' for i, (sid, name, _, _) in enumerate(SERVICES))
    ld = head(p, "Eiro Studio | Estudio creativo de branding en Buenos Aires",
              "Eiro es un estudio creativo de Buenos Aires. Estrategia, identidad, digital, contenido y eventos para marcas con ganas de crecer.", "")
    org = open(os.path.join(ROOT, "tools", "org-ld.json"), encoding="utf-8").read().strip()  # datos del estudio para buscadores
    ld = ld.replace("</head>", '<script type="application/ld+json">' + org + '</script>\n</head>')
    body = f'''
<main id="top" tabindex="-1">
  <section class="hero" data-label="Inicio" aria-label="Portada">
    <div class="hero-frame">
      {pic(p, "estudio", "(max-width:600px) 100vw, 50vw", "Matías Gaiteiro trabajando en un escritorio con dos monitores, en medio de un campo al atardecer", 928, 1152, eager=True)}
      <p class="hero-kicker mono" aria-hidden="true">Estudio creativo<br>Marcas · Contenido · Eventos</p>
      <p class="origin" id="origin" aria-hidden="true"><span class="cut"><span>G</span><span>A</span><span>I</span><span>T</span></span>EIRO</p>
      <div class="hero-meta mono" aria-hidden="true"><span>Eiro Studio™ — Estudio creativo</span><span>34°36′S 58°22′O</span></div>
    </div>
  </section>

  <section class="intro grid pad" data-label="Estudio">
    <h1 class="statement short" data-reveal aria-label="Hacemos marcas inolvidables, inconfundibles, deseadas, auténticas y rentables."><span aria-hidden="true">Hacemos marcas <span class="rot"><em id="rot">inolvidables.</em></span></span></h1>
    <p class="intro-sub mono" data-reveal>Estudio creativo en Buenos Aires</p>
    <div class="intro-links" data-reveal>
      <a class="btn accent" href="contacto/">Trabajemos juntos</a>
      <a class="bracket" href="trabajos/">Ver trabajos</a>
    </div>
  </section>

  <section class="sec pad" data-label="Trabajos" aria-labelledby="t-trabajos">
    <div class="sec-row" data-reveal><h2 class="h2" id="t-trabajos"><span>Trabajos</span><span class="gray">Lo último que hicimos.</span></h2><a class="bracket" href="trabajos/">Ver todos</a></div>
    <div class="wgrid">
      {cards}
    </div>
  </section>

  <section class="sec pad grid" data-label="Servicios" aria-labelledby="t-servicios">
    <div class="svc-side" data-reveal>
      <h2 class="h2" id="t-servicios"><span>Qué hacemos</span><span class="gray">De la idea a la calle.</span></h2>
      <a class="bracket" href="servicios/">Ver servicios</a>
    </div>
    <nav class="svc-list" aria-label="Servicios">{svc}</nav>
  </section>

  <section class="pad" data-label="Contacto" aria-label="Más de Eiro">
    <div class="trio">
      <a class="tcard" href="servicios/" data-reveal><span class="mono">01 — Servicios</span><div><h3>Qué hacemos</h3><p>Seis áreas, un mismo equipo.</p></div></a>
      <a class="tcard" href="estudio/" data-reveal><span class="mono">02 — Estudio</span><div><h3>Quiénes somos</h3><p>De dónde sale el nombre.</p></div></a>
      <a class="tcard green" href="contacto/" data-reveal><span class="mono">03 — Contacto</span><div><h3>Hablemos</h3><p>El café va por nuestra cuenta.</p></div></a>
    </div>
  </section>
</main>'''
    write("index.html", ld + chrome(p, "", "Inicio") + body + footer(p))


def trabajos():
    p = "../"
    cards = "\n      ".join(work_card(p, pr) for pr in PROJECTS) + "\n      " + free_card(p)
    html = head(p, "Trabajos | Eiro Studio", "Proyectos de Eiro Studio: identidad, contenido y eventos para marcas de Argentina.", "trabajos/") + chrome(p, "trabajos", "Trabajos") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Trabajos</span>', 'Trabajos', 'Marcas que crecen con nosotros.', None)}
  <section class="sec pad" aria-label="Proyectos">
    <div class="wgrid">
      {cards}
    </div>
    <p class="cap mono" style="margin-top:48px;color:var(--soft)">Hay más proyectos. Te los mostramos cuando hablemos.</p>
  </section>
</main>''' + footer(p)
    write("trabajos/index.html", html)


def gen_pic(p, name, alt, sizes, cls="media", attrs=""):
    """Imagen generada (img/gen): JPG de respaldo + WebP en dos anchos."""
    return (f'<figure class="{cls}"{attrs}><picture><source type="image/webp" srcset="{p}img/gen/{name}-900.webp 900w, {p}img/gen/{name}-1800.webp 1800w" sizes="{sizes}">'
            f'<img src="{p}img/gen/{name}.jpg" alt="{alt}" loading="lazy" decoding="async"></picture></figure>')


def split_words(text, cls="wd"):
    """Separa una frase en palabras para animarlas una por una (el texto sigue siendo legible para lectores de pantalla)."""
    return " ".join(f'<span class="{cls}">{w}</span>' for w in text.split())


def caso(i, pr):
    p = "../../"
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    meta = "".join(f'<div><dt class="mono">{k}</dt><dd>{v}</dd></div>' for k, v in pr["meta"])
    sub = " ".join(f'<span class="wi" style="--i:{k}">{w}</span>' for k, w in enumerate(pr["sub"].split()))
    zn, zalt = pr["zoom"]
    zoom = gen_pic(p, zn, zalt, "100vw", cls="media-z")
    mq_items = "  ·  ".join(pr["deliver"])
    mq = "".join(f'<span class="mq" aria-hidden="true">{mq_items}  ·  {mq_items}  ·  {mq_items}</span>' for _ in range(2))
    gal = "\n    ".join(gen_pic(p, n, alt, "(max-width:820px) 100vw, 33vw", attrs=' data-scrub="free"') for n, alt in pr["gallery"])
    lis = "".join(f"<li>{x}</li>" for x in pr["deliver"])
    html = head(p, f'{pr["name"]} | Trabajos | Eiro Studio', f'{pr["name"]}: {pr["sub"]} Un proyecto de Eiro Studio.', f'trabajos/{pr["slug"]}/') + chrome(p, "trabajos", "Trabajos") + f'''
<main id="top" tabindex="-1">
  <!-- placa 00 · título -->
  <section class="plate-title" aria-labelledby="t-page">
    <p class="crumb mono"><a href="{p or './'}">Eiro</a><span aria-hidden="true">/</span><a href="{p}trabajos/">Trabajos</a><span aria-hidden="true">/</span><span>0{i+1}</span></p>
    <dl class="case-meta">{meta}</dl>
    <h1 class="kin" id="t-page"><span class="ln"><span>{pr["name"]}</span></span></h1>
    <p class="kin-sub">{sub}</p>
    <span class="scroll-hint mono" aria-hidden="true">Scroll ↓</span>
  </section>

  <!-- placa 01 · la imagen se abre -->
  <section class="scrub zoom" data-scrub aria-label="Imagen principal">
    <div class="stick">
      <span class="plate-label mono" aria-hidden="true">01 — {pr["name"]}</span>
      {zoom}
      <div class="zoom-cap mono" aria-hidden="true"><span>{pr["tags"]}</span><span>Eiro Studio™</span></div>
    </div>
  </section>

  <!-- placa 02 · el desafío se enciende palabra por palabra -->
  <section class="scrub words" data-scrub aria-labelledby="t-desafio">
    <div class="stick">
      <h2 class="plate-label mono" id="t-desafio">02 — Desafío</h2>
      <p class="wtext">{split_words(pr["challenge"])}</p>
    </div>
  </section>

  <!-- placa 03 · una placa blanca sube con lo que hicimos -->
  <section class="scrub wipe" data-scrub data-from=".5" aria-labelledby="t-hicimos">
    <div class="stick">
      <div class="panel">
        <h2 class="plate-label mono" id="t-hicimos">03 — Qué hicimos</h2>
        <p class="wtext">{split_words(pr["did"])}</p>
      </div>
    </div>
  </section>

  <!-- placa 04 · entregables en movimiento -->
  <section class="marquee" data-scrub="free" aria-labelledby="t-entregables">
    <h2 class="plate-label mono" id="t-entregables">04 — Entregables</h2>
    <ul class="sr">{lis}</ul>
    {mq}
  </section>

  <section class="pad gallery" aria-label="Galería">
    {gal}
  </section>

  <a class="next-plate" href="{p}trabajos/{nxt["slug"]}/"><span class="mono">Siguiente proyecto →</span><b>{nxt["name"]}</b></a>
</main>''' + footer(p)
    write(f'trabajos/{pr["slug"]}/index.html', html)


def servicios():
    p = "../"
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    html = head(p, "Servicios | Eiro Studio", "Estrategia, identidad, digital, contenido, eventos y acompañamiento. Por proyecto o todo el año.", "servicios/") + chrome(p, "servicios", "Servicios") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Servicios</span>', 'Qué hacemos', 'De la idea a la calle.', 'Por proyecto o todo el año.')}
  <section class="sec pad grid table-sec" aria-label="Áreas de trabajo">
    <div class="table-head" data-reveal><h2 class="h2"><span>Seis áreas</span><span class="gray">Un mismo equipo.</span></h2></div>
    <div class="rows">
      {rows_services()}
    </div>
  </section>

  <section class="sec pad grid table-sec" aria-labelledby="t-faq">
    <div class="table-head" data-reveal><h2 class="h2" id="t-faq"><span>Preguntas</span><span class="gray">Las que nos hacen siempre.</span></h2></div>
    <div class="faq" data-reveal>{faq}</div>
  </section>
{cta_band(p)}
</main>''' + footer(p)
    write("servicios/index.html", html)


def estudio():
    p = "../"
    html = head(p, "Estudio | Eiro Studio", "Eiro viene de Gaiteiro. Un estudio creativo de Buenos Aires movido por el optimismo, el trabajo en equipo y el oficio.", "estudio/") + chrome(p, "estudio", "Estudio") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Estudio</span>', 'Estudio', 'Eiro viene de Gaiteiro.')}
  <section class="pad" aria-label="El nombre">
    <div class="name-frame" data-reveal>
      <p class="origin" id="origin" data-wait aria-hidden="true"><span class="cut"><span>G</span><span>A</span><span>I</span><span>T</span></span>EIRO</p>
    </div>
  </section>

  <section class="sec pad grid table-sec" aria-labelledby="t-nombre" style="padding-top:var(--sec)">
    <div class="studio-photo"><figure class="media" data-reveal>{pic(p, "estudio", "(max-width:1024px) 100vw, 40vw", "Matías Gaiteiro trabajando en un escritorio con dos monitores, en medio de un campo al atardecer", 928, 1152)}</figure></div>
    <figure class="founder" data-reveal>
      <h2 class="sr" id="t-nombre">El nombre</h2>
      <blockquote><p>“No se me ocurría ningún nombre. Al final le borré una parte a mi apellido y quedó Eiro.”</p></blockquote>
      <figcaption><i style="background-image:url({p}img/estudio-600.webp)" aria-hidden="true"></i><span><b>Matías Gaiteiro</b><span class="mono">Fundador y director creativo</span></span></figcaption>
      <p class="founder-text">Trabajamos con vos, no para vos. Tu idea, nuestro oficio, un solo equipo.</p>
    </figure>
  </section>

  <section class="sec pad grid" aria-labelledby="t-valores">
    <h2 class="values-statement" id="t-valores" data-reveal><span>Nuestros valores.</span><span class="gray">Con optimismo.</span><span class="gray">En equipo.</span><span class="gray">Con oficio.</span></h2>
    <div class="values">
      {values_html()}
    </div>
  </section>

  <section class="sec pad grid" aria-labelledby="t-proceso">
    <h2 class="h2" id="t-proceso" data-reveal style="grid-column:1/-1"><span>Cómo trabajamos</span><span class="gray">Cuatro pasos, cero sorpresas.</span></h2>
    <ol class="steps">
      {steps_html()}
    </ol>
  </section>
{cta_band(p, "Contanos tu idea.")}
</main>''' + footer(p)
    write("estudio/index.html", html)


def contacto():
    p = "../"
    html = head(p, "Contacto | Eiro Studio", "Escribinos por WhatsApp y lo charlamos. Eiro Studio, Buenos Aires.", "contacto/") + chrome(p, "contacto", "Contacto") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Contacto</span>', 'Contacto', 'Hagamos algo bueno juntos.', None)}
  <section class="sec pad grid table-sec" aria-label="Formas de contacto">
    <div class="hello" data-reveal>
      <a class="hello-card" href="{WA_PROJ}" target="_blank" rel="noopener">{logo(p)}<span class="mono">Decí hola<br>WhatsApp</span><span class="arrow" aria-hidden="true">→</span>{SR_WA}</a>
    </div>
    <dl class="rows">
      <div class="row" data-reveal><dt>Proyectos nuevos</dt><dd class="row-body" style="margin:0"><p>Contanos tu idea. El café va por nuestra cuenta.</p><a href="{WA_PROJ}" target="_blank" rel="noopener">WhatsApp{SR_WA}</a><br><a href="{TEL}">{TEL_TXT}</a></dd></div>
      <div class="row" data-reveal><dt>Estudio</dt><dd class="row-body" style="margin:0"><p>Buenos Aires, Argentina.</p><ul><li>Respondemos rápido.</li></ul></dd></div>
    </dl>
  </section>
</main>''' + footer(p)
    write("contacto/index.html", html)


def sitemap():
    today = date.today().isoformat()
    paths = ["", "trabajos/", "servicios/", "estudio/", "contacto/"] + [f'trabajos/{pr["slug"]}/' for pr in PROJECTS]
    urls = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in paths)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


if __name__ == "__main__":
    home(); trabajos(); servicios(); estudio(); contacto()
    for i, pr in enumerate(PROJECTS):
        caso(i, pr)
    sitemap()
    print("ok")
