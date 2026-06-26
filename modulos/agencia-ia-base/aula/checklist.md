# ✅ Checklist de conclusão — Base da Agência de IA

O módulo só está **pronto** quando todos os itens passam. A skill `install-base` marca
cada um com o aluno.

## Pré-requisitos
- [ ] `claude`, `git`, `node`/`npx`, `python3` respondem no terminal
- [ ] `gh auth status` autenticado (pros módulos seguintes)

## Instalação
- [ ] `ls ~/.claude/skills/` mostra as 7 skills (opensquad, sscia-sync, ghl-publisher, carousel-generator, creative-factory, higgsfield-content, viral-video-factory)
- [ ] `sscia-sync --help` funciona (wrapper no PATH)
- [ ] `_TEMPLATE_SSCIA` posicionado na pasta de projetos
- [ ] Instância da agência criada (`sscia-sync --status` lista ela)

## Validação (teste de fogo)
- [ ] `cd <agência> && claude` → `/opensquad` abre o menu
- [ ] `/opensquad run nexus` passa pelo gate do NEXUS
- [ ] Escritórios dos agentes (dashboard) abrem

## Segurança
- [ ] `.gitignore` da agência cobre `.mcp.json`, `.env*`, `_opensquad/_memory/`, `*.bak`
- [ ] `scripts/scan-secrets.sh <agência>` = 0 hits (se for versionar)

## Aula
- [ ] Aula gravada: da cópia do template até `/opensquad run nexus` + dashboard
