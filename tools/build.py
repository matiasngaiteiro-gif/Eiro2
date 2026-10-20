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
KIT_CASOS = "hfs0xvx"  # tipografías de los clientes, solo en las páginas de casos: New Spirit (+ Condensed), Gotham, Shuttleblock Narrow

# tipografía real de cada marca (familia CSS del kit, peso, interletrado, tipografía para textos chicos)
BRAND_FONT = {
    "el-calenton": ("'new-spirit-condensed',serif", 700, "-.01em", "700 13px/1.2 'new-spirit-condensed',serif"),
    "extracto-importado": ("'gotham',sans-serif", 700, "-.02em", "400 11px/1.3 'gotham',sans-serif"),
    "cer": ("'shuttleblock-narrow',sans-serif", 700, "0em", None),
}


def font_vars(slug):
    f = BRAND_FONT.get(slug)
    if not f:
        return ""
    v = f";--c-font:{f[0]};--c-w:{f[1]};--c-tr:{f[2]}"
    return v + (f";--c-lab:{f[3]}" if f[3] else "")
WA = "https://wa.me/5491134850669"
WA_PROJ = WA + "?text=%C2%A1Hola!%20Tengo%20un%20proyecto%3A%20"
TEL = "tel:+5491134850669"
TEL_TXT = "+54 9 11 3485-0669"
SR_WA = '<span class="sr"> (se abre WhatsApp)</span>'
IG = "https://www.instagram.com/matiasgaiteiro/"  # cambiar por la cuenta del estudio cuando exista
IG_TXT = "@matiasgaiteiro"
SR_IG = '<span class="sr"> (se abre Instagram)</span>'

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
    dict(slug="el-calenton", publicado=True, name="El Calentón", sub="Cada line up, un estreno.", tags="Eventos · Identidad y video",
         img=("el-calenton", "Fiesta al aire libre con DJ al atardecer en El Calentón", 1800, 1013, ""),
         meta=[("Cliente", "El Calentón"), ("Rubro", "Eventos · Música latina"), ("Servicios", "Identidad, video y gráfica")],
         lead='Una fiesta que se anuncia como un estreno. <span class="gray">Identidad y teasers de video para cada edición de El Calentón, una fiesta de música latina.</span>',
         challenge='Cada fin de semana hay decenas de fiestas peleando por la misma atención.',
         did='Armamos una identidad con calor propio: color, tipografía y ritmo.',
         deliver=["Identidad visual", "Teasers de line up", "Piezas para redes", "Gráfica del evento"],
         words=["Calor", "Cielo", "Atardecer", "Noche", "Ritmo", "El Calentón"],
         zoom=("calenton-pantalla", "Pantalla LED detrás del DJ con gráfica en movimiento, al atardecer"),
         gallery=[("calenton-afiches", "Afiches del evento pegados en una pared de la ciudad"), ("calenton-historias", "Celular con una historia que anuncia el line up"), ("calenton-fiesta", "Gente bailando al atardecer con papel picado")]),
    dict(slug="crisger", publicado=False, name="Crisger", sub="Una marca, igual en todos lados.", tags="Industria · Manual de marca",
         img=("crisger", "Operario con casco y chaleco en una planta industrial", 928, 1152, "object-position:center 28%"),
         meta=[("Cliente", "Crisger"), ("Rubro", "Seguridad industrial"), ("Servicios", "Branding y manual de marca")],
         lead='Una marca que se ve igual en todos lados. <span class="gray">Manual de marca interactivo para Crisger, empresa de seguridad industrial.</span>',
         challenge='La marca se usaba distinto en la planta, en la oficina y en la web.',
         did='Ordenamos el sistema y lo llevamos a un manual interactivo.',
         deliver=["Manual de marca interactivo", "Sistema de color y tipografía", "Aplicaciones en planta y oficina", "Plantillas"],
         words=["Seguridad", "Orden", "Precisión", "Confianza", "Sistema", "Crisger"],
         zoom=("crisger-manual", "Manual de marca impreso abierto sobre un escritorio, con muestras de color"),
         gallery=[("crisger-color", "Muestras de color y especimen tipográfico"), ("crisger-planta", "Casco y chaleco con el emblema en una planta"), ("crisger-web", "Laptop con la versión web del manual")]),
    dict(slug="extracto-importado", publicado=False, name="Extracto Importado", sub="Cada fragancia, su historia.", tags="Perfumería · Contenido",
         img=None,
         meta=[("Cliente", "Extracto Importado"), ("Rubro", "Perfumería"), ("Servicios", "Contenido con creadoras")],
         lead='Cada fragancia, su propia historia. <span class="gray">Contenido con creadoras para cada lanzamiento de Extracto Importado, marca de perfumes.</span>',
         challenge='En perfumería no se puede oler a través de la pantalla.',
         did='Escribimos guiones y produjimos videos con creadoras para cada lanzamiento.',
         deliver=["Videos con creadoras", "Guiones", "Piezas para redes", "Calendario de lanzamientos"],
         words=["Deseo", "Aroma", "Piel", "Cercanía", "Historia", "Extracto Importado"],
         zoom=("extracto-creadora", "Creadora de contenido grabándose con un perfume en la mano"),
         gallery=[("extracto-producto", "Frasco de perfume sobre piedra con luz de atardecer"), ("extracto-guion", "Storyboard y guion impresos sobre el escritorio"), ("extracto-historias", "Tres celulares con historias del lanzamiento")]),
    dict(slug="cer", publicado=True, name="CER Entrenamientos", sub="El plan, en el bolsillo.", tags="Entrenamiento · Producto digital",
         img=None,
         meta=[("Cliente", "CER Entrenamientos"), ("Rubro", "Entrenamiento personalizado"), ("Servicios", "App web, interfaz y marca")],
         lead='El plan de entrenamiento, en el bolsillo. <span class="gray">Una app web para que los alumnos de CER sigan su rutina a distancia.</span>',
         challenge='Un profesor, decenas de alumnos a distancia y las rutinas perdidas en planillas.',
         did='Diseñamos una app simple: la próxima rutina arriba, cada ejercicio para tildar y el descanso con reloj.',
         deliver=["App web de seguimiento", "Diseño de interfaz", "Temporizador de descanso", "Registro de progreso"],
         words=["Constancia", "Fuerza", "Progreso", "Disciplina", "Plan", "CER"],
         zoom=("cer-descanso", "Alumno descansando entre series con el celular en la mano, en un gimnasio al atardecer"),
         gallery=[("cer-checklist", "Manos con un celular que muestra la rutina con ejercicios tildados"), ("cer-coach", "Profesor corrigiendo una sentadilla con barra"), ("cer-plan", "Plan de entrenamiento impreso, celular y tiza sobre un banco")]),
]

PUB = [pr for pr in PROJECTS if pr.get("publicado")]  # casos visibles en la web

SERVICES = [  # los cuatro primeros crean la marca; los dos últimos la cuidan todos los meses
    ("estrategia", "Estrategia", "Entendemos antes de diseñar.", ["Posicionamiento", "Naming", "Tono de voz"]),
    ("identidad", "Identidad", "Marcas que se reconocen a una cuadra.", ["Identidad visual", "Manual de marca", "Packaging"]),
    ("digital", "Digital", "Tu marca, donde está tu público.", ["Diseño web", "E-commerce", "Motion"]),
    ("eventos", "Branding de eventos", "Identidad y campaña para cada edición.", ["Sistema gráfico por edición", "Campaña y teasers de lanzamiento", "Contenido para pantallas LED"]),
    ("contenido", "Producción de contenido", "Planificación, producción y publicación.", ["Planificación editorial", "Gestión de redes", "Foto, video y UGC"]),
    ("acompanamiento", "Acompañamiento", "Un equipo creativo, sin armarlo adentro.", ["Dirección creativa externa", "Diseño mensual", "Gestión de marketing"]),
]
CREAMOS = 4

# TESTIMONIOS DE EJEMPLO: son simulados para ver el diseño. Reemplazar por testimonios reales
# (texto, nombre, rol) y poner TESTIMONIOS_REALES = True para que se quite la marca "Ejemplo".
TESTIMONIOS_REALES = False
TESTIMONIALS = [
    ("Entendieron la marca mejor que nosotros. Ahora todo lo que sacamos se ve igual de bien.", "Nombre Apellido", "Dueño · Gastronomía"),
    ("Pedimos un logo y nos ordenaron el negocio entero.", "Nombre Apellido", "Socia · Indumentaria"),
    ("Cumplieron cada fecha del calendario. Eso solo ya vale.", "Nombre Apellido", "Gerente · Industria"),
    ("Los teasers agotaron la preventa antes de anunciar el line up completo.", "Nombre Apellido", "Productor · Eventos"),
    ("Se nota que les importa. Responden rápido y proponen sin que les pidas.", "Nombre Apellido", "Fundadora · Cosmética"),
    ("El manual nos ahorró meses de idas y vueltas con proveedores.", "Nombre Apellido", "Marketing · Industria"),
    ("Nuestros clientes empezaron a reconocernos en la calle.", "Nombre Apellido", "Dueño · Retail"),
    ("Trabajar con Eiro es como tener un área creativa propia.", "Nombre Apellido", "Director · Servicios"),
    ("Las piezas para redes duplicaron las consultas del mes.", "Nombre Apellido", "Dueña · Estética"),
    ("Claros con los tiempos, claros con los precios. Volvería a trabajar con ellos.", "Nombre Apellido", "Socio · Tecnología"),
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
def head(p, title, desc, path, casos=False):
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
<meta name="theme-color" content="#0E3A31">
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Azeret+Mono:wght@300;400;500&display=swap">
<link rel="stylesheet" href="https://use.typekit.net/{KIT}.css">{f'<link rel="stylesheet" href="https://use.typekit.net/{KIT_CASOS}.css">' if casos else ""}
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
    <div><span class="mono">Eiro Studio™</span><p>Creamos y cuidamos marcas. Desde Buenos Aires.</p></div>
    <div><span class="mono">Páginas</span><a href="{p or './'}">Inicio</a>{pages}</div>
    <div><span class="mono">Hablemos</span><a href="{WA_PROJ}" target="_blank" rel="noopener">WhatsApp{SR_WA}</a><a href="{IG}" target="_blank" rel="noopener">Instagram{SR_IG}</a><a href="{TEL}">{TEL_TXT}</a><span class="gray" style="min-height:32px;display:flex;align-items:center">Buenos Aires, Argentina</span></div>
  </div>
  <div class="foot-logo" aria-hidden="true">{logo(p)}</div>
  <div class="foot-bottom mono">
    <span>© {date.today().year} Eiro Studio™</span>
    <span>Hecho en Buenos Aires</span>
    <a href="#top">Volver arriba ↑</a>
  </div>
</footer>
<a class="wa-fab" href="{WA_PROJ}" target="_blank" rel="noopener"><span aria-hidden="true">●</span> WhatsApp{SR_WA}</a>
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
        zn, zalt = pr["zoom"]
        media = gen_pic(p, zn, zalt, sizes, attrs=" data-reveal")
    return f'''<a class="wcard" href="{p}trabajos/{pr["slug"]}/">
        {media}
        <div><h3 class="wcard-name">{pr["name"]}</h3><p class="wcard-sub">{pr["sub"]}</p><p class="mono">{pr["tags"]}</p></div>
      </a>'''


def free_line(p):
    return f'<a class="next-line" href="{p}contacto/" data-reveal><span>¿Tu marca es la próxima?</span><span class="mono">Hablemos →</span></a>'


def rows_services(with_ids=True, part=None):
    out = []
    for i, (sid, name, line, items) in enumerate(SERVICES):
        if part == "creamos" and i >= CREAMOS or part == "cuidamos" and i < CREAMOS:
            continue
        lis = "".join(f"<li>{x}</li>" for x in items)
        idattr = f' id="{sid}"' if with_ids else ""
        out.append(f'<article class="row"{idattr} data-reveal><h3><span class="num mono">0{i+1}</span>{name}</h3><div class="row-body"><p>{line}</p><ul>{lis}</ul></div></article>')
    return "\n      ".join(out)


def steps_html():
    return "\n      ".join(f'<li class="step" data-reveal><span class="mono">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS))


def values_html():
    return "\n      ".join(f'<article class="value" data-reveal><h3>{t}</h3><p>{d}</p></article>' for t, d in VALUES)


def contact_btns(cls="btn"):
    return (f'<div class="ctas"><a class="{cls}" href="{WA_PROJ}" target="_blank" rel="noopener">WhatsApp{SR_WA}</a>'
            f'<a class="{cls} line" href="{IG}" target="_blank" rel="noopener">Instagram{SR_IG}</a></div>')


def cta_band(p, title="¿Tenés un proyecto? Hablemos."):
    return f'''
  <section class="pad sec cta-sec" aria-label="Contacto">
    <div class="cta-band" data-reveal><h2>{title}</h2>{contact_btns()}</div>
  </section>'''


def testimonials_html():
    tag = "" if TESTIMONIOS_REALES else '<span class="t-tag mono">Ejemplo</span>'
    note = "" if TESTIMONIOS_REALES else '<p class="t-note mono">Testimonios de ejemplo. Se reemplazan por los reales.</p>'
    cards = "".join(f'<figure class="tcard-q">{tag}<blockquote><p>“{q}”</p></blockquote><figcaption><b>{n}</b><span class="mono">{r}</span></figcaption></figure>' for q, n, r in TESTIMONIALS)
    return f'''
  <section class="sec pad" data-label="Clientes" aria-labelledby="t-clientes">
    <div class="sec-row" data-reveal><h2 class="h2" id="t-clientes"><span>Clientes</span><span class="gray">Lo que dicen de trabajar con nosotros.</span></h2>{note}</div>
    <div class="tq-row" tabindex="0" role="region" aria-label="Testimonios, se desplazan de costado">{cards}</div>
  </section>'''


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


# Portada: los mockups pasan como un GIF (cortes secos). Se generan desde tools/mockups (ver README ahí).
MOCKUPS = [
    ("01-tarjetas", "Crisger — Tarjetas personales"), ("02-papeleria", "Crisger — Papelería"),
    ("03-credencial", "Crisger — Credencial"), ("04-bolsas", "Crisger — Bolsas"),
    ("05-redes", "Crisger — Redes sociales"), ("06-web", "Crisger — Sitio web"),
    ("07-via-publica", "Crisger — Vía pública"), ("08-etiquetas", "Crisger — Etiquetas"),
    ("09-carpeta", "Crisger — Carpeta y presupuesto"), ("10-puerta", "Crisger — Vinilo en puerta"),
]


def hero_reel(p):
    imgs = "".join(
        f'<img src="{p}img/mockups/{n}-1200.webp" srcset="{p}img/mockups/{n}-600.webp 600w, {p}img/mockups/{n}-1200.webp 1200w" '
        f'sizes="(max-width:600px) 100vw, 50vw" width="1200" height="900" alt="{cap}" data-cap="{cap}" decoding="async"'
        f'{" class=\"on\" fetchpriority=\"high\"" if i == 0 else ""}>' for i, (n, cap) in enumerate(MOCKUPS))
    return f'<div class="hero-reel" data-reel>{imgs}</div>'


# ---------- páginas ----------
def home():
    p = ""
    cards = "\n      ".join(work_card(p, pr) for pr in PUB)
    svc = "".join(f'<a href="servicios/#{sid}" data-reveal>{name}<span class="mono">0{i+1}</span></a>' for i, (sid, name, _, _) in enumerate(SERVICES))
    ld = head(p, "Eiro Studio | Estudio creativo de branding en Buenos Aires",
              "Eiro es un estudio creativo de Buenos Aires. Estrategia, identidad, digital, contenido y eventos para marcas con ganas de crecer.", "")
    org = open(os.path.join(ROOT, "tools", "org-ld.json"), encoding="utf-8").read().strip()  # datos del estudio para buscadores
    ld = ld.replace("</head>", '<script type="application/ld+json">' + org + '</script>\n</head>')
    body = f'''
<main id="top" tabindex="-1">
  <section class="hero" data-label="Inicio" aria-label="Portada">
    <div class="hero-frame">
      {hero_reel(p)}
      <div class="hero-copy">
        <h1 class="hero-title">Estudio de branding y contenido para marcas y eventos.</h1>
        <div class="hero-ctas"><a class="btn accent" href="{WA_PROJ}" target="_blank" rel="noopener">Escribinos por WhatsApp{SR_WA}</a><a class="bracket" href="trabajos/">Ver trabajos</a></div>
      </div>
      <p class="origin" id="origin" aria-hidden="true"><span class="cut"><span>G</span><span>A</span><span>I</span><span>T</span></span>EIRO</p>
      <div class="hero-meta mono"><span aria-hidden="true">Buenos Aires, Argentina</span><span class="reel-cap"><span id="reelCap" aria-hidden="true">{MOCKUPS[0][1]}</span><button type="button" class="reel-pause" data-reel-pause aria-pressed="false">Pausar</button></span></div>
    </div>
  </section>

  <section class="sec pad" data-label="Trabajos" aria-labelledby="t-trabajos">
    <div class="sec-row" data-reveal><h2 class="h2" id="t-trabajos"><span>Trabajos</span><span class="gray">Lo último que hicimos.</span></h2><a class="bracket" href="trabajos/">Ver todos</a></div>
    <div class="wgrid">
      {cards}
    </div>
    {free_line(p)}
  </section>
{testimonials_html()}

  <section class="sec pad grid" data-label="Servicios" aria-labelledby="t-servicios">
    <div class="svc-side" data-reveal>
      <h2 class="h2" id="t-servicios"><span>Qué hacemos</span><span class="gray">Creamos y cuidamos marcas.</span></h2>
      <a class="bracket" href="servicios/">Ver servicios</a>
    </div>
    <nav class="svc-list" aria-label="Servicios">{svc}</nav>
  </section>

{cta_band(p)}
</main>'''
    write("index.html", ld + chrome(p, "", "Inicio") + body + footer(p))


def trabajos():
    p = "../"
    cards = "\n      ".join(work_card(p, pr) for pr in PUB)
    html = head(p, "Trabajos | Eiro Studio", "Proyectos de Eiro Studio: identidad, contenido y eventos para marcas de Argentina.", "trabajos/") + chrome(p, "trabajos", "Trabajos") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Trabajos</span>', 'Trabajos', 'Marcas que crecen con nosotros.', None)}
  <section class="sec pad" aria-label="Proyectos">
    <div class="wgrid">
      {cards}
    </div>
    {free_line(p)}
    <p class="cap mono" style="margin-top:32px;color:var(--soft)">Hay más proyectos. Te los mostramos cuando hablemos.</p>
  </section>
</main>''' + footer(p)
    write("trabajos/index.html", html)


def gen_pic(p, name, alt, sizes, cls="media", attrs=""):
    """Imagen generada (img/gen): JPG de respaldo + WebP en dos anchos."""
    return (f'<figure class="{cls}"{attrs}><picture><source type="image/webp" srcset="{p}img/gen/{name}-900.webp 900w, {p}img/gen/{name}-1800.webp 1800w" sizes="{sizes}">'
            f'<img src="{p}img/gen/{name}.jpg" alt="{alt}" loading="lazy" decoding="async"></picture></figure>')


def _rows(word, n=4):
    rep = ("  " + word) * 6
    return "".join(f'<span class="row rt">{rep}{rep}</span>' for _ in range(n))


MOTION = {
    # El Calentón: logos y colores del manual de marca v2; el movimiento sigue su guion (día, el dato, barrido, el pico, cierre)
    "el-calenton": dict(vars="--c-bg:#1C2F5E;--c-ink:#E1E4E7;--c-acc:#E65329;--c-amb:#F2A03D", pieces=[
        ("wide", "Teaser de line up", '<div class="ec-teaser" aria-hidden="true">'
            '<span class="day"></span><span class="cloud c1"></span><span class="cloud c2"></span>'
            '<img class="sec" src="{P}img/clientes/el-calenton/secundaria.webp" alt="">'
            '<span class="artist rt">Anthony Godfather</span>'
            '<span class="night"></span><span class="sweep"></span>'
            '<span class="deg rt"><span class="win"><span class="nums"><span>28</span><span>29</span><span>30</span><span>31</span><span>32</span><span>33</span><span>34</span><span>35</span><span>36</span><span>37</span><span>38</span><span>39</span><span>40</span></span></span><i>°</i></span>'
            '<img class="main" src="{P}img/clientes/el-calenton/principal.webp" alt=""><span class="date rt">11.10</span></div>'),
        ("", "Flyer · aniversario", '<div class="ec-flyer" aria-hidden="true"><span class="stars"></span>'
            '<span class="top"><span>Latin Music Festival</span><span>Primer aniversario</span></span>'
            '<span class="big rt">11.10</span><span class="name rt">Anthony Godfather</span>'
            '<img class="sec" src="{P}img/clientes/el-calenton/secundaria.webp" alt=""></div>'),
        ("", "Historia · temperatura", '<div class="ec-temp" aria-hidden="true"><span class="sky"></span>'
            '<span class="lab">Sube la temperatura</span>'
            '<span class="deg rt"><span class="win"><span class="nums"><span>28</span><span>29</span><span>30</span><span>31</span><span>32</span><span>33</span><span>34</span><span>35</span><span>36</span><span>37</span><span>38</span><span>39</span><span>40</span></span></span><i>°</i></span>'
            '<span class="th"><i></i></span>'
            '<img class="iso" src="{P}img/clientes/el-calenton/isotipo.webp" alt=""></div>'),
    ]),
    "crisger": dict(vars="--c-bg:#1E2124;--c-ink:#F2F2F2;--c-acc:#FF6A13;--c-line:rgba(242,242,242,.3)", pieces=[
        ("wide", "Construcción de marca", '<div class="k-build" aria-hidden="true"><svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">'
            '<line x1="0" y1="300" x2="1600" y2="300"/><line x1="0" y1="600" x2="1600" y2="600"/><line x1="560" y1="0" x2="560" y2="900"/><line x1="1040" y1="0" x2="1040" y2="900"/>'
            '<circle cx="800" cy="390" r="190"/><rect x="610" y="200" width="380" height="380"/>'
            '<rect class="shape" x="650" y="240" width="150" height="300"/><circle class="shape" cx="900" cy="390" r="110"/></svg>'
            '<span class="word rt">CRISGER</span></div>'),
        ("", "Sistema de color", '<div class="k-swatch" aria-hidden="true" style="position:absolute;inset:0">'
            '<span class="sw" style="background:#FF6A13;color:#1E2124">Naranja seguridad<b>01</b></span>'
            '<span class="sw" style="background:#2B2F33">Carbón<b>02</b></span>'
            '<span class="sw" style="background:#B9BDC1;color:#1E2124">Acero<b>03</b></span>'
            '<span class="sw" style="background:#F2F2F2;color:#1E2124">Blanco<b>04</b></span></div>'),
        ("", "Manual · páginas", '<div class="k-pages" aria-hidden="true" style="position:absolute;inset:0">'
            '<div class="pg" style="background:#F2F2F2;color:#1E2124"><span>Manual de marca · 01</span><b>Logo</b></div>'
            '<div class="pg" style="background:#FF6A13;color:#1E2124"><span>Manual de marca · 02</span><b>Color</b></div>'
            '<div class="pg" style="background:#2B2F33;color:#F2F2F2"><span>Manual de marca · 03</span><b>Tipografía</b></div>'
            '<div class="pg" style="background:#B9BDC1;color:#1E2124"><span>Manual de marca · 04</span><b>Aplicaciones</b></div></div>'),
    ]),
    "extracto-importado": dict(vars="--c-bg:#1A120A;--c-ink:#F5E9D8;--c-acc:#C98A2E", pieces=[
        ("wide", "Campaña · loop", f'<div class="k-stack" aria-hidden="true">{_rows("EXTRACTO IMPORTADO")}</div>'),
        ("", "Lanzamiento · notas", '<div class="k-bottle" aria-hidden="true" style="position:absolute;inset:0"><span class="lab">Nueva fragancia</span>'
            '<span class="bt"><span class="liq"></span></span>'
            '<span class="notes rt"><span>Salida</span><span>Corazón</span><span>Fondo</span></span></div>'),
        ("", "Historia con creadora", '<div class="k-story rt" aria-hidden="true" style="position:absolute;inset:0"><div class="bars"><i></i><i></i><i></i></div>'
            '<div class="fr" style="background:#2A1C10"><b>Lo probé</b><span>Contenido con creadoras</span></div>'
            '<div class="fr" style="background:#C98A2E;color:#1A120A"><b>Me encantó</b><span>Notas de salida, corazón y fondo</span></div>'
            '<div class="fr" style="background:#F5E9D8;color:#1A120A"><b>Link en bio</b><span>Lanzamiento</span></div></div>'),
    ]),
    "cer": dict(vars="--c-bg:#0B0B0C;--c-ink:#F2F2F0;--c-acc:#FF6A13", pieces=[
        ("wide", "App · loop", f'<div class="k-stack" aria-hidden="true">{_rows("CER ENTRENAMIENTOS")}</div>'),
        ("", "Temporizador de descanso", '<div class="k-timer" aria-hidden="true" style="position:absolute;inset:0"><span class="lab">Descanso</span>'
            '<div class="clk rt"><span>1:30</span><span>1:00</span><span>0:30</span><span>0:00</span></div><span class="tbar"><i></i></span>'
            '<span class="fl"></span><b class="go rt">A la próxima serie</b></div>'),
        ("", "Rutina · ejercicios", '<div class="k-check" aria-hidden="true" style="position:absolute;inset:0"><span class="lab">Semana 2 · Estímulo A</span><ul>'
            '<li><i></i><b class="rt">Press de banca</b><em>4 × 3</em></li><li><i></i><b class="rt">Dominadas</b><em>3 × 4</em></li>'
            '<li><i></i><b class="rt">Press de hombros</b><em>3 × 7</em></li><li><i></i><b class="rt">Vuelo lateral</b><em>3 × 7</em></li></ul>'
            '<span class="done rt">Rutina completada</span></div>'),
    ]),
}


def motion_html(pr):
    m = MOTION.get(pr["slug"])
    if not m:
        return ""
    items = "\n      ".join(
        f'<figure class="reel {cls}" style="{m["vars"]}{font_vars(pr["slug"])}">{body.replace("{P}", "../../")}<figcaption>{cap}</figcaption></figure>' for cls, cap, body in m["pieces"])
    return f'''
  <!-- placa 04 · la marca en movimiento -->
  <section class="pad reels-wrap" aria-labelledby="t-motion">
    <div class="reels-head"><h2 class="mono" id="t-motion">04 — En movimiento</h2><button type="button" data-pause aria-pressed="false">Pausar</button></div>
    <div class="reels">
      {items}
    </div>
  </section>
'''


def words_piece(pr):
    """Pieza 1080×1350 (4:5): las palabras de la marca suben solas, en mayúscula, con sus colores y su tipografía."""
    ws = pr["words"]
    n = len(ws)
    items = "".join(f'<li><span style="--w:{len(w)}">{w}</span></li>' for w in ws + ws[:1])
    # cada palabra queda quieta en el centro el 70% de su tiempo y después sube a la siguiente
    frames = []
    for k in range(n):
        a, b = k / n * 100, (k + .7) / n * 100
        frames.append(f"{a:.2f}%,{b:.2f}%{{transform:translateY({-k * 1.25:.2f}em)}}")
    frames.append(f"100%{{transform:translateY({-n * 1.25:.2f}em)}}")
    kf = f"kw-{pr['slug']}"
    m = MOTION.get(pr["slug"], {"vars": ""})
    col = f'<ul class="col rt" style="animation-name:{kf};animation-duration:{n * 1.5:.1f}s">{items}</ul>'
    return f'''
  <!-- placa 05 · la marca en palabras: pieza 1080×1350 que sube sola -->
  <section class="pad words-wrap" aria-labelledby="t-palabras">
    <div class="reels-head"><h2 class="mono" id="t-palabras">05 — En palabras</h2><button type="button" data-pause aria-pressed="false">Pausar</button></div>
    <style>@keyframes {kf}{{{"".join(frames)}}}</style>
    <div class="reels solo">
      <figure class="reel k-words" style="{m["vars"]}{font_vars(pr["slug"])}">
        <p class="sr">{", ".join(ws)}.</p>
        <div aria-hidden="true">{col}<div class="hi">{col}</div></div>
        <figcaption>Pieza 1080 × 1350</figcaption>
      </figure>
    </div>
  </section>'''


def inter_pic(p, item, label):
    n, alt = item
    return f'''
  <section class="pad inter" aria-label="{label}">
    {gen_pic(p, n, alt, "100vw", attrs=' data-scrub="free"')}
  </section>'''


def next_link(p, nxt):
    if nxt:
        return f'<a class="next-plate" href="{p}trabajos/{nxt["slug"]}/"><span class="mono">Siguiente proyecto →</span><b style="--w:{max(len(x) for x in nxt["name"].split())}">{nxt["name"]}</b></a>'
    return f'<a class="next-plate" href="{p}contacto/"><span class="mono">¿Tu marca es la próxima? →</span><b style="--w:8">Hablemos</b></a>'


def caso(i, pr):
    p = "../../"
    nxt = PUB[(PUB.index(pr) + 1) % len(PUB)] if len(PUB) > 1 else None
    meta = "".join(f'<div><dt class="mono">{k}</dt><dd>{v}</dd></div>' for k, v in pr["meta"])
    sub = " ".join(f'<span class="wi" style="--i:{k}">{w}</span>' for k, w in enumerate(pr["sub"].split()))
    zn, zalt = pr["zoom"]
    zoom = gen_pic(p, zn, zalt, "100vw", cls="media-f")
    g = pr["gallery"]
    html = head(p, f'{pr["name"]} | Trabajos | Eiro Studio', f'{pr["name"]}: {pr["sub"]} Un proyecto de Eiro Studio.', f'trabajos/{pr["slug"]}/', casos=True) + chrome(p, "trabajos", "Trabajos") + f'''
<main id="top" tabindex="-1">
  <!-- placa 00 · título -->
  <section class="plate-title" aria-labelledby="t-page">
    <p class="crumb mono"><a href="{p or './'}">Eiro</a><span aria-hidden="true">/</span><a href="{p}trabajos/">Trabajos</a><span aria-hidden="true">/</span><span>0{PUB.index(pr)+1}</span></p>
    <dl class="case-meta">{meta}</dl>
    <h1 class="kin" id="t-page" style="--w:{max(len(x) for x in pr["name"].split())}"><span class="ln"><span>{pr["name"]}</span></span></h1>
    <p class="kin-sub">{sub}</p>
    <span class="scroll-hint mono" aria-hidden="true">Scroll ↓</span>
  </section>

  <!-- placa 01 · imagen principal, quieta: invita a bajar al proyecto -->
  <section class="lead-img" aria-label="Imagen principal">
    <span class="plate-label mono" aria-hidden="true">01 — {pr["name"]}</span>
    {zoom}
    <div class="zoom-cap mono" aria-hidden="true"><span>{pr["tags"]}</span><span>Eiro Studio™</span></div>
  </section>

  <!-- 02 · desafío (texto quieto) -->
  <section class="pad story" aria-labelledby="t-desafio">
    <h2 class="plate-label mono" id="t-desafio">02 — Desafío</h2>
    <p class="wtext">{pr["challenge"]}</p>
  </section>
{inter_pic(p, g[0], "Imagen del proyecto")}

  <!-- 03 · qué hicimos (texto quieto) -->
  <section class="pad story" aria-labelledby="t-hicimos">
    <h2 class="plate-label mono" id="t-hicimos">03 — Qué hicimos</h2>
    <p class="wtext">{pr["did"]}</p>
  </section>
{motion_html(pr)}
{inter_pic(p, g[1], "Imagen del proyecto")}
{words_piece(pr)}
{inter_pic(p, g[2], "Imagen del proyecto")}

  {next_link(p, nxt)}
</main>''' + footer(p)
    write(f'trabajos/{pr["slug"]}/index.html', html)


def servicios():
    p = "../"
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    html = head(p, "Servicios | Eiro Studio", "Estrategia, identidad, digital, contenido, eventos y acompañamiento. Por proyecto o todo el año.", "servicios/") + chrome(p, "servicios", "Servicios") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Servicios</span>', 'Qué hacemos', 'Creamos y cuidamos marcas.', 'Por proyecto o todo el año.')}
  <section class="sec pad grid table-sec" aria-label="Áreas de trabajo">
    <div class="table-head" data-reveal><h2 class="h2"><span>Creamos</span><span class="gray">Proyectos con principio y fin.</span></h2></div>
    <div class="rows">
      {rows_services(part="creamos")}
    </div>
  </section>

  <section class="sec pad grid table-sec" aria-label="Acompañamiento mensual">
    <div class="table-head" data-reveal><h2 class="h2"><span>Cuidamos</span><span class="gray">Todos los meses.</span></h2></div>
    <div class="rows">
      {rows_services(part="cuidamos")}
    </div>
  </section>

  <section class="sec pad grid table-sec" aria-labelledby="t-faq">
    <div class="table-head" data-reveal><h2 class="h2" id="t-faq"><span>Preguntas</span><span class="gray">Las que nos hacen siempre.</span></h2></div>
    <div class="faq" data-reveal>{faq}</div>
  </section>
{cta_band(p)}
</main>''' + footer(p)
    write("servicios/index.html", html)


def matias_photo(p):
    """Foto real de Matías: subir img/matias.jpg (vertical 4:5) y aparece sola. Mientras tanto, un marco vacío."""
    if os.path.exists(os.path.join(ROOT, "img", "matias.jpg")):
        return f'<figure class="media" data-reveal><img src="{p}img/matias.jpg" alt="Matías Gaiteiro, fundador de Eiro Studio" loading="lazy" decoding="async"></figure>'
    return '<div class="media photo-slot" data-reveal><span class="mono">Foto de Matías<br>Pendiente</span></div>'


def estudio():
    p = "../"
    html = head(p, "Estudio | Eiro Studio", "Eiro viene de Gaiteiro. Un estudio creativo de Buenos Aires movido por el optimismo, el trabajo en equipo y el oficio.", "estudio/") + chrome(p, "estudio", "Estudio") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Estudio</span>', 'Estudio', 'Eiro viene de Gaiteiro.')}
  <section class="pad manifesto" aria-label="Manifiesto">
    <p class="statement" data-reveal>Detrás de cada marca hay gente con una historia por contar. <span class="gray">Nosotros la creamos y la cuidamos.</span></p>
  </section>
  <section class="pad" aria-label="El nombre">
    <div class="name-frame" data-reveal>
      <p class="origin" id="origin" data-wait aria-hidden="true"><span class="cut"><span>G</span><span>A</span><span>I</span><span>T</span></span>EIRO</p>
    </div>
  </section>

  <section class="sec pad grid table-sec" aria-labelledby="t-quien" style="padding-top:var(--sec)">
    <div class="studio-photo">{matias_photo(p)}</div>
    <div class="founder" data-reveal>
      <h2 class="h2" id="t-quien"><span>Quién está detrás</span><span class="gray">Matías Gaiteiro.</span></h2>
      <p class="founder-bio">Soy diseñador multimedial. Hace más de diez años que diseño marcas, coordino equipos de redes y llevo áreas de marketing.</p>
      <p class="founder-text">Estudié relaciones públicas y se nota: casi todos mis clientes llegaron por vínculos de años, y se quedaron. Cada proyecto lo encaro de cerca, con un equipo armado a medida.</p>
      <blockquote class="founder-quote"><p>“No se me ocurría ningún nombre. Al final le borré una parte a mi apellido y quedó Eiro.”</p></blockquote>
      <dl class="founder-facts">
        <div><dt class="mono">Oficio</dt><dd>Más de 10 años</dd></div>
        <div><dt class="mono">Hace</dt><dd>Diseño, marketing y redes</dd></div>
        <div><dt class="mono">Base</dt><dd>Buenos Aires</dd></div>
      </dl>
      {contact_btns()}
    </div>
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
      {contact_btns()}
    </div>
    <dl class="rows">
      <div class="row" data-reveal><dt>Proyectos nuevos</dt><dd class="row-body" style="margin:0"><p>Contanos tu idea. El café va por nuestra cuenta.</p><a href="{WA_PROJ}" target="_blank" rel="noopener">WhatsApp{SR_WA}</a><br><a href="{TEL}">{TEL_TXT}</a></dd></div>
      <div class="row" data-reveal><dt>Instagram</dt><dd class="row-body" style="margin:0"><p>Mirá lo último que estamos haciendo.</p><a href="{IG}" target="_blank" rel="noopener">{IG_TXT}{SR_IG}</a></dd></div>
      <div class="row" data-reveal><dt>Estudio</dt><dd class="row-body" style="margin:0"><p>Buenos Aires, Argentina.</p><ul><li>Respondemos rápido.</li></ul></dd></div>
    </dl>
  </section>
</main>''' + footer(p)
    write("contacto/index.html", html)


def sitemap():
    today = date.today().isoformat()
    paths = ["", "trabajos/", "servicios/", "estudio/", "contacto/"] + [f'trabajos/{pr["slug"]}/' for pr in PUB]
    urls = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in paths)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


if __name__ == "__main__":
    home(); trabajos(); servicios(); estudio(); contacto()
    for i, pr in enumerate(PUB):
        caso(i, pr)
    sitemap()
    print("ok")
