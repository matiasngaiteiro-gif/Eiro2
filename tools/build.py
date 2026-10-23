#!/usr/bin/env python3
"""Genera las páginas de eirostudio.com.

Todas las páginas comparten barra, menú, clave de acceso y pie; por eso se arman desde acá
en lugar de copiarse a mano. Uso: python3 tools/build.py (desde la raíz del repositorio).
Los estilos están en assets/eiro.css y el comportamiento en assets/eiro.js.
"""
from urllib.parse import quote
import hashlib, json, os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://eirostudio.com/"
KIT = "oqj6tze"  # kit de Adobe Fonts: Neulis Cursive (y Neue Haas, solo para la marca Crisger)
KIT_CASOS = "hfs0xvx"
KIT_WEB = "wfo6ver"  # Neue Haas Grotesk Text (Roman, Medium y Bold): la tipografía principal de la web  # tipografías de los clientes, solo en las páginas de casos: New Spirit (+ Condensed), Gotham, Shuttleblock Narrow

# tipografía real de cada marca (familia CSS del kit, peso, interletrado, tipografía para textos chicos)
BRAND_FONT = {
    "el-calenton": ("'new-spirit-condensed',serif", 700, "-.01em", "700 13px/1.2 'new-spirit-condensed',serif"),
    "extracto-importado": ("'gotham',sans-serif", 700, "-.02em", "400 11px/1.3 'gotham',sans-serif"),
    "cer": ("'shuttleblock-narrow',sans-serif", 700, "0em", None),
}


# Íconos de marca: Font Awesome Free 7 (fontawesome.com, licencia CC BY 4.0)
WA_PATH = "M380.9 97.1c-41.9-42-97.7-65.1-157-65.1-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480 117.7 449.1c32.4 17.7 68.9 27 106.1 27l.1 0c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3 18.6-68.1-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1s56.2 81.2 56.1 130.5c0 101.8-84.9 184.6-186.6 184.6zM325.1 300.5c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8s-14.3 18-17.6 21.8c-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7 .9-6.9-.5-9.7s-12.5-30.1-17.1-41.2c-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2s-9.7 1.4-14.8 6.9c-5.1 5.6-19.4 19-19.4 46.3s19.9 53.7 22.6 57.4c2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4s4.6-24.1 3.2-26.4c-1.3-2.5-5-3.9-10.5-6.6z"
IG_PATH = "M224.3 141a115 115 0 1 0 -.6 230 115 115 0 1 0 .6-230zm-.6 40.4a74.6 74.6 0 1 1 .6 149.2 74.6 74.6 0 1 1 -.6-149.2zm93.4-45.1a26.8 26.8 0 1 1 53.6 0 26.8 26.8 0 1 1 -53.6 0zm129.7 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM399 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"


def icon(path):
    return f'<svg class="ico" viewBox="0 0 448 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="{path}"/></svg>'


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
    """EIROSTUDIO: el logotipo original en vector (img/sprite.svg#i-word), nunca reescrito con texto (manual 1.3)"""
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    return f'<svg class="{cls} wordmark" viewBox="0 0 1415.86 193.46" {a}><use href="{p}img/sprite.svg#i-word"/></svg>'


def isotipo(p, cls="isotipo", label=None):
    """isologo de la marca: la e con forma de globo (img/sprite.svg#i-eiro)"""
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    return f'<svg class="{cls}" viewBox="0 0 765.98 636.35" {a}><use href="{p}img/sprite.svg#i-eiro"/></svg>'


ISO_N = [0]


def iso(p, cls="isologo", label=None):
    """isologo de línea: dos círculos que se cruzan, la barra y el remate de la e
    (geometría en tools/isologo-linea.txt; va en línea con su propio recorte)"""
    ISO_N[0] += 1
    inner = open(os.path.join(ROOT, "tools", "isologo-linea.txt"), encoding="utf-8").read().replace('id="ap"', f'id="ap{ISO_N[0]}"').replace("url(#ap)", f"url(#ap{ISO_N[0]})")
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    return f'<svg class="{cls}" viewBox="0 0 606 478" {a}>{inner}</svg>'


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

SERVICES = [
    ("marca", "Marca", "Para arrancar o renovarse: definimos quién sos y cómo te ves en todos lados.",
     ["Estrategia y naming", "Identidad visual", "Manual de marca", "Packaging y papelería"]),
    ("contenido", "Contenido", "Para estar presentes todas las semanas, sin improvisar.",
     ["Planificación editorial", "Gestión de redes", "Foto, video y UGC", "Campañas"]),
    ("eventos", "Eventos", "Para fiestas, festivales y productoras: una identidad para cada edición.",
     ["Sistema gráfico por edición", "Teasers de line up", "Pantallas LED", "Vía pública y redes"]),
    ("web", "Web", "Para vender o recibir consultas desde tu sitio.",
     ["Sitios y landings", "E-commerce", "Apps web", "Motion"]),
]

# formas de trabajar (sin precios: se cotiza cada caso)
MODES = [("Proyecto", "Para lanzar o renovar una marca.", ["Presupuesto cerrado", "Calendario por escrito", "Archivos y manual de uso"]),
         ("Abono mensual", "Un equipo creativo todo el año, sin sumar gente.", ["Monto fijo por mes", "Planificación mes a mes", "Prioridad en los tiempos"]),
         ("Pieza suelta", "Para algo puntual que no puede esperar.", ["Una pieza o una campaña", "Presupuesto en el día", "Sin compromiso"])]

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

FAQ = [("¿Cuánto tarda un proyecto?", "Depende del alcance. Antes de arrancar te pasamos un calendario por escrito."),
       ("¿Cómo se cobra?", "Por proyecto, por abono mensual o por pieza. Siempre sabés el número antes de empezar: nada de costos que aparecen en el camino."),
       ("¿Qué necesitan para arrancar?", "Una charla corta: qué hacés, a quién le hablás y qué querés lograr. Con eso armamos la propuesta."),
       ("¿De quién son los archivos?", "Tuyos. Al cerrar el proyecto te entregamos los archivos editables y el manual de uso.")]


# ---------- piezas comunes ----------
CRUMB_NAMES = {"trabajos": "Trabajos", "servicios": "Servicios", "estudio": "Estudio", "contacto": "Contacto"}


def head(p, title, desc, path, casos=False, extra_ld=None, preload=None):
    url = SITE + path
    page = {"@type": "WebPage", "name": title, "url": url, "inLanguage": "es-AR", "description": desc,
            "isPartOf": {"@type": "WebSite", "name": "Eiro Studio", "url": SITE}}
    graph = [page]
    parts = [x for x in path.strip("/").split("/") if x]
    if parts:   # migas de pan para buscadores
        items = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE}]
        acc = ""
        for k, part in enumerate(parts):
            acc += part + "/"
            name = CRUMB_NAMES.get(part) or next((pr["name"] for pr in PROJECTS if pr["slug"] == part), part)
            items.append({"@type": "ListItem", "position": k + 2, "name": name, "item": SITE + acc})
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})
    graph += extra_ld or []
    ld = {"@context": "https://schema.org", "@graph": graph}
    pre = f'\n<link rel="preload" as="image" href="{preload[0]}" imagesrcset="{preload[1]}" imagesizes="{preload[2]}" fetchpriority="high">' if preload else ""
    return f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#141517">
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
<meta property="og:image:alt" content="Eiro Studio, estudio creativo en Buenos Aires">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}img/og-eiro.jpg">
<link rel="icon" href="{p}favicon.ico" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="{p}favicon.svg">
<link rel="icon" type="image/png" sizes="192x192" href="{p}img/icon-192.png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
{{LD}}
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('eiro-acceso')==='1')document.documentElement.classList.add('unlocked')}}catch(e){{}}</script>
<link rel="preconnect" href="https://use.typekit.net" crossorigin><link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://use.typekit.net/{KIT_WEB}.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;400&display=swap">
{f'<link rel="stylesheet" href="https://use.typekit.net/{KIT}.css"><link rel="stylesheet" href="https://use.typekit.net/{KIT_CASOS}.css">' if casos else ""}{pre}
<link rel="stylesheet" href="{p}assets/eiro.css?v={VER}">
</head>'''.replace("{LD}", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')


def brand(p):
    """arriba a la izquierda: el isologo y EIROSTUDIO, cada uno con su aire"""
    return f'<span class="lockup">{logo(p, "lockup-word")}</span>'


def chrome(p, page, where):
    items = "".join(
        f'<li><a href="{p}{slug}/"{" aria-current=\"true\"" if slug == page else ""}><span class="mono">0{i+1}</span>{name}</a></li>'
        for i, (slug, name) in enumerate(NAV))
    links = "".join(
        f'<li><a href="{p}{slug}/"{" aria-current=\"page\"" if slug == page else ""}>{name}</a></li>' for slug, name in NAV)
    return f'''
<body>
<a class="skip" href="#top">Saltar al contenido</a>
<div class="gate" id="gate" role="dialog" aria-modal="true" aria-label="Acceso a Eiro">
  <div class="gate-box">
    {seal(p, "seal seal-gate", "Eiro Studio")}
    <form id="gateForm" autocomplete="off">
      <label for="gateKey" class="sr">Clave</label>
      <input id="gateKey" name="gateKey" type="password" inputmode="numeric" maxlength="4" placeholder="Clave" enterkeyhint="go">
      <button type="submit" aria-label="Entrar">→</button>
    </form>
    <p class="gate-note mono">Estamos terminando algo bueno</p>
  </div>
</div>

<header class="bar" id="barra">
  <a class="brand" href="{p or './'}" aria-label="Eiro Studio, ir al inicio">{brand(p)}</a>
  <nav class="bar-nav" aria-label="Principal"><ul>{links}</ul></nav>
  <div class="bar-right">
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú"><svg viewBox="0 0 14 14" aria-hidden="true"><circle cx="3" cy="3" r="1.6" fill="currentColor"/><circle cx="11" cy="3" r="1.6" fill="currentColor"/><circle cx="3" cy="11" r="1.6" fill="currentColor"/><circle cx="11" cy="11" r="1.6" fill="currentColor"/></svg></button>
  </div>
</header>

<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menú" hidden>
  <div class="menu-top">
    <a class="brand" href="{p or './'}" aria-label="Ir al inicio">{brand(p)}</a>
    <button class="menu-btn" id="menuClose" type="button" aria-label="Cerrar menú"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.6"/></svg></button>
  </div>
  <nav aria-label="Menú"><ul>{items}</ul></nav>
  <div class="menu-foot mono">
    <span>Buenos Aires, Argentina</span>
    {social_btns()}
  </div>
</div>
'''


SEAL_N = [0]
SEAL_P = 1668.9  # largo del óvalo por donde corre el texto (elipse de 295 × 234.5)


def seal(p, cls="seal", label=None):
    """el óvalo de la lámina de marca: EIRO STUDIO · BUENOS AIRES · ARGENTINA corre alrededor del isologo.
    Respeta la forma original (elipse de 829 × 665 con el texto sobre una elipse de 590 × 469); el texto gira siguiendo el óvalo."""
    SEAL_N[0] += 1
    i = f"seal-{SEAL_N[0]}"
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    txt = "EIRO STUDIO · BUENOS AIRES · ARGENTINA · "
    return (f'<svg class="{cls}" viewBox="0 0 829.4 665.28" {a}>'
            f'<defs><path id="{i}" d="M{414.7-295} 332.64a295 234.5 0 1 1 {2*295:g} 0a295 234.5 0 1 1 -{2*295:g} 0"/></defs>'
            f'<ellipse class="seal-bg" cx="414.7" cy="332.64" rx="414.7" ry="332.64"/>'
            f'<text class="seal-txt"><textPath href="#{i}" textLength="{2*SEAL_P:.1f}" lengthAdjust="spacing">{txt * 2}'
            f'<animate attributeName="startOffset" from="-{SEAL_P:.1f}" to="0" dur="36s" repeatCount="indefinite"/></textPath></text>'
            f'<use class="seal-iso" href="{p}img/sprite.svg#i-eiro" x="186.24" y="142.85" width="456.94" height="379.61"/></svg>')


def footer(p):
    pages = "".join(f'<a href="{p}{s}/">{n}</a>' for s, n in NAV)
    return f'''
<footer>
  <div class="foot-nav">
    <div class="foot-brand"><span class="mono">Eiro Studio™</span><p>Estudio creativo en Buenos Aires.</p>{seal(p)}</div>
    <div><span class="mono">Páginas</span><a href="{p or './'}">Inicio</a>{pages}</div>
    <div><span class="mono">Hablemos</span><a href="{WA_PROJ}" target="_blank" rel="noopener">WhatsApp{SR_WA}</a><a href="{IG}" target="_blank" rel="noopener">Instagram{SR_IG}</a><a href="{TEL}">{TEL_TXT}</a><span class="gray" style="min-height:32px;display:flex;align-items:center">Buenos Aires, Argentina</span></div>
  </div>
  <div class="foot-bottom mono">
    <span>© {date.today().year} Eiro Studio™</span>
    <span class="foot-code"><i class="barcode" aria-hidden="true"></i>Hecho en Buenos Aires</span>
    <a href="#top">Volver arriba ↑</a>
  </div>
</footer>
<a class="wa-orb" id="waOrb" href="{WA_PROJ}" target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp (se abre WhatsApp)"><span class="wa-in">{icon(WA_PATH)}</span></a>
<script src="{p}assets/eiro.js?v={VER}" defer></script>
</body>
</html>
'''


def page_head(p, crumb, title_a, title_b, lead=None, extra=""):
    lead_html = f'<p class="page-lead" data-reveal>{lead}</p>' if lead else ""
    return f'''
  <section class="page-head grid pad" aria-labelledby="t-page">
    <p class="crumb mono" data-reveal><a href="{p or './'}">Eiro</a><span aria-hidden="true">/</span>{crumb}</p>
    <h1 class="page-title" id="t-page" data-reveal><span>{title_a}</span>{f'<span class="gray">{title_b}</span>' if title_b else ""}</h1>
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
        <div class="wcard-cap"><h3 class="wcard-name">{pr["name"]}</h3><p class="wcard-sub mono">{pr["tags"]}</p></div>
      </a>'''



def services_grid():
    out = []
    for i, (sid, name, line, items) in enumerate(SERVICES):
        lis = "".join(f"<li>{x}</li>" for x in items)
        out.append(f'<article class="svc" id="{sid}" data-reveal><span class="mono">0{i+1}</span><h3>{name}</h3><p>{line}</p><ul>{lis}</ul></article>')
    return "\n      ".join(out)


def modes_html(p):
    cards = "".join(
        f'<article class="mode" data-reveal><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul>'
        f'<a class="bracket" href="{p}contacto/#formulario">Pedir propuesta</a></article>' for t, d, li in MODES)
    return f'''
  <section class="sec pad tone-monte" aria-labelledby="t-modos">
    <div class="sec-row" data-reveal><h2 class="h2" id="t-modos"><span>Cómo trabajamos</span><span class="gray">Tres formas, un mismo equipo.</span></h2></div>
    <div class="modes">{cards}</div>
  </section>'''


def steps_html():
    return "\n      ".join(f'<li class="step" data-reveal><span class="mono">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS))


def values_html():
    return "\n      ".join(f'<article class="value" data-reveal><h3>{t}</h3><p>{d}</p></article>' for t, d in VALUES)


def social_btns():
    return (f'<div class="socials"><a href="{WA_PROJ}" target="_blank" rel="noopener">{icon(WA_PATH)}<span>WhatsApp</span>{SR_WA}</a>'
            f'<a href="{IG}" target="_blank" rel="noopener">{icon(IG_PATH)}<span>Instagram</span>{SR_IG}</a></div>')


def cta_band(p, lines=("Si tu marca tiene algo para contar,", "empecemos por acá.")):
    spans = "".join(f'<span>{l}</span>' for l in lines)
    return f'''
  <section class="pad sec cta-sec" aria-labelledby="t-cta">
    <div class="cta" data-reveal>
      <p class="mono cta-kicker">Hablemos</p>
      <h2 class="cta-title" id="t-cta">{spans}</h2>
      <p class="cta-sub">Contanos qué necesitás en un minuto. Respondemos rápido y sin compromiso.</p>
      <div class="cta-actions">
        <a class="btn accent big" href="{p}contacto/#formulario">Contanos tu proyecto <span aria-hidden="true">→</span></a>
        <a class="btn ghost big" href="{WA_PROJ}" target="_blank" rel="noopener">{icon(WA_PATH)}WhatsApp{SR_WA}</a>
      </div>
    </div>
  </section>'''


def cta_inline(p, text, btn="Pedí tu propuesta"):
    """llamado a la acción en medio de una página larga"""
    return (f'<div class="cta-inline" data-reveal><p>{text}</p>'
            f'<a class="btn accent big" href="{p}contacto/#formulario">{btn} <span aria-hidden="true">→</span></a></div>')


def testimonials_html():
    if not TESTIMONIOS_REALES:  # sin testimonios reales, la sección no se muestra
        return ""
    tag = "" if TESTIMONIOS_REALES else '<span class="t-tag mono">Ejemplo</span>'
    note = "" if TESTIMONIOS_REALES else '<p class="t-note mono">Testimonios de ejemplo. Se reemplazan por los reales.</p>'
    n_t = len(TESTIMONIALS)
    slides = "".join(
        f'<figure class="tq-slide" role="group" aria-roledescription="testimonio" aria-label="{i+1} de {n_t}">'
        f'<blockquote><p>“{q}”</p></blockquote>'
        f'<figcaption><span class="tq-who"><b>{n}</b> {r.split(" · ")[0]}</span><span class="tq-org">{r.split(" · ")[-1]}</span></figcaption></figure>'
        for i, (q, n, r) in enumerate(TESTIMONIALS))
    bars = "".join(f'<i{" class=\"on\"" if i == 0 else ""}></i>' for i in range(n_t))
    return f'''
  <section class="sec pad tq-sec" data-label="Clientes" aria-labelledby="t-clientes">
    <div class="sec-row centered" data-reveal><h2 class="h2" id="t-clientes"><span>Lo que cuentan</span></h2>{note}</div>
    <div class="tq-box" data-tq data-reveal aria-roledescription="carrusel" aria-label="Testimonios">
      <div class="tq-track" tabindex="0" aria-label="Testimonios: deslizá o usá las flechas">{slides}</div>
      <div class="tq-nav">
        <button type="button" data-tq-prev aria-label="Testimonio anterior">←</button>
        <span class="tq-count" aria-live="polite"><span data-tq-n>1</span>/{n_t}</span>
        <span class="tq-bars" aria-hidden="true">{bars}</span>
        <button type="button" data-tq-next aria-label="Testimonio siguiente">→</button>
      </div>
    </div>
  </section>'''


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


# El telón de entrada se salta con movimiento reducido o si ya se vio en esta visita (se decide antes de pintar).
INTRO_HEAD = """<script>try{if(sessionStorage.getItem('eiro-intro')||matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('no-intro')}catch(e){}</script>
<noscript><style>.curtain{display:none}</style></noscript>"""


# Portada: a la izquierda la frase (con la última palabra que cambia) y los botones; a la derecha los mockups en modo GIF.
# Tocar los mockups abre el reel a pantalla completa con sonido.
MOCKUPS = [  # solo los que están completos (sin textos de relleno)
    ("07-via-publica", "Crisger: vía pública"), ("04-bolsas", "Crisger: bolsas"),
    ("05-redes", "Crisger: redes sociales"), ("06-web", "Crisger: sitio web"),
    ("08-etiquetas", "Crisger: etiquetas"),
]
REEL_REAL = False  # True cuando img/reel/reel.mp4 sea el reel de verdad: el botón pasa a decir "Ver reel"


def hero_media(p):
    imgs = "".join(
        f'<img src="{p}img/mockups/{n}-1200.webp" srcset="{p}img/mockups/{n}-600.webp 600w, {p}img/mockups/{n}-1200.webp 1200w" '
        f'sizes="(max-width:820px) 100vw, 50vw" width="1200" height="900" alt="{cap}" decoding="async"'
        f'{" class=\"on\" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>' for i, (n, cap) in enumerate(MOCKUPS))
    return f'''<div class="hero-media" data-player data-reel>
        {imgs}
        <button type="button" class="play-orb" data-play aria-haspopup="dialog"><svg class="orb-globe" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="47"/><line x1="3" y1="50" x2="97" y2="50"/><g class="m1"><ellipse cx="50" cy="50" rx="24" ry="47"/></g><g class="m2"><ellipse cx="50" cy="50" rx="24" ry="47"/></g></svg><span>{"Ver reel" if REEL_REAL else "Ver en grande"}</span></button>
        <button type="button" class="reel-pause mono" data-reel-pause aria-pressed="false">Pausar</button>
      </div>'''


# Reel a pantalla completa (provisorio, armado con los mockups; se reemplaza por img/reel/reel.mp4).
# El reel es un video provisorio armado con los mockups; se reemplaza por img/reel/reel.mp4 (el video de Matías) sin tocar nada más.
HERO_WORDS = ["la calle", "las redes", "un evento", "la web", "todos lados"]  # los lugares donde contamos una marca: calle, redes, eventos, web


def reel_player(p):
    return f'''
<div class="player" id="player" role="dialog" aria-modal="true" aria-label="Reel de Eiro Studio" hidden>
      <video class="player-video" src="{p}img/reel/reel.mp4" poster="{p}img/reel/poster.jpg" controls playsinline preload="none"></video>
      <button type="button" class="player-close" data-close aria-label="Cerrar el reel"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.4"/></svg></button>
</div>'''


# ---------- páginas ----------
def home():
    p = ""
    cards = "\n      ".join(work_card(p, pr) for pr in PUB)
    svc = "".join(f'<a href="servicios/#{sid}" data-reveal>{name}<span class="mono">0{i+1}</span></a>' for i, (sid, name, _, _) in enumerate(SERVICES))
    m0 = MOCKUPS[0][0]
    ld = head(p, "Eiro Studio | Estudio creativo en Buenos Aires",
              "Estudio creativo en Buenos Aires: identidad de marca, contenido para redes, branding de eventos y web, para marcas con algo para contar.", "",
              preload=(f"img/mockups/{m0}-1200.webp", f"img/mockups/{m0}-600.webp 600w, img/mockups/{m0}-1200.webp 1200w", "(max-width:820px) 100vw, 50vw"))
    org = open(os.path.join(ROOT, "tools", "org-ld.json"), encoding="utf-8").read().strip()  # datos del estudio para buscadores
    ld = ld.replace("</head>", '<script type="application/ld+json">' + org + '</script>\n</head>')
    body = f'''
<main id="top" tabindex="-1">
  <section class="hero" data-label="Inicio" aria-labelledby="t-hero">
    <div class="hero-copy">
      <div class="hero-mark"><i class="crop tl" aria-hidden="true"></i><i class="crop tr" aria-hidden="true"></i><i class="crop bl" aria-hidden="true"></i><i class="crop br" aria-hidden="true"></i>{seal(p, "seal seal-hero", "Eiro Studio · Buenos Aires, Argentina")}</div>
      <h1 class="hero-title" id="t-hero"><span class="hl">Contamos tu marca</span> <span class="hl">en <span class="swap" data-swap="{"|".join(HERO_WORDS)}"><span class="sr">{HERO_WORDS[0]}</span><span class="swap-vis" aria-hidden="true">{HERO_WORDS[0]}</span></span>.</span></h1>
      <p class="hero-sub">Marca, contenido y eventos para marcas con algo para contar.</p>
      <div class="hero-ctas"><a class="btn accent big" href="contacto/#formulario">Contanos tu proyecto <span aria-hidden="true">→</span></a><a class="bracket" href="trabajos/">Ver trabajos</a></div>
    </div>
  </section>

  <section class="pad reel-sec" aria-label="Reel">
    {hero_media(p)}
  </section>

  <section class="sec pad" data-label="Trabajos" aria-labelledby="t-trabajos">
    <div class="sec-row" data-reveal><h2 class="h2" id="t-trabajos"><span>Trabajos</span></h2><a class="bracket" href="trabajos/">Ver todos</a></div>
    <div class="wgrid">
      {cards}
    </div>
  </section>
{testimonials_html()}

  <section class="sec pad grid tone-paper" data-label="Servicios" aria-labelledby="t-servicios">
    <div class="svc-side" data-reveal>
      <h2 class="h2" id="t-servicios"><span>Qué hacemos</span></h2>
      <p>Por proyecto, por mes o por pieza, con un equipo armado a medida.</p>
      <a class="bracket" href="servicios/">Ver servicios</a>
    </div>
    <nav class="svc-list" aria-label="Servicios">{svc}</nav>
  </section>

{cta_band(p)}
</main>'''
    curtain = f'''
<div class="curtain" id="curtain" aria-hidden="true"><div class="ic"><div class="ic-in">{seal(p, "seal seal-big")}</div></div></div>'''
    ld = ld.replace("</head>", INTRO_HEAD + "\n</head>")
    write("index.html", ld + chrome(p, "", "Inicio") + curtain + body + reel_player(p) + footer(p))


def trabajos():
    p = "../"
    cards = "\n      ".join(work_card(p, pr) for pr in PUB)
    html = head(p, "Trabajos de branding y contenido | Eiro Studio", "Casos de Eiro Studio: identidad visual, contenido para redes y branding de eventos para marcas de Argentina.", "trabajos/") + chrome(p, "trabajos", "Trabajos") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Trabajos</span>', 'Trabajos', 'Historias que ya contamos.', None)}
  <section class="sec pad" aria-label="Proyectos">
    <div class="wgrid">
      {cards}
    </div>
    <p class="cap mono" style="margin-top:32px;color:var(--soft)">Hay más proyectos. Te los mostramos cuando hablemos.</p>
  </section>
{cta_band(p)}
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
    return f'<a class="next-plate" href="{p}contacto/#formulario"><span class="mono">Contanos tu proyecto →</span><b style="--w:8">Hablemos</b></a>'


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
    html = head(p, "Servicios: marca, contenido, eventos y web | Eiro Studio", "Identidad de marca, contenido para redes, branding de eventos y web en Buenos Aires. Por proyecto, por abono mensual o por pieza.", "servicios/",
                extra_ld=[{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
                          {"@type": "ItemList", "name": "Servicios de Eiro Studio", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "description": l, "provider": {"@id": SITE + "#estudio"}, "areaServed": "AR"}} for i, (_, n, l, _) in enumerate(SERVICES)]}]) + chrome(p, "servicios", "Servicios") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Servicios</span>', 'Servicios', 'Cuatro áreas, un mismo equipo.')}
  <section class="sec pad tone-paper" aria-label="Áreas de trabajo">
    <div class="svc-grid">
      {services_grid()}
    </div>
  </section>
{modes_html(p)}

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
    return ""


def estudio():
    p = "../"
    html = head(p, "Estudio | Eiro Studio, estudio creativo en Buenos Aires", "Eiro es un estudio creativo de Buenos Aires movido por el optimismo, el trabajo en equipo y el oficio. Contamos marcas en la calle, en redes y en eventos.", "estudio/") + chrome(p, "estudio", "Estudio") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Estudio</span>', 'Estudio', 'Chico a propósito, cerca siempre.')}

  <section class="sec pad grid table-sec" aria-labelledby="t-quien">
    {f'<div class="studio-photo">{matias_photo(p)}</div>' if matias_photo(p) else ""}
    <div class="founder{"" if matias_photo(p) else " solo"}" data-reveal>
      <h2 class="h2" id="t-quien"><span>Quién está detrás</span><span class="gray">Matías Gaiteiro.</span></h2>
      <p class="founder-bio">Lo dirige Matías Gaiteiro, diseñador multimedial. Hace más de diez años que diseñamos marcas, coordinamos equipos de redes y llevamos áreas de marketing.</p>
      <p class="founder-text">Venimos de las relaciones públicas y se nota: casi todos nuestros clientes llegaron por vínculos de años, y se quedaron. Cada proyecto lo encaramos de cerca, con un equipo armado a medida.</p>
      <dl class="founder-facts">
        <div><dt class="mono">Oficio</dt><dd>Más de 10 años</dd></div>
        <div><dt class="mono">Hace</dt><dd>Diseño, marketing y redes</dd></div>
        <div><dt class="mono">Base</dt><dd>Buenos Aires</dd></div>
      </dl>
      {social_btns()}
    </div>
  </section>

  <section class="sec pad grid tone-paper" aria-labelledby="t-valores">
    <h2 class="values-statement" id="t-valores" data-reveal><span>Nuestros valores.</span><span class="gray">Con optimismo.</span><span class="gray">En equipo.</span><span class="gray">Con oficio.</span></h2>
    <div class="values">
      {values_html()}
    </div>
  </section>

  <section class="sec pad grid tone-monte" aria-labelledby="t-proceso">
    <h2 class="h2" id="t-proceso" data-reveal style="grid-column:1/-1"><span>Cómo trabajamos</span><span class="gray">Cuatro pasos, cero sorpresas.</span></h2>
    <ol class="steps">
      {steps_html()}
    </ol>
  </section>
{cta_band(p)}
</main>''' + footer(p)
    write("estudio/index.html", html)


# Formulario breve: casi todo se elige tocando; al enviar arma el mensaje y abre WhatsApp con el estudio.
BRIEF_NEEDS = ["Identidad de marca", "Redes y contenido", "Branding de un evento", "Web o app", "Fotos y video", "Todavía no sé"]
BRIEF_WHEN = ["Lo antes posible", "En uno o dos meses", "Sin apuro"]
BRIEF_FILL = ["Estoy por lanzar una marca nueva.", "Quiero renovar la imagen de mi marca.", "Tengo un evento en camino.", "Necesito contenido todos los meses."]


def brief_form():
    needs = "".join(f'<label class="chip"><input type="checkbox" name="necesito" value="{x}"><span>{x}</span></label>' for x in BRIEF_NEEDS)
    when = "".join(f'<label class="chip"><input type="radio" name="cuando" value="{x}"><span>{x}</span></label>' for x in BRIEF_WHEN)
    fill = "".join(f'<button type="button" class="chip fill" data-fill="{x}">{x}</button>' for x in BRIEF_FILL)
    return f'''
  <section class="sec pad brief-sec" id="formulario" aria-labelledby="t-brief">
    <form class="brief" id="brief" data-wa="{WA.split("/")[-1]}" novalidate data-reveal>
      <h2 class="h2" id="t-brief"><span>Contanos tu proyecto</span><span class="gray">Toma un minuto. Te respondemos por WhatsApp.</span></h2>
      <fieldset><legend><span class="n">01</span>¿Qué necesitás? <span class="opt">Podés elegir varias</span></legend><div class="chips">{needs}</div></fieldset>
      <fieldset><legend><span class="n">02</span>¿Para cuándo?</legend><div class="chips">{when}</div></fieldset>
      <fieldset><legend><span class="n">03</span>¿Quién sos?</legend>
        <div class="fields">
          <label class="field"><span>Tu nombre</span><input type="text" name="nombre" autocomplete="given-name" required aria-describedby="brief-err" enterkeyhint="next"></label>
          <label class="field"><span>Tu marca o proyecto <span class="opt">Opcional</span></span><input type="text" name="marca" autocomplete="organization" enterkeyhint="next"></label>
        </div>
      </fieldset>
      <fieldset><legend><span class="n">04</span>Contanos un poco más <span class="opt">Opcional · tocá una idea para empezar</span></legend>
        <div class="chips">{fill}</div>
        <label class="field"><span class="sr">Mensaje</span><textarea name="mensaje" rows="3" placeholder="Lo que quieras sumar"></textarea></label>
      </fieldset>
      <p class="brief-err" id="brief-err" role="alert"></p>
      <div class="brief-send"><button type="submit" class="cta-link">Enviar por WhatsApp <span class="arr" aria-hidden="true">→</span></button><span class="mono">Se abre WhatsApp con tu mensaje listo</span></div>
    </form>
  </section>'''


def contacto():
    p = "../"
    html = head(p, "Contacto: pedí tu propuesta | Eiro Studio", "Contanos tu proyecto en un minuto y te respondemos por WhatsApp. Eiro Studio, estudio creativo en Buenos Aires.", "contacto/") + chrome(p, "contacto", "Contacto") + f'''
<main id="top" tabindex="-1">
{page_head(p, '<span>Contacto</span>', 'Contacto', 'Hagamos algo bueno juntos.', None)}
{brief_form()}
  <section class="sec pad grid table-sec tone-monte" aria-label="Otras formas de contacto">
    <div class="hello" data-reveal>
      <h2 class="h2"><span>Otras formas</span><span class="gray">Si preferís escribir directo.</span></h2>
      {social_btns()}
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
