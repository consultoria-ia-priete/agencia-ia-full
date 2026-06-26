# 🆘 Troubleshooting — Windsor.ai + Google My Business

### Sintoma: o conector não acha a ficha / vem vazio
**Causa:** a conta Google autorizada não administra essa ficha do GMB.
**Conserto:** autorize no Windsor a conta Google que é **gerente/dona** da ficha.

### Sintoma: erro de Location / nada retorna
**Causa:** usou o `place_id` do Google Maps em vez do ID do GMB.
**Conserto:** use o formato `locations/XXXXXXXXXXXX`. Peça ao Claude pra listar as localizações
disponíveis no conector e copie o ID certo.

### Sintoma: o Windsor não aparece numa execução agendada (cron/headless)
**Causa:** o Windsor é uma integração via **claude.ai** — pode não estar presente em runs
headless/cron.
**Conserto:** rode os pulls de GMB numa sessão interativa do Claude (com a integração ativa).

### Sintoma: quero responder reviews/postar mas só consigo ler
**Causa:** ações de escrita precisam ser descobertas/autorizadas.
**Conserto:** rode `list_actions` no conector `google_my_business` e confirme a ação antes de executar.
