// Dibuja la G de Neulis Cursive Bold grande (tools/icons/g.html) y la guarda en tools/icons/g-big.png.
// Necesita un servidor en http://localhost:8765 sirviendo la raíz del repo (el kit de Adobe solo carga en localhost).
import { pathToFileURL } from 'node:url';
const pw = process.argv[2] || 'playwright';
const { chromium } = await import(pw.startsWith('/') ? pathToFileURL(pw).href : pw);
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 2000, height: 2000 } });
await pg.goto('http://localhost:8765/tools/icons/g.html', { waitUntil: 'networkidle' });
await pg.evaluate(() => document.fonts.ready);
const ok = await pg.evaluate(() => document.fonts.check('700 100px "neulis-cursive"'));
if (!ok) { console.error('Neulis Cursive no cargó: no se generan íconos'); process.exit(1); }
await pg.screenshot({ path: 'tools/icons/g-big.png' });
await b.close(); console.log('ok');
