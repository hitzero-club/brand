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
│   ├── logo.png        # Logo completo 400×400 (fondo negro)
│   └── app-icon-512.png  # Ícono PWA
└── .github/workflows/  # Deploy automático a GitHub Pages
```

## Desarrollo local

Abrí `index.html` en el navegador. No necesita servidor ni build.

## Assets disponibles

Los assets de marca viven en `/assets/` (copiados de `workers/platform/public/` del monorepo). Aún no existe versión vectorial (SVG) del logo.

Los colores y la tipografía de la plataforma salen de `packages/ui/globals.css` del monorepo; esta guía los refleja.
