# 🔶 Esquadrão Google Ads

> Crie o seu **MCC** e o **acesso de API do Google Ads** (OAuth + developer token) pra operar
> campanhas pelo Claude Code: ler relatórios, criar e otimizar anúncios, subir conversões.

Template — gere a sua cópia e instale com o Claude Code, sem programar.

## 🚀 Como começar (3 passos)

1. **`Use this template`** → `Create a new repository`.
2. **Baixe:** `git clone` + `cd`. (Windows? [Tutorial Windows](docs/windows.md).)
3. **Abra o Claude Code e diga `instalar`** (`claude` → **`instalar`**).
   O Claude te guia pelo MCC + Google Cloud e roda o teste. Aula em [`aula/roteiro.md`](aula/roteiro.md).

## ✅ Pré-requisitos

- Conta **Google Ads MCC** (Manager) — ou criamos uma no processo.
- Acesso ao **Google Cloud Console** (mesma conta Google).
- `python3` + `pip install google-ads google-auth-oauthlib`.

## ⏳ Importante: o prazo do Google

O **Basic Access** do developer token leva **~3 dias** de aprovação. A **leitura** já funciona
antes (você valida tudo com o smoke test); a **escrita** (criar/editar campanha) só depois.
Comece a solicitação **logo no primeiro dia** pra não travar.

## 🧩 O que você instala

- **Developer Token** no MCC + solicitação de Basic Access (com modelo de design doc).
- **OAuth** no Google Cloud (client Desktop) + **refresh token** via navegador.
- **Smoke test** que valida as 4 credenciais e lista suas contas.

---

🤖 Feito com [Claude Code](https://claude.com/claude-code) · método **ConsultorIA**
