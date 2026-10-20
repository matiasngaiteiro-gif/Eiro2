# Mockups de la portada

Los diez mockups que pasan en modo GIF en la portada.

- `src/` — cada mockup como HTML de 1200×900 (copiados del lienzo "Crisger · 10 mockups de marca").
- `assets/` — los logos que usan.
- Al subir un cambio en `src/`, el workflow **Renderizar mockups** los convierte en imágenes
  (`img/mockups/<nombre>-1200.webp` y `-600.webp`) con las tipografías reales.
- El orden y los textos que se ven en la portada están en `MOCKUPS`, en `tools/build.py`.

Para sumar mockups de otra marca: agregá su HTML en `src/` (o directamente las imágenes en
`img/mockups/` con el mismo formato de nombre) y sumalo a `MOCKUPS`.
