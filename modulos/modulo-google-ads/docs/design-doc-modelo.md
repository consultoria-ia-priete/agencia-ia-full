# Modelo — Design Doc pro Basic Access (Google Ads API)

Preencha com os seus dados e anexe/cole no formulário de solicitação de Basic Access.
O Google quer entender **o que** seu sistema faz com a API. Seja específico e honesto.

---

**Company / Account name:** {{NOME_DA_EMPRESA}}
**Contact email:** {{EMAIL}}
**Manager (MCC) ID:** {{MCC_ID}}
**Tool type:** Internal tool (uso próprio / gestão das contas dos meus clientes)

## What does your tool do?

Uma ferramenta interna que usa a Google Ads API para:
- **Reporting:** puxar métricas de campanhas (impressões, cliques, custo, conversões) para
  dashboards e relatórios dos clientes da agência.
- **Campaign Management:** criar, pausar e ajustar campanhas/orçamentos sob orientação do
  operador (human-in-the-loop), via o assistente Claude Code.
- **Conversion upload (opcional):** subir conversões offline/server-side para otimização.

## Who uses it?
A própria agência ({{NOME_DA_EMPRESA}}) para gerir as contas de anúncio dos seus clientes,
todas vinculadas ao MCC acima.

## API services used
- GoogleAdsService (search/searchStream) — leitura de métricas e entidades.
- CampaignService / CampaignBudgetService — gestão de campanhas e orçamentos.
- ConversionUploadService — (se aplicável) upload de conversões.

## Data handling
Os dados ficam na infraestrutura da própria agência. Não revendemos dados nem expomos a
API a terceiros. Acesso só pelo operador autenticado.

---

> Dica: solicitações genéricas costumam ser recusadas na 1ª tentativa. Cite os serviços
> da API que você realmente vai usar e o caso de uso concreto (gestão das contas do MCC).
