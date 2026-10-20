// Convierte los mockups (tools/mockups/src/*.html, 1200×900) en imágenes PNG para la portada.
// Uso: node tools/mockups/render.mjs [ruta de playwright]
import { readdirSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const pw = process.argv[2] || 'playwright';
const { chromium } = await import(pw.startsWith('/') ? pathToFileURL(pw).href : pw);
const out = join(here, 'png'); mkdirSync(out, { recursive: true });
const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1.5 });
for (const f of readdirSync(join(here, 'src')).filter(f => f.endsWith('.html')).sort()) {
  await pg.goto(pathToFileURL(join(here, 'src', f)).href, { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  await pg.screenshot({ path: join(out, f.replace('.html', '.png')), clip: { x: 0, y: 0, width: 1200, height: 900 } });
  console.log('ok', f);
}
await b.close();
