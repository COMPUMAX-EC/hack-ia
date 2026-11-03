# FINOVA 🦊 · IA para licitaciones y crédito PYME

**Innovando hoy, transformando finanzas.** FINOVA es la propuesta de nuestro equipo para una hackatón de
inteligencia artificial en finanzas. Resuelve dos problemas del sector financiero de Ecuador:

1. **Licitaciones inteligentes:** los procesos de licitación pública son lentos y propensos a errores. FINOVA
   analiza los documentos automáticamente, detecta riesgos y compara ofertas para ahorrar tiempo al evaluador.
2. **Evaluación crediticia inclusiva para PYMEs:** muchas pequeñas empresas no acceden a crédito porque no tienen
   historial bancario. FINOVA calcula un **score crediticio con datos alternativos**: presencia digital,
   referencias comerciales, actividad financiera y datos de comportamiento.

**Demo en línea:** https://hack-ia.vercel.app

> Es un prototipo: los análisis de NLP y Machine Learning están **simulados** en la interfaz para mostrar el flujo.

## Qué muestra la demo

- `/` — presentación de FINOVA, misión y soluciones.
- `/reto1` — licitaciones: tipo de documento, análisis automático, detección de riesgos, comparación inteligente.
- `/reto2` — score crediticio IA para PYMEs y su impacto social.
- `/equipo` — el equipo: Geovanny Basantes, Edison López y Jaime Pergueza.

Marca: azul oscuro `#0D3B66`, verde azulado `#1FAA59`, naranja `#F25C05` y gris claro `#E1E5F2`, con **Byte**, el
zorro mascota.

## Detalles técnicos

| Capa | Tecnología |
|---|---|
| Framework | Next.js 15 (App Router) + React 19 |
| Lenguaje | TypeScript |
| Estilos | CSS propio con sistema de diseño |
| Íconos | lucide-react |
| Despliegue | Vercel |

```
src/app/              páginas: inicio, reto1, reto2, equipo
src/components/       Header, Layout, ByteMascot
public/               logo, fotos del equipo
```

### Ejecutar localmente

```bash
npm install
npm run dev      # http://localhost:3000
```

## In English

FINOVA is a hackathon prototype for AI in finance: automatic analysis of public tender documents, and an inclusive
credit score for SMEs based on alternative data. AI results are simulated in the UI. Next.js 15 + React 19 on Vercel.

## Licencia

El código está bajo licencia [MIT](LICENSE). Las fotos del equipo y la marca FINOVA no forman parte de la licencia.
