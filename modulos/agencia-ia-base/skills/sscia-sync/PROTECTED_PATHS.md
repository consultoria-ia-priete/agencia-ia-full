# Contrato de paths protegidos — sscia-sync

> **Regra absoluta:** estes paths NUNCA são tocados por `sscia-sync`, em nenhum modo (incluindo `--propagate-all`).

## Hardcoded como protegido

```python
PROTECTED_DIRS = [
    "_opensquad/_memory",         # brand-profile, company, brand-kit, preferences, credentials
    "_opensquad/chief",            # memória do chief
    "squads/*/_memory",            # CHRONICLER local de cada squad
    "squads/*/output",             # trabalho gerado pelo cliente
    ".claude",                     # config local do Claude Code
    ".sscia-backup",               # backups de sync anteriores
    ".vscode",
    ".idea",
    ".git",
]

PROTECTED_FILES = [
    ".mcp.json",                   # CRM Funnels key, MCPs específicos
    ".sscia-state.json",           # hashes de última sync (gerenciado pelo sscia-sync)
    ".env",
    ".env.*",
    ".gitignore",
]

# Glob patterns (qualquer lugar)
PROTECTED_PATTERNS = [
    "**/credentials.md",
    "**/ghl-credentials.md",
    "**/*credentials*",
    "**/*-secret*",
    "**/*.local.*",
    "**/*.env",
]
```

## Arquivos PROPAGÁVEIS (o que SIM é tocado, mediante confirmação)

```python
PROPAGABLE_GLOBS = [
    "squads/*/squad.yaml",
    "squads/*/squad-party.csv",
    "squads/*/agents/*.md",
    "squads/*/agents/*.agent.md",
    "squads/*/playbooks/*.md",
    "squads/*/tasks/*.md",
    "VERSION",                     # versão do template
]
```

## Como decidir se um arquivo deve ser tocado

```
arquivo X no cliente:
  1. X bate com algum PROTECTED_DIRS / PROTECTED_FILES / PROTECTED_PATTERNS?
     → SIM → 🔒 NUNCA toca (nem mostra no diff)
     → NÃO → continua

  2. X bate com algum PROPAGABLE_GLOBS?
     → SIM → 🟢 candidato a propagação
     → NÃO → ⚪ ignora (sscia-sync não conhece esse arquivo)

  3. Arquivo é candidato a propagação:
     - Hash atual no cliente == hash em .sscia-state.json?
        → SIM → não customizado, propagação direta segura
        → NÃO → ⚠️ CUSTOMIZADO (operador editou desde última sync)
                 → Pede confirmação: sobrescrever ou pular?
```

## Justificativa da política

- **Propagáveis = LÓGICA**: como agentes operam, prompts, definições. Update no template = update pra todos os clientes (ex: melhorou um agente de copy → vale pra Floor to Ceiling, JRS, Mendes...).

- **Protegidos = DADOS**: identidade do cliente (cores, voz, CRM Funnels key, memórias acumuladas, trabalho gerado). Nunca devem ser sobrescritos por uma propagação cega.

- **Customizados**: quando operador editou um arquivo de lógica em um cliente específico. Sscia-sync detecta via checksum vs `.sscia-state.json` e pede confirmação antes de sobrescrever.
