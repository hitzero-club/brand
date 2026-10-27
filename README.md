# HitZero Brand Guide

Guía de marca oficial de HitZero. Identidad, logo, paleta de colores, tipografía, tono de voz y variables CSS/Tailwind.

## Stack

- HTML + CSS + vanilla JS
- Zero build step
- Deploy: GitHub Pages

## Estructura

```
├── index.html          # Brand guide (single page)
├── assets/             # Logo y recursos de marca
│   ├── logo/           # Set de logo HZ vigente (SVG + PNG)
│   ├── logo.png        # Logo anterior (escudo), se conserva como referencia
│   └── app-icon-512.png  # Ícono anterior (escudo), se conserva como referencia
├── source/
│   └── build_logo.py   # Genera los SVG de assets/logo/
└── .github/workflows/  # Deploy automático a GitHub Pages
```

## Desarrollo local

Abrí `index.html` en el navegador. No necesita servidor ni build.

## Assets disponibles

Los assets de marca viven en `/assets/`.

**Logo vigente (`assets/logo/`)**

- `hitzero-logo.svg` / `.png` — lockup horizontal para fondos claros.
- `hitzero-logo-dark.svg` / `.png` — lockup en blanco para fondos oscuros.
- `hitzero-logo-mono.svg` — una tinta (uniformes, bordado, sellos).
- `hitzero-mark.svg` / `.png`, `hitzero-mark-dark.svg`, `hitzero-mark-mono.svg` — monograma HZ solo.
- `hitzero-wordmark.svg` — solo el nombre (HITZERO .club).
- `hitzero-app-icon.svg` y `hitzero-app-icon-{1024,512,180}.png` — ícono de app (monograma blanco sobre cuadrado negro, sin máscara de esquinas).
- `hitzero-favicon.svg` y `hitzero-favicon-32.png` — favicon.

**Logo anterior:** `assets/logo.png` y `assets/app-icon-512.png` (escudo), se conservan como referencia.

**Regenerar los SVG** (desde la raíz del repo; la fuente Sora, SIL OFL 1.1, se descarga en `source/.cache/` la primera vez):

```bash
uv run --no-project --with shapely --with fonttools --with uharfbuzz \
    python source/build_logo.py
```

**Renderizar los PNG** desde los SVG con VectorCraft:

```bash
vectorcraft-cli convert <archivo>.svg <archivo>.png --scale N
```

Los colores y la tipografía de la plataforma salen de `packages/ui/globals.css` del monorepo; esta guía los refleja.
