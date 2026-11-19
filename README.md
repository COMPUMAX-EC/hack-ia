# FINOVA 🦊 · AI for public tenders and SME credit

🇬🇧 **English** · 🇪🇨 [Español](README.es.md)

**Innovating today, transforming finance.** FINOVA is our team's proposal for an AI-in-finance hackathon. It tackles
two problems in Ecuador's financial sector:

1. **Smart tenders:** public tender processes are slow and error-prone. FINOVA analyzes the documents automatically,
   detects risks and compares bids to save the evaluator time.
2. **Inclusive credit scoring for SMEs:** many small businesses cannot get credit because they have no banking
   history. FINOVA computes a **credit score from alternative data**: digital presence, trade references, financial
   activity and behavioral data.

**Live demo:** https://hack-ia.vercel.app (in Spanish)

> It is a prototype: the NLP and machine-learning analyses are **simulated** in the interface to show the flow.

## What the demo shows

- `/` — FINOVA introduction, mission and solutions.
- `/reto1` — tenders: document type, automatic analysis, risk detection, smart comparison.
- `/reto2` — AI credit score for SMEs and its social impact.
- `/equipo` — the team: Geovanny Basantes, Edison López and Jaime Pergueza.

Brand: dark blue `#0D3B66`, teal green `#1FAA59`, orange `#F25C05` and light grey `#E1E5F2`, with **Byte**, the fox
mascot.

## Technical details

| Layer | Technology |
|---|---|
| Framework | Next.js 15 (App Router) + React 19 |
| Language | TypeScript |
| Styling | Custom CSS with a design system |
| Icons | lucide-react |
| Deployment | Vercel |

```
src/app/              pages: home, reto1, reto2, equipo
src/components/       Header, Layout, ByteMascot
public/               logo, team photos
```

### Run locally

```bash
npm install
npm run dev      # http://localhost:3000
```

## License

The code is under the [MIT](LICENSE) license. The team photos and the FINOVA brand are not covered by the license.
