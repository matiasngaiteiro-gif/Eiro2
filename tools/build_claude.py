"""/pruebaclaude: la web de Eiro con la estructura, el estilo y el tono de una app de chat
(barra lateral, saludo con caja para escribir y cada página como una conversación).
Usa los mismos datos que build.py; estilos en assets/eiro-claude.css y comportamiento en assets/eiro.js + assets/eiro-claude.js."""
import build as B

DIR = "pruebaclaude"

# íconos de línea, 20 px
I = {
    "inicio": '<path d="M3 9.5 10 4l7 5.5V16a1 1 0 0 1-1 1h-3.5v-4.5h-5V17H4a1 1 0 0 1-1-1z"/>',
    "trabajos": '<rect x="3" y="3" width="6" height="6" rx="1.2"/><rect x="11" y="3" width="6" height="6" rx="1.2"/><rect x="3" y="11" width="6" height="6" rx="1.2"/><rect x="11" y="11" width="6" height="6" rx="1.2"/>',
    "servicios": '<path d="m10 3 7 3.5-7 3.5-7-3.5z"/><path d="m3 10 7 3.5 7-3.5"/><path d="m3 13.5 7 3.5 7-3.5"/>',
    "estudio": '<circle cx="10" cy="7" r="3.2"/><path d="M4 17c.8-3 3.2-4.6 6-4.6s5.2 1.6 6 4.6"/>',
    "contacto": '<path d="M4 4h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H9l-4 3v-3H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z"/>',
    "mas": '<path d="M10 4v12M4 10h12"/>',
    "menu": '<path d="M3 6h14M3 10h14M3 14h9"/>',
    "cerrar": '<path d="m5 5 10 10M15 5 5 15"/>',
    "enviar": '<path d="M10 16V4M5 9l5-5 5 5"/>',
    "flecha": '<path d="M5 10h10M11 6l4 4-4 4"/>',
    "doc": '<path d="M6 3h6l4 4v10a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M12 3v4h4"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 20 20" aria-hidden="true" focusable="false">{I[name]}</svg>'


def iso(p, cls="isologo"):
    return B.iso(p, cls)


NAV = [("", "Inicio", "inicio"), ("trabajos", "Trabajos", "trabajos"), ("servicios", "Servicios", "servicios"),
       ("estudio", "Estudio", "estudio"), ("contacto", "Contacto", "contacto")]


def page_head(p, q, title, desc, path):
    """p: hasta la raíz del sitio (archivos compartidos) · q: hasta la raíz de /pruebaclaude"""
    h = B.head(p, title, desc, path)
    h = h.replace(f'<link rel="stylesheet" href="{p}assets/eiro.css?v={B.VER}">',
                  f'<link rel="stylesheet" href="{p}assets/eiro-claude.css?v={VER}">')
    h = h.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    h = h.replace('<meta name="theme-color" content="#021719">', '<meta name="theme-color" content="#F4F2EC">')
    return h


VER = B._ver("assets/eiro-claude.css", "assets/eiro-claude.js", "assets/eiro.js")


def side(p, q, cur):
    nav = "".join(
        f'<li><a href="{q}{s + "/" if s else ""}"{" aria-current=\"page\"" if s == cur else ""}>{ic(icn)}<span>{n}</span></a></li>'
        for s, n, icn in NAV)
    recent = "".join(f'<li><a href="{q}trabajos/{pr["slug"]}/"{" aria-current=\"page\"" if cur == pr["slug"] else ""}>{pr["name"]}</a></li>' for pr in B.PUB)
    return f'''
<a class="skip" href="#top">Saltar al contenido</a>
<div class="gate" id="gate" role="dialog" aria-modal="true" aria-label="Acceso a Eiro">
  <div class="gate-box">
    {iso(p, "isologo gate-iso")}
    <form id="gateForm" autocomplete="off">
      <label for="gateKey" class="sr">Clave</label>
      <input id="gateKey" name="gateKey" type="password" inputmode="numeric" maxlength="4" placeholder="Clave" enterkeyhint="go">
      <button type="submit" aria-label="Entrar">→</button>
    </form>
    <p class="gate-note mono">Estamos terminando algo bueno</p>
  </div>
</div>

<div class="topbar">
  <button class="icon-btn" type="button" data-side-open aria-controls="side" aria-expanded="false" aria-label="Abrir menú">{ic("menu")}</button>
  <a class="top-iso" href="{q}" aria-label="Eiro Studio, ir al inicio">{iso(p)}</a>
  <a class="icon-btn" href="{q}contacto/" aria-label="Nuevo proyecto">{ic("mas")}</a>
</div>
<div class="scrim" data-side-close></div>

<header class="side" id="side">
  <div class="side-top">
    <a class="side-iso" href="{q}" aria-label="Eiro Studio, ir al inicio">{iso(p)}</a>
    <button class="icon-btn side-x" type="button" data-side-close aria-label="Cerrar menú">{ic("cerrar")}</button>
  </div>
  <a class="new" href="{q}contacto/"><span class="new-plus">{ic("mas")}</span>Nuevo proyecto</a>
  <nav aria-label="Principal"><ul class="side-nav">{nav}</ul></nav>
  <p class="side-label">Trabajos recientes</p>
  <ul class="side-recent">{recent}</ul>
  <div class="side-foot">
    <span class="who-av">{iso(p)}</span>
    <span class="who"><b>Eiro Studio</b><span>Buenos Aires</span></span>
    <a class="icon-btn" href="{B.WA_PROJ}" target="_blank" rel="noopener" aria-label="WhatsApp (se abre WhatsApp)">{B.icon(B.WA_PATH)}</a>
    <a class="icon-btn" href="{B.IG}" target="_blank" rel="noopener" aria-label="Instagram (se abre Instagram)">{B.icon(B.IG_PATH)}</a>
  </div>
</header>
'''


def foot(p):
    return f'''
<script src="{p}assets/eiro.js?v={VER}" defer></script>
<script src="{p}assets/eiro-claude.js?v={VER}" defer></script>
</body>
</html>
'''


def chat_head(q, title):
    """barra de la conversación: título y botón para hablar"""
    return f'''<div class="chat-bar"><h1 class="chat-title" id="t-page">{title}</h1><a class="pill-btn" href="{q}contacto/">Hablemos</a></div>'''


def ask(text):
    return f'<div class="msg-user"><p>{text}</p></div>'


def answer(p, html):
    return f'<div class="msg-ai"><span class="ai-av">{iso(p)}</span><div class="ai-body">{html}</div></div>'


def reply_box(q, text="Contanos tu proyecto…"):
    """caja para escribir al pie de cada conversación: lleva al formulario"""
    return f'''<div class="reply"><a class="reply-box" href="{q}contacto/"><span>{text}</span><span class="send">{ic("enviar")}</span></a>
  <p class="reply-note">Te respondemos por WhatsApp, rápido y sin compromiso.</p></div>'''


def card(p, q, pr):
    """trabajo como tarjeta de archivo (imagen, nombre y rubro)"""
    if pr["img"]:
        n, alt, w, h, st = pr["img"]
        media = B.pic(p, n, "(max-width:700px) 100vw, 360px", alt, w, h, st)
    else:
        zn, zalt = pr["zoom"]
        media = f'<img src="{p}img/gen/{zn}-900.webp" alt="{zalt}" loading="lazy" decoding="async">'
    return (f'<a class="art" href="{q}trabajos/{pr["slug"]}/"><span class="art-media">{media}</span>'
            f'<span class="art-txt"><b>{pr["name"]}</b><span>{pr["tags"]}</span></span><span class="art-go">{ic("flecha")}</span></a>')


def composer(full=False):
    needs = "".join(f'<label class="chip"><input type="checkbox" name="necesito" value="{x}"><span>{x}</span></label>' for x in B.BRIEF_NEEDS)
    when = "".join(f'<label class="chip"><input type="radio" name="cuando" value="{x}"><span>{x}</span></label>' for x in B.BRIEF_WHEN)
    extra = f'''
      <fieldset class="opts"><legend>¿Para cuándo?</legend><div class="chips">{when}</div></fieldset>''' if full else ""
    marca = '<label class="mini"><span class="sr">Tu marca o proyecto (opcional)</span><input type="text" name="marca" autocomplete="organization" placeholder="Tu marca (opcional)"></label>' if full else '<input type="hidden" name="marca" value="">'
    return f'''
    <form class="brief-wrap" id="brief" data-wa="{B.WA.split("/")[-1]}" novalidate>
      <div class="composer">
        <label class="sr" for="msg">Contanos tu proyecto</label>
        <textarea id="msg" name="mensaje" rows="{3 if full else 2}" placeholder="Contanos tu proyecto…"></textarea>
        <div class="comp-row">
          <label class="mini"><span class="sr">Tu nombre</span><input type="text" name="nombre" autocomplete="given-name" required aria-describedby="brief-err" placeholder="Tu nombre"></label>
          {marca}
          <button type="submit" class="send" aria-label="Enviar por WhatsApp">{ic("enviar")}</button>
        </div>
      </div>
      <p class="brief-err" id="brief-err" role="alert"></p>
      <fieldset class="opts"><legend>¿Qué necesitás?</legend><div class="chips">{needs}</div></fieldset>{extra}
    </form>'''


def doc(p, q, cur, title, desc, path, body, depth):
    html = page_head(p, q, title, desc, path) + "\n<body>" + side(p, q, cur) + f'''
<main id="top" tabindex="-1" class="main">
{body}
</main>''' + foot(p)
    B.write(f"{DIR}/{path}index.html", html)


# ---------- páginas ----------
def home():
    p, q = "../", ""
    cards = "".join(card(p, q, pr) for pr in B.PUB)
    body = f'''
  <section class="hello" aria-labelledby="t-page">
    <h1 class="greet" id="t-page"><span class="greet-iso">{iso(p)}</span><span><span data-greet>Hola</span>. ¿Qué historia contamos hoy?</span></h1>
    {composer()}
    <p class="hello-note">Creamos marcas, contenido, eventos y webs desde Buenos Aires. Contanos qué tenés en mente y seguimos por WhatsApp.</p>
  </section>
  <section class="recent" aria-labelledby="t-rec">
    <div class="recent-head"><h2 id="t-rec">Trabajos recientes</h2><a href="trabajos/">Ver todos</a></div>
    <div class="arts">{cards}</div>
  </section>'''
    doc(p, q, "", "Eiro Studio | Estudio creativo en Buenos Aires", "Estudio creativo en Buenos Aires: marca, contenido, eventos y web.", "", body, 1)


def trabajos():
    p, q = "../../", "../"
    cards = "".join(card(p, q, pr) for pr in B.PUB)
    body = f'''
  {chat_head(q, "Trabajos")}
  <div class="thread">
    {ask("¿Qué hicieron hasta ahora?")}
    {answer(p, f'<p>Estos son algunos de los proyectos que ya contamos. Tocá uno para ver cómo lo pensamos.</p><div class="arts">{cards}</div><p>Hay más. Te los mostramos cuando hablemos.</p>')}
  </div>
  {reply_box(q, "¿Querés algo así para tu marca?")}'''
    doc(p, q, "trabajos", "Trabajos | Eiro Studio", "Casos de Eiro Studio: identidad, contenido y branding de eventos.", "trabajos/", body, 2)


def caso(pr):
    p, q = "../../../", "../../"
    zn, zalt = pr["zoom"]
    gal = "".join(B.gen_pic(p, n, alt, "(max-width:700px) 100vw, 340px", cls="shot") for n, alt in pr["gallery"])
    deliver = "".join(f"<li>{x}</li>" for x in pr["deliver"])
    meta = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in pr["meta"])
    i = B.PUB.index(pr)
    nxt = B.PUB[(i + 1) % len(B.PUB)]
    lead = pr["lead"].replace('<span class="gray">', '<span class="soft">')
    body = f'''
  {chat_head(q, pr["name"])}
  <div class="thread">
    {ask(f'Contame de {pr["name"]}.')}
    {answer(p, f"""<p class="lead">{lead}</p>
      {B.gen_pic(p, zn, zalt, "(max-width:760px) 100vw, 720px", cls="shot wide")}
      <dl class="meta">{meta}</dl>
      <h3>El desafío</h3><p>{pr["challenge"]}</p>
      <h3>Lo que hicimos</h3><p>{pr["did"]}</p>
      <h3>Entregamos</h3><ul>{deliver}</ul>
      <div class="shots">{gal}</div>""")}
    {ask("¿Qué más hicieron?")}
    {answer(p, f'<p>Seguí con este:</p><div class="arts">{card(p, q, nxt)}</div>')}
  </div>
  {reply_box(q, "¿Te gustaría algo así para tu marca?")}'''
    doc(p, q, pr["slug"], f'{pr["name"]} | Trabajos | Eiro Studio', f'{pr["name"]}: {pr["sub"]}', f'trabajos/{pr["slug"]}/', body, 3)


def servicios():
    p, q = "../../", "../"
    svc = "".join(f'<h3>{n}</h3><p>{l}</p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>' for _, n, l, items in B.SERVICES)
    rows = "".join(f'<tr><th scope="row">{t}</th><td>{d}</td><td>{" · ".join(li)}</td></tr>' for t, d, li in B.MODES)
    faq = "".join(ask(qq) + answer(p, f"<p>{a}</p>") for qq, a in B.FAQ)
    body = f'''
  {chat_head(q, "Servicios")}
  <div class="thread">
    {ask("¿Qué hacen?")}
    {answer(p, f'<p>Trabajamos en cuatro áreas, con un mismo equipo:</p>{svc}')}
    {ask("¿Y cómo trabajan?")}
    {answer(p, f'<p>De tres formas. Elegís la que te sirve:</p><div class="table"><table><thead><tr><th>Forma</th><th>Para qué</th><th>Incluye</th></tr></thead><tbody>{rows}</tbody></table></div>')}
    {faq}
  </div>
  {reply_box(q)}'''
    doc(p, q, "servicios", "Servicios | Eiro Studio", "Marca, contenido, eventos y web. Por proyecto, por abono mensual o por pieza.", "servicios/", body, 2)


def estudio():
    p, q = "../../", "../"
    steps = "".join(f"<li><b>{t}.</b> {d}</li>" for t, d in B.STEPS)
    vals = "".join(f"<li><b>{t}.</b> {d}</li>" for t, d in B.VALUES)
    body = f'''
  {chat_head(q, "Estudio")}
  <div class="thread">
    {ask("¿Quiénes son?")}
    {answer(p, '<p class="lead">Un estudio chico a propósito, y cerca siempre.</p><p>Lo dirige Matías Gaiteiro, diseñador multimedial. Hace más de diez años que diseñamos marcas, coordinamos equipos de redes y llevamos áreas de marketing.</p><p>Venimos de las relaciones públicas y se nota: casi todos nuestros clientes llegaron por vínculos de años, y se quedaron. Cada proyecto lo encaramos de cerca, con un equipo armado a medida.</p><dl class="meta"><div><dt>Oficio</dt><dd>Más de 10 años</dd></div><div><dt>Hacemos</dt><dd>Diseño, marketing y redes</dd></div><div><dt>Base</dt><dd>Buenos Aires</dd></div></dl>')}
    {ask("¿Cómo es trabajar con ustedes?")}
    {answer(p, f'<p>En cuatro pasos, sin sorpresas:</p><ol>{steps}</ol><p>Y con tres cosas que no negociamos:</p><ul>{vals}</ul>')}
  </div>
  {reply_box(q, "Contanos de tu marca…")}'''
    doc(p, q, "estudio", "Estudio | Eiro Studio", "Eiro es un estudio creativo de Buenos Aires.", "estudio/", body, 2)


def contacto():
    p, q = "../../", "../"
    body = f'''
  <section class="hello" aria-labelledby="t-page">
    <h1 class="greet" id="t-page"><span class="greet-iso">{iso(p)}</span><span>Contanos tu proyecto.</span></h1>
    {composer(full=True)}
    <p class="hello-note">Al enviar se abre WhatsApp con tu mensaje listo. Te respondemos rápido.</p>
    <div class="ways">
      <a class="way" href="{B.WA_PROJ}" target="_blank" rel="noopener">{B.icon(B.WA_PATH)}<span><b>WhatsApp</b><span>{B.TEL_TXT}</span></span></a>
      <a class="way" href="{B.IG}" target="_blank" rel="noopener">{B.icon(B.IG_PATH)}<span><b>Instagram</b><span>{B.IG_TXT}</span></span></a>
    </div>
  </section>'''
    doc(p, q, "contacto", "Contacto | Eiro Studio", "Contanos tu proyecto y te respondemos por WhatsApp.", "contacto/", body, 2)


def run():
    home(); trabajos(); servicios(); estudio(); contacto()
    for pr in B.PUB:
        caso(pr)
