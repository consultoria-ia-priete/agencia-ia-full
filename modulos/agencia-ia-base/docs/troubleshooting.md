# 🆘 Troubleshooting — Base da Agência de IA

O Claude Code lê este arquivo quando o aluno diz "deu erro".

---

### Sintoma: `sscia-sync: command not found`
**Causa:** `~/.local/bin` não está no PATH, ou o wrapper não foi copiado.
**Conserto:**
```bash
cp ~/.claude/skills/sscia-sync/sscia-sync ~/.local/bin/sscia-sync && chmod +x ~/.local/bin/sscia-sync
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```
Reabra o terminal e teste `sscia-sync --help`.

### Sintoma: `/opensquad` não abre o menu
**Causa:** o `claude` foi aberto fora da pasta da agência (sem `_opensquad/`).
**Conserto:** `cd` na pasta da agência (onde tem `_opensquad/` e `squads/`) e rode `claude` ali.

### Sintoma: as skills não aparecem / o Claude não conhece o opensquad
**Causa:** as skills não foram copiadas pra `~/.claude/skills/`, ou a sessão é antiga.
**Conserto:** confira `ls ~/.claude/skills/`. Se faltar, repita o Passo 2 do `install-base`.
Reabra o Claude Code pra ele recarregar as skills.

### Sintoma: `sscia-sync --new-client` reclama que não acha o template
**Causa:** `_TEMPLATE_SSCIA` não está na pasta de projetos esperada.
**Conserto:** confirme que existe `<PROJECTS_ROOT>/_TEMPLATE_SSCIA`. Se você usou outra
pasta, passe `--projects-root <caminho>` no comando.

### Sintoma: Python reclama de versão / módulo
**Causa:** `python3` ausente ou muito antigo.
**Conserto:** instale Python 3.10+ (`brew install python` no macOS). No Windows, `docs/windows.md`.

### Sintoma: `command not found` (git / node / npx / gh)
**Conserto:** instale o que faltar (`brew install git node gh`) e reabra o terminal.
