# Quiz Negócio.IA — Funil Low Ticket

Funil de quiz para diagnóstico do perfil de empreendedor digital.
Promessa: **R$5K a R$15K/mês vendendo sites que a IA cria em 10 minutos.**

Stack: Vite + React 18 + TypeScript + TailwindCSS + shadcn/ui + react-router-dom.

---

## Rodar local

```bash
cd "Funil Low Ticket Quiz NegocioIA"
npm install
npm run dev
```

Abre em `http://localhost:8080`.

## Build de produção

```bash
npm run build
npm run preview   # opcional: testa o build local
```

Saída em `dist/`.

---

## Deploy na Cloudflare Pages

### Opção A — Via dashboard (mais simples)

1. Faça push deste diretório para um repo Git (GitHub, GitLab, Bitbucket).
2. No dashboard Cloudflare Pages → **Create a project** → **Connect to Git**.
3. Configurações de build:
   - **Framework preset:** None (ou Vite)
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory:** caminho até esta pasta no repo (ex: `Funil Low Ticket Quiz NegocioIA`)
   - **Node version:** definir variável `NODE_VERSION = 20`
4. Após o primeiro deploy, vincule o domínio `SEU-DOMINIO.com` em **Custom domains**.

### Opção B — Via Wrangler CLI

```bash
npm install -g wrangler
wrangler login
npm run build
wrangler pages deploy dist --project-name quiz-negocio-ia
```

### SPA routing
O arquivo `public/_redirects` já está configurado com `/* /index.html 200` — Cloudflare Pages
serve qualquer rota como o `index.html` para o React Router funcionar.

---

## Integração com CRM Funnels (próximo passo)

O `LeadCaptureScreen.tsx` tem um TODO marcado para o webhook.
Quando for plugar no CRM Funnels, adicionar variável de ambiente no painel da Cloudflare:

```
VITE_GHL_WEBHOOK_URL=https://services.leadconnectorhq.com/hooks/...
```

E descomentar o bloco `fetch` em `src/components/quiz/LeadCaptureScreen.tsx`.

---

## Estrutura

```
src/
├── App.tsx               # Router + providers
├── main.tsx              # Entrypoint
├── index.css             # Tailwind + tokens (tema dark verde)
├── pages/
│   ├── Index.tsx         # Quiz state machine
│   ├── Dashboard.tsx     # Stub admin (placeholder)
│   └── NotFound.tsx      # 404
├── components/
│   ├── ui/               # shadcn/ui mínimo (button, input, etc)
│   └── quiz/
│       ├── EntranceScreen.tsx
│       ├── QuestionScreen.tsx
│       ├── LeadCaptureScreen.tsx
│       └── ResultScreen.tsx
├── data/
│   └── quizData.ts       # 8 perguntas + lógica de 3 perfis (Pioneiro/Estrategista/Construtor)
├── lib/
│   └── utils.ts          # cn() helper
└── hooks/                # vazio por enquanto
```

## Customização rápida

- **Texto das perguntas:** `src/data/quizData.ts` → array `quizQuestions`
- **Faixas de pontuação dos perfis:** `src/data/quizData.ts` → função `getProfileType`
- **Copy dos resultados:** `src/data/quizData.ts` → objeto `profileDescriptions`
- **Cores e visual:** `src/index.css` (variáveis CSS HSL) e `tailwind.config.ts`
- **Hero da entrada:** `src/components/quiz/EntranceScreen.tsx`

---

Construído por Alex Priete · ConsultorIA · Sociedade Secreta dos Consultores de IA
