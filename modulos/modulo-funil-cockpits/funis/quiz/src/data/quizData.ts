export type QuestionType = "single" | "multi";

export interface QuizOption {
  value: string;
  label: string;
}

export interface QuizQuestion {
  id: number;
  title: string;
  subtitle?: string;
  type: QuestionType;
  options: QuizOption[];
  /** Texto de prova social ou transição que aparece DEPOIS da resposta desta pergunta. */
  interText?: string;
  /** Se retornar false, a pergunta é pulada (lógica condicional). */
  condition?: (answers: Record<number, string[]>) => boolean;
}

export type ProfileType = "travado" | "iniciante" | "profissional" | "empregado";

const SIM_OPTIONS_P6 = ["afiliado", "dropshipping", "criador", "freelancer"];

export const quizQuestions: QuizQuestion[] = [
  // ETAPA 1 — TRIAGEM
  {
    id: 1,
    title: "Qual é a sua situação hoje?",
    type: "single",
    options: [
      { value: "emprego_fixo", label: "🏢 Tenho emprego fixo e quero uma renda extra no digital" },
      { value: "desempregado", label: "🔄 Estou desempregado e preciso de renda real o quanto antes" },
      { value: "marketing_tech", label: "💼 Já trabalho com marketing ou tecnologia e quero expandir" },
      { value: "estudante", label: "🎓 Sou estudante ou estou mudando de área" },
    ],
  },
  {
    id: 2,
    title: "Qual é a sua meta principal nos próximos 90 dias?",
    type: "single",
    options: [
      { value: "renda_extra", label: "💰 Ter uma renda extra de R$1K a R$3K/mês" },
      { value: "substituir_salario", label: "🚀 Substituir meu salário e trabalhar de casa" },
      { value: "5k_mais", label: "📈 Chegar a R$5K ou mais por mês com um serviço real" },
      { value: "liberdade", label: "🏠 Ter liberdade de horário e de lugar para trabalhar" },
    ],
  },
  {
    id: 3,
    title: "Você já usa ou já experimentou o Claude Code (ou qualquer IA para criar conteúdo ou sites)?",
    type: "single",
    options: [
      { value: "sim_uso", label: "✅ Sim, uso com frequência" },
      { value: "tentei_nao_soube", label: "🤔 Já tentei mas não soube usar direito" },
      { value: "ouvi_falar", label: "👀 Já ouvi falar mas nunca abri" },
      { value: "primeira_vez", label: "❌ Não — é a primeira vez que ouço esse nome" },
    ],
  },
  {
    id: 4,
    title: "Quanto tempo por dia você conseguiria dedicar a um negócio digital?",
    type: "single",
    options: [
      { value: "menos_1h", label: "⏱️ Menos de 1 hora" },
      { value: "1_2h", label: "🕐 Entre 1 e 2 horas" },
      { value: "2_4h", label: "🕑 Entre 2 e 4 horas" },
      { value: "mais_4h", label: "🕓 Mais de 4 horas — estou disposto a me dedicar de verdade" },
    ],
  },
  {
    id: 5,
    title: "Como você se descreveria em relação à tecnologia?",
    type: "single",
    options: [
      { value: "viro_bem", label: "💻 Me viro bem — aprendo rápido com ferramentas novas" },
      { value: "celular", label: "📱 Uso bastante o celular mas não mexo muito no computador" },
      { value: "dificuldade", label: "🤔 Tenho dificuldade mas aprendo quando alguém me ensina" },
      { value: "trava", label: "😰 Tecnologia me trava — fico com medo de fazer errado" },
    ],
  },

  // ETAPA 2 — DIAGNÓSTICO
  {
    id: 6,
    title: "Você já tentou algum modelo de negócio digital antes?",
    subtitle: "Pode marcar mais de uma opção.",
    type: "multi",
    options: [
      { value: "afiliado", label: "📢 Sim — afiliado (divulgar produtos de outros)" },
      { value: "dropshipping", label: "📦 Sim — dropshipping ou e-commerce" },
      { value: "criador", label: "📸 Sim — tentei virar criador de conteúdo ou influencer" },
      { value: "freelancer", label: "💻 Sim — freelancer ou prestação de serviços digitais" },
      { value: "nunca", label: "❌ Nunca tentei nada ainda" },
    ],
  },
  {
    id: 7,
    title: "Por que não deu o resultado que você queria?",
    type: "single",
    condition: (answers) => {
      const p6 = answers[6] || [];
      return p6.some((v) => SIM_OPTIONS_P6.includes(v));
    },
    options: [
      { value: "trafego_caro", label: "📉 Dependia de tráfego pago caro e o resultado era imprevisível" },
      { value: "audiencia", label: "👥 Precisava ter audiência grande ou muitos seguidores" },
      { value: "demorava", label: "⏳ Demorava muito para começar a ver dinheiro — me desanimei" },
      { value: "capital", label: "💸 Precisava de capital para investir e não tinha disponível" },
      { value: "complexo", label: "🧠 Era complexo demais — não consegui aprender enquanto trabalhava" },
    ],
    interText:
      '"Isso acontece com 83% das pessoas que tentam o digital. Não é falta de esforço — é modelo errado para o momento errado. Existem modelos que exigem audiência. Outros que exigem capital. E existe um que exige só o método certo e uma ferramenta de R$0."',
  },
  {
    id: 8,
    title: "Quando você pensa em oferecer um serviço para uma empresa local, o que passa pela sua cabeça?",
    type: "single",
    options: [
      { value: "nao_sei_comecar", label: '😮 "Não sei nem por onde começar a conversa"' },
      { value: "medo_entregar", label: '🤔 "Consigo imaginar, mas teria medo de não saber entregar"' },
      { value: "faz_sentido", label: '💡 "Essa ideia faz sentido — só preciso saber o que oferecer"' },
      { value: "pronto", label: '🙌 "Estou pronto — só preciso do método certo"' },
    ],
  },
  {
    id: 9,
    title: "Você já percebeu quantas empresas na sua cidade têm site ruim, desatualizado ou nem têm site?",
    type: "single",
    options: [
      { value: "nunca_pensei", label: "😲 Sim! E nunca tinha pensado que isso poderia ser uma oportunidade" },
      { value: "ja_percebi", label: "💡 Já tinha percebido e me perguntei como aproveitar isso" },
      { value: "agora_vejo", label: "🤔 Agora que você falou, começo a ver isso em todo lugar" },
      { value: "nunca_atencao", label: "😐 Nunca tinha prestado atenção nisso" },
    ],
  },
  {
    id: 10,
    title:
      "Se você conseguisse criar um site profissional para uma empresa em menos de 10 minutos usando IA, e cobrar R$1.500 por isso — o que você faria?",
    type: "single",
    options: [
      { value: "fecharia_semana", label: "🚀 Fecharia o primeiro cliente ainda essa semana" },
      { value: "entender_antes", label: "🤔 Precisaria entender melhor como funciona antes de agir" },
      { value: "medo_errar", label: "😰 Queria fazer mas teria medo de errar na entrega" },
      { value: "nao_me_vejo", label: '💭 Nunca me vi como "prestador de serviço" — não sei se funciona pra mim' },
    ],
  },
  {
    id: 11,
    title: "Qual dessas frases mais representa o que você sente hoje?",
    type: "single",
    options: [
      { value: "frustrei", label: '😔 "Já tentei coisas no digital e me frustrei — não sei se funciona pra mim"' },
      { value: "vejo_outros", label: '😤 "Vejo pessoas ganhando online e não entendo por que não funciona pra mim"' },
      { value: "potencial", label: '🔥 "Sei que tenho potencial — só preciso do caminho certo"' },
      { value: "procrastino", label: '💤 "Fico procrastinando por medo de errar de novo"' },
    ],
  },
  {
    id: 12,
    title: "O que você acha que falta para você ter uma renda de R$5K ou mais por mês online?",
    type: "single",
    options: [
      { value: "servico_real", label: "🎯 Um serviço real para oferecer — algo que o mercado pague bem" },
      { value: "conhecimento", label: "📚 Conhecimento técnico para executar sem depender de outros" },
      { value: "fechar_clientes", label: "💼 Saber como encontrar e fechar clientes sem parecer vendedor" },
      { value: "organizacao", label: "⏰ Organização e foco para colocar em prática de verdade" },
      { value: "autoconfianca", label: "💪 Autoconfiança para cobrar o que meu trabalho realmente vale" },
    ],
  },
  {
    id: 13,
    title: "Qual modelo te parece mais viável para o seu perfil hoje?",
    type: "single",
    options: [
      { value: "servico_local", label: "🤝 Prestar serviço para empresas locais (sem precisar de audiência)" },
      { value: "redes_sociais", label: "📱 Crescer nas redes sociais e monetizar audiência" },
      { value: "afiliado_comissoes", label: "🔁 Ganhar comissões como afiliado" },
      { value: "produtos_proprios", label: "📦 Vender produtos físicos ou digitais próprios" },
    ],
  },
  {
    id: 14,
    title: "Você prefere um modelo de negócio que:",
    type: "single",
    options: [
      { value: "rapido", label: "📅 Gera resultado rápido — primeiros clientes em dias, não meses" },
      { value: "seguro", label: "📈 Cresce devagar mas de forma segura e previsível" },
      { value: "escala_grande", label: "🎲 Pode demorar mas tem potencial de escala grande no longo prazo" },
      { value: "recorrente", label: "🔄 Gera renda recorrente todo mês sem precisar fechar cliente novo" },
    ],
  },
  {
    id: 15,
    title:
      "Como você se sentiria se, daqui a 30 dias, tivesse fechado seus primeiros 2 ou 3 clientes de site e estivesse faturando R$3K a R$4K?",
    type: "single",
    options: [
      { value: "aliviado", label: "🥹 Aliviado — finalmente provaria para mim mesmo que funciona" },
      { value: "motivado", label: "🚀 Motivado para escalar e ir muito além disso" },
      { value: "surpreso", label: "😮 Surpreso — não acredito que conseguiria tão rápido" },
      { value: "medo_manter", label: "🤔 Com medo de não conseguir manter esse ritmo" },
    ],
    interText:
      '"Mateus, de Porto Alegre, nunca tinha criado um site na vida. Em 15 dias aplicando o método do Alex Priete, fechou 2 clientes locais e faturou R$3.200. O terceiro cliente veio por indicação, sem precisar prospectar."',
  },
  {
    id: 16,
    title: "Qual das opções abaixo melhor descreve onde você está agora?",
    type: "single",
    options: [
      { value: "iniciante_zero", label: "🌱 Iniciante — começaria do zero absoluto" },
      { value: "base_marketing", label: "🔓 Tenho base em marketing ou tecnologia e quero usar IA para servir" },
      { value: "ja_tentei_tudo", label: "📉 Já tentei de tudo e estou em busca de algo que realmente funcione" },
      { value: "emprego_segunda", label: "💼 Tenho emprego e quero uma segunda renda antes de me comprometer totalmente" },
    ],
  },
  {
    id: 17,
    title:
      "Se eu te mostrasse exatamente como usar o Claude Code para criar um site profissional em 10 minutos — e ainda te desse o script para fechar o primeiro cliente — você colocaria isso em prática essa semana?",
    type: "single",
    options: [
      { value: "sim_certeza", label: "🔥 Sim, com certeza — estou esperando por isso" },
      { value: "provavelmente", label: "🤔 Provavelmente sim — mas precisaria entender bem antes" },
      { value: "medo_travar", label: "😰 Quero, mas tenho medo de travar na hora de abordar o cliente" },
      { value: "nao_pronto", label: "❌ Honestamente, não tenho certeza se estou pronto" },
    ],
  },
];

/**
 * Determina o perfil baseado na lógica de arquétipo:
 *  - Iniciante:    nunca tentou nada (P6 = ❌)
 *  - Profissional: já trabalha com marketing/tech (P1 = 💼)
 *  - Empregado:    tem emprego fixo (P1 = 🏢)
 *  - Travado:      qualquer outra combinação — já tentou modelo digital sem sucesso
 */
export const getProfileType = (answers: Record<number, string[]>): ProfileType => {
  const p1 = (answers[1] || [])[0];
  const p6 = answers[6] || [];

  const nuncaTentou = p6.length === 1 && p6[0] === "nunca";

  if (nuncaTentou) {
    if (p1 === "marketing_tech") return "profissional";
    if (p1 === "emprego_fixo") return "empregado";
    return "iniciante";
  }

  if (p1 === "marketing_tech") return "profissional";
  if (p1 === "emprego_fixo") return "empregado";

  return "travado";
};

export interface ProfileDescription {
  /** Tag pequena no topo do diagnóstico (ex: "O EMPREENDEDOR TRAVADO"). */
  profileTag: string;
  /** Headline principal — recebe {nome} interpolado. */
  diagnosisHeadline: (firstName: string) => string;
  /** Texto introdutório do diagnóstico (cinza). */
  realityCard: string;
  /** Texto da revelação (verde — A revelação). */
  opportunityCard: string;
  /** Percentual de potencial de sucesso (0-100). */
  successPercent: number;
  /** Texto sob o gauge. */
  successDescription: string;
}

export const profileDescriptions: Record<ProfileType, ProfileDescription> = {
  travado: {
    profileTag: "O EMPREENDEDOR TRAVADO",
    diagnosisHeadline: (n) =>
      `${n}, você não falhou. O modelo que você escolheu é que não era feito para o seu momento.`,
    realityCard:
      "Afiliado, dropshipping, criador de conteúdo — todos esses modelos têm algo em comum: eles exigem ou muito capital para anúncios, ou anos construindo audiência, ou muita dependência de algoritmo que você não controla. Para quem está começando ou recomeçando, esses são os modelos de maior risco e menor previsibilidade. Existe um modelo diferente. Um onde você controla seu resultado desde o primeiro cliente. Sem audiência. Sem estoque. Sem depender de plataforma.",
    opportunityCard:
      "Empresas locais — restaurantes, clínicas, salões, escritórios — pagam entre R$1.000 e R$3.000 por site. São milhares de negócios na sua cidade que ainda não têm site, ou têm um que não converte nada. Com o Claude Code, você cria um site profissional em 10 minutos. Você fecha 3 a 5 clientes por mês. Você chega a R$3K, R$8K, R$15K — com um serviço real que o mercado precisa. Esse é o caminho para o seu perfil.",
    successPercent: 78,
    successDescription:
      "Com base no seu perfil, você tem **78% de chances** de atingir R$3K a R$15K/mês — você já tem a maturidade da tentativa anterior, agora precisa do método certo.",
  },
  iniciante: {
    profileTag: "O INICIANTE COM POTENCIAL",
    diagnosisHeadline: (n) =>
      `${n}, boa notícia: você tem o perfil perfeito para começar pelo modelo mais seguro do digital.`,
    realityCard:
      "Você ainda não tentou nada — e isso é uma vantagem enorme. Não tem vícios de modelos que não funcionam. Não tem frustração de tentativas anteriores. Está com a cabeça aberta para aprender do jeito certo. O seu diagnóstico mostra disponibilidade, disposição para aprender e busca por algo real — não por um \"ganhe dinheiro rápido sem fazer nada\". Exatamente o perfil que prospera no modelo de sites com IA.",
    opportunityCard:
      "Enquanto a maioria perde meses tentando virar afiliado ou influencer, você pode — em 30 dias — criar sites profissionais com Claude Code, fechar seus primeiros clientes locais e ter sua primeira renda real online. Sem precisar aparecer. Sem seguidores. Sem programar.",
    successPercent: 88,
    successDescription:
      "Com base no seu perfil, você tem **88% de chances** de atingir R$3K a R$15K/mês — começando do jeito certo desde o primeiro dia, sem vícios de modelos que não funcionam.",
  },
  profissional: {
    profileTag: "O PROFISSIONAL EM EXPANSÃO",
    diagnosisHeadline: (n) =>
      `${n}, você já tem a base. Falta só o método para transformar IA em receita real e escalável.`,
    realityCard:
      "Você já tem conhecimento — o problema é que a maioria dos profissionais de marketing e tecnologia usa IA de forma genérica: para gerar texto, para editar imagem, para automatizar tarefa pontual. Mas existe um uso de IA que ninguém está explorando direito: criar e vender sites para empresas locais como serviço recorrente. Com o Claude Code, você entrega em 10 minutos o que outros demoram dias. E cobra R$1K a R$3K por projeto.",
    opportunityCard:
      "O seu perfil tem uma vantagem enorme: você já tem credibilidade para abordar empresários. Agora você precisa do método para transformar isso em faturamento de R$3K a R$15K/mês.",
    successPercent: 92,
    successDescription:
      "Com base no seu perfil, você tem **92% de chances** de atingir R$3K a R$15K/mês — você já tem credibilidade, falta só o método específico para vender sites com IA.",
  },
  empregado: {
    profileTag: "O EMPREGADO EM TRANSIÇÃO",
    diagnosisHeadline: (n) =>
      `${n}, seu diagnóstico mostra algo importante: você precisa de previsibilidade — e vender sites com IA entrega exatamente isso.`,
    realityCard:
      "Você está exatamente onde as pessoas inteligentes estão: quer a liberdade do digital, mas não vai largar tudo sem segurança. Isso não é covardia — é estratégia. O problema é que a maioria dos modelos digitais não gera renda previsível no curto prazo. Afiliado pode levar meses. Influencer pode levar anos. Mas prestar serviço é diferente.",
    opportunityCard:
      "Quando você fecha um cliente de site, você recebe. Quando fecha mais um, recebe mais. É direto, previsível, sem depender de algoritmo. Com o método do Alex Priete, você pode estar faturando R$3K a R$6K/mês — ainda empregado. Quando essa renda ultrapassar seu salário, você decide. Sem pressão. Com método. Com segurança.",
    successPercent: 82,
    successDescription:
      "Com base no seu perfil, você tem **82% de chances** de atingir R$3K a R$6K/mês — ainda mantendo seu emprego, com previsibilidade total.",
  },
};

/** Conteúdo da oferta — fixo entre os 4 perfis. */
export const offerContent = {
  ctaUrl: "https://lastlink.com/p/{{LASTLINK_PRODUTO_ALT}}/checkout-payment/",
  modules: [
    "**Módulo 0 — A Corrida do Ouro do AI Search:** como empresas estão pagando R$1K-5K por site que aparece no ChatGPT, Perplexity e Google AI Overviews (e por que essa janela fecha em 18 meses)",
    "**Módulo 1 — O Arsenal + Claude Code:** a estrutura que faz você entregar em 2h o que agência cobra R$8K e demora 3 semanas",
    "**Módulo 2 — Construa Hoje o Site Que Vai Pagar R$1.000 a R$5.000:** do zero ao 'pronto pra cobrar' em 30 minutos — sem escrever uma linha de código",
    "**Módulo 3 — O Framework 'Especialista Instantâneo':** o posicionamento reverso que faz cliente te tratar como sócio em vez de freelancer implorando trabalho",
    "**Módulo 4 — R$1.000 em 7 Dias:** o roteiro que já tirou aluno do zero ao primeiro cliente pagante na mesma semana da compra",
    "**Módulo 5 — Você Não Precisa Ser Vendedor:** o método consultivo que faz o cliente pedir o boleto antes de você mencionar preço",
    "**Módulo 6 — 1 Cliente Bem Atendido Vale por 5:** como transformar a primeira entrega no início de uma sequência de R$10K-30K (sem contrato mensal)",
  ],
  bonuses: [
    {
      name: "Bônus 1 — A Máquina Social Selling",
      detail: "script de prospecção pronto + lista de 50 empresas famintas por esse serviço (você só copia, cola e manda)",
      oldPrice: "R$197",
    },
    {
      name: "Bônus 2 — Workshop ao Vivo: A Ponte ConsultorIA",
      detail: "como subir do Negócio.IA pro modelo de recorrência high ticket que trava R$33K/mês com 5 contratos",
      oldPrice: "R$547",
    },
  ],
  totalValue: "R$971",
  fullPrice: "R$ 37,00",
  installments: "7x de R$ 6,16",
  priceSuffix: "Pagamento único · Sem mensalidade",
};
