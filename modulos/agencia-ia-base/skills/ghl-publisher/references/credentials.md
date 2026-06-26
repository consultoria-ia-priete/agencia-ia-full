# 🔐 Credenciais CRM Funnels — TEMPLATE (preencha com a SUA conta)

> Referência centralizada das credenciais do CRM Funnels usadas pela skill.
> **NÃO commitar este arquivo depois de preenchido** — ele vira secret.
> Os valores abaixo são **placeholders**; o módulo `modulo-crm-funnels` (skill `install-crm-funnels`)
> coleta e valida os seus e preenche aqui (ou no `.mcp.json`).

---

## API & Location

| Campo | Valor |
|---|---|
| **Location ID** | `{{GHL_LOCATION_ID}}` |
| **API Key (PIT)** | `{{GHL_API_KEY}}` |
| **API Version** | `2021-07-28` |
| **Base URL** | `https://services.leadconnectorhq.com` |

## User

| Campo | Valor |
|---|---|
| **User ID** | `{{GHL_USER_ID}}` |
| **Email** | {{EMAIL_OPERADOR}} |

## Canais sociais conectados

> Os Account IDs do CRM Funnels têm o formato `<companyId>_<locationId>_<accountId>`.
> Descubra os seus com a chamada de validação abaixo (lista as contas conectadas).

### Instagram
```
Account ID: {{IG_ACCOUNT_ID}}
Platform: instagram
Account name: @{{SEU_INSTAGRAM}}
```

### LinkedIn
```
Account ID: {{LI_ACCOUNT_ID}}
Platform: linkedin
Account name: {{SEU_NOME}}
```

---

## Como cada agente deve carregar essas credenciais

### Em Python
```python
LOC = "{{GHL_LOCATION_ID}}"
API_KEY = "{{GHL_API_KEY}}"
USER_ID = "{{GHL_USER_ID}}"
IG_ID = "{{IG_ACCOUNT_ID}}"
LI_ID = "{{LI_ACCOUNT_ID}}"
```

### Headers padrão
```python
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
}
```

---

## Validação pré-uso (recomendado) — também descobre seus Account IDs

Antes de qualquer publicação, valide que os canais estão conectados (e copie os
Account IDs que aparecerem pros campos acima):

```python
import urllib.request, ssl, json

req = urllib.request.Request(
    f"https://services.leadconnectorhq.com/social-media-posting/{LOC}/accounts",
    headers=HEADERS
)
r = urllib.request.urlopen(req, context=ssl._create_unverified_context())
data = json.loads(r.read())
for acc in data["results"]["accounts"]:
    print(f"{acc['platform']:10} | {acc.get('name', '?'):20} | {acc.get('status', '?')} | id={acc['id']}")
```

Se algum canal não estiver `active`, **bloquear publicação** e reconectar o canal no CRM Funnels.
