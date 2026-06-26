# 🔗 Integração CRM Funnels

> Conecta o seu **CRM Funnels** ao Claude Code por API. A partir daí o Claude trabalha
> dentro do seu CRM: lê e cria contatos, responde conversas, move oportunidades no funil
> e publica nas redes — tudo validado antes de gravar qualquer credencial.

Template — você gera a sua cópia e instala com o Claude Code, sem programar.

## 🚀 Como começar (3 passos)

1. **`Use this template`** (botão verde no topo) → `Create a new repository`.
2. **Baixe:** `git clone` do seu repo + `cd`. (Windows? [Tutorial Windows](docs/windows.md).)
3. **Abra o Claude Code e diga `instalar`** (`claude` → escreva **`instalar`**).
   O Claude te guia: criar a chave no CRM Funnels, validar, e conectar. Aula em [`aula/roteiro.md`](aula/roteiro.md).

## ✅ Pré-requisitos

- A **Base da Agência de IA** já instalada (módulo `agencia-ia-base`).
- Conta **CRM Funnels** com acesso à Location que você quer conectar.
- `python3` (o instalador usa pra validar a credencial).

## 🧩 O que ele faz

- Te guia a criar a **Private Integration** no CRM Funnels (com os scopes certos).
- **Valida** a chave + Location ID com uma chamada real **antes** de salvar.
- Injeta no `.mcp.json` de forma **idempotente** (com backup e rollback).

---

🤖 Feito com [Claude Code](https://claude.com/claude-code) · método **ConsultorIA**
