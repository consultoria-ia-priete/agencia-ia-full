import { useState } from "react";
import { Button } from "@/components/ui/button";
import { CaptureModal } from "@/components/CaptureModal";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  ArrowRight,
  CheckCircle2,
  XCircle,
  Sparkles,
  Terminal,
  Zap,
  Shield,
  CreditCard,
  Lock,
  Rocket,
  Target,
  TrendingUp,
  Flame,
} from "lucide-react";

const marqueeItems = [
  "⚡ Brasil abre 3,5 milhões de novos CNPJs por ano",
  "7 a 11 milhões de empresas precisando aparecer no AI Search",
  "Mercado de R$47 bilhões aberto pra quem tem o método",
  "ChatGPT · Perplexity · Google AI Overviews — onde os clientes olham agora",
  "Bônus: Script R$1.000 em 15 dias + lista de 50 empresas famintas",
  "8 anos refinando o método — testado e validado em produção",
];

const modules = [
  {
    n: "00",
    title: "A Corrida do Ouro do AI Search",
    tag: "abertura",
    body:
      "Por que 99% dos sites brasileiros vão sumir do ChatGPT, Perplexity e Google AI Overviews nos próximos 18 meses. O contexto da janela de R$47 bilhões — e por que quem entrar AGORA vai cobrar enquanto os outros ainda descobrem do que se trata.",
  },
  {
    n: "01",
    title: "O Arsenal + Claude Code",
    tag: "estrutura",
    body:
      "A estrutura que faz você entregar em 2 horas o que agência cobra R$8.000 e demora 3 semanas. O setup completo do Claude Code + ferramentas auxiliares — sem stack pesado, sem mensalidade que come seu lucro, sem complexidade.",
  },
  {
    n: "02",
    title: "Construa Hoje o Site Que Vai Pagar R$1.000 a R$5.000",
    tag: "execução",
    body:
      "O passo a passo cronometrado: do briefing em branco ao 'pronto pra cobrar' em 30 minutos. Estrutura de comando pra Claude Code entregar site responsivo, com SEO, AI Search optimization, animações e formulário — sem você escrever uma linha de código.",
  },
  {
    n: "03",
    title: "O Framework \"Especialista Instantâneo\"",
    tag: "posicionamento",
    body:
      "O posicionamento reverso que faz cliente te tratar como sócio em vez de freelancer implorando trabalho. Como construir credibilidade em 7 dias sem inventar currículo, sem mentir, sem precisar de portfólio gigante. Funciona pra quem tá começando do zero.",
  },
  {
    n: "04",
    title: "R$1.000 em 7 Dias",
    tag: "primeira venda",
    body:
      "O roteiro que já tirou aluno do zero ao primeiro PIX de R$1.000 na mesma semana. 3 caminhos validados — Lista Quente, Prospecção Ativa e Funil com Anúncios — com scripts copy-paste pra cada um. Modelos de mensagem que já funcionaram em produção.",
  },
  {
    n: "05",
    title: "Você Não Precisa Ser Vendedor",
    tag: "fechamento",
    body:
      "O método consultivo que faz cliente pedir o boleto antes de você mencionar preço. Sem pressão, sem técnica de venda batida — só uma estrutura de diagnóstico que faz o empresário entender por que precisa do site AGORA, e por que VOCÊ é a pessoa certa.",
  },
  {
    n: "06",
    title: "1 Cliente Bem Atendido Vale por 5",
    tag: "LTV",
    body:
      "Como transformar a primeira entrega no início de uma sequência de R$10K-30K do mesmo cliente — site novo, landing page, blog, página de vendas. Um cliente bem atendido vira a fila do próximo projeto, sem você precisar prospectar de novo.",
  },
];

const faqs = [
  {
    q: "Preciso saber programar para usar o método?",
    a: "Não. O Claude Code escreve o código pra você. Você só dá os comandos certos — e eles estão prontos no Módulo 02. Em 30 minutos sai um site profissional sem você escrever uma linha de código.",
  },
  {
    q: "O que é o Claude Code? Preciso pagar por ele?",
    a: "Claude Code é a ferramenta de IA da Anthropic que cria sites a partir de descrição em texto. Tem versão gratuita generosa pra começar. Pra escalar, o plano pago vale a pena (US$20/mês) — uma única venda já cobre o ano todo.",
  },
  {
    q: "Em quanto tempo consigo meu primeiro cliente?",
    a: "Depende do caminho. Lista Quente: 7-15 dias. Prospecção Ativa: 30-45 dias com disciplina. Funil com Anúncios: 30-60 dias com R$300-500 de investimento inicial em mídia. Os 3 caminhos estão detalhados no Módulo 04 — com scripts prontos.",
  },
  {
    q: "Eu não tenho tempo. Trabalho o dia todo. Funciona?",
    a: "Aulas curtas, scripts copy-paste, lista de empresas pronta no Bônus 1. 2 horas no fim de semana já são suficientes pra mandar a primeira prospecção e começar a fila de clientes — sem largar o que você faz hoje.",
  },
  {
    q: "E se eu não conseguir fechar nenhum cliente?",
    a: "7 dias de garantia incondicional. Se você seguir o método e não fechar, devolvo R$37. Sem perguntas. O Bônus 1 entrega lista de 50 empresas + script — é literalmente copia-cola. O método não falha, quem falha é quem não faz.",
  },
  {
    q: "Funciona para quem já trabalha com marketing?",
    a: "Funciona ainda melhor. Quem já tem base de marketing (tráfego, copy, funil) acelera muito mais rápido. O método é a peça que estava faltando pra você converter sua skill em receita real entregando sites que o mercado precisa AGORA.",
  },
];

const Index = () => {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30 overflow-x-hidden">
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none hidden md:block">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[140px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#3a1d12]/20 rounded-full blur-[140px]" />
      </div>

      <main className="relative z-10">
        {/* NAV */}
        <nav className="sticky top-0 z-30 backdrop-blur-md bg-background/80 border-b border-border">
          <div className="container mx-auto px-4 py-4 flex items-center">
            <div className="font-mono text-lg">
              <span className="font-bold">negócio.ia</span>
              <span className="text-muted-foreground"> | by Alex Priete</span>
            </div>
          </div>
        </nav>

        {/* HERO — Halbert+Hormozi storytelling visceral + Schwartz "sem X" */}
        <section className="container mx-auto px-4 py-12 md:py-20 text-center max-w-5xl">
          <div className="inline-flex flex-wrap items-center gap-x-2 px-3 py-1 mb-6 text-[10px] md:text-xs font-mono tracking-wider text-primary uppercase border rounded-full border-primary/30 bg-primary/10 max-w-full">
            <span>Mini Curso Completo</span>
            <span className="text-muted-foreground">·</span>
            <span>Claude Code · AI Search Era</span>
            <span className="text-muted-foreground">·</span>
            <span>R$37 — pagamento único</span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold md:tracking-tight leading-tight mb-5 break-words [overflow-wrap:anywhere]">
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
              R$3K a R$15K por mês
            </span>
            <span className="block text-foreground mt-1">
              vendendo sites que o Claude Code cria em 30 minutos
            </span>
            <span className="block mt-3 text-xl sm:text-2xl md:text-3xl lg:text-4xl text-foreground/90 font-bold">
              — pra empresas que precisam aparecer no ChatGPT antes de sumir do mapa
            </span>
          </h1>

          <p className="max-w-3xl mx-auto text-base md:text-lg text-muted-foreground leading-relaxed mb-6 break-words">
            99% dos sites brasileiros vão sumir do AI Search nos próximos{" "}
            <strong className="text-foreground">18 meses</strong>. As empresas que descobrirem isso vão pagar{" "}
            <strong className="text-foreground">R$1.000 a R$5.000 por site</strong>.{" "}
            <span className="block mt-1 text-foreground font-semibold">
              3 a 5 sites no mês = R$3K a R$15K na sua conta.
            </span>
          </p>

          <ul className="max-w-2xl mx-auto mb-8 space-y-2 text-left">
            <li className="flex items-start gap-3 text-sm md:text-base text-foreground/90">
              <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
              <span>
                <strong className="text-foreground">Sem precisar saber programar</strong> — o Claude Code escreve o código pra você
              </span>
            </li>
            <li className="flex items-start gap-3 text-sm md:text-base text-foreground/90">
              <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
              <span>
                <strong className="text-foreground">Sem precisar de seguidores</strong>, autoridade prévia ou histórico de mercado
              </span>
            </li>
            <li className="flex items-start gap-3 text-sm md:text-base text-foreground/90">
              <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
              <span>
                <strong className="text-foreground">Sem dependência</strong> de algoritmo, dropshipping ou produto chinês
              </span>
            </li>
          </ul>

          <div className="flex flex-col items-center gap-4">
            <Button
              size="lg"
              onClick={() => setModalOpen(true)}
              className="w-full sm:w-auto h-auto min-h-14 md:min-h-16 py-3 md:py-4 px-6 sm:px-10 text-base sm:text-lg md:text-xl font-bold bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.6)] hover:scale-[1.02] transition-transform whitespace-normal text-center leading-tight"
            >
              <span className="break-words">→ Quero Entrar Agora — 7x de R$ 6,16</span>
            </Button>
            <div className="flex flex-wrap gap-x-5 gap-y-2 justify-center text-xs text-muted-foreground">
              <span className="inline-flex items-center gap-1.5"><CheckCircle2 className="w-3.5 h-3.5 text-primary" /> Acesso imediato</span>
              <span className="inline-flex items-center gap-1.5"><Shield className="w-3.5 h-3.5 text-primary" /> Garantia de 7 dias</span>
              <span className="inline-flex items-center gap-1.5"><Lock className="w-3.5 h-3.5 text-primary" /> Pagamento seguro</span>
            </div>
          </div>
        </section>

        {/* MARQUEE */}
        <section className="border-y border-border bg-card/50 overflow-hidden py-4">
          <div className="flex animate-marquee whitespace-nowrap">
            {[...marqueeItems, ...marqueeItems].map((item, i) => (
              <div key={i} className="flex items-center gap-4 px-6 text-sm text-muted-foreground font-mono">
                <span>{item}</span>
                <span className="text-primary">◆</span>
              </div>
            ))}
          </div>
        </section>

        {/* REVELAÇÃO — story bridge Halbert (post-marquee) */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-3xl">
          <div className="bg-gradient-to-br from-orange-950/40 via-card to-card border border-orange-500/30 rounded-2xl p-6 md:p-9">
            <p className="text-xs md:text-sm font-bold tracking-wider uppercase text-orange-400 mb-3 flex items-center gap-2">
              <Flame className="w-4 h-4" /> A parte que ninguém tá te contando
            </p>
            <p className="text-base md:text-lg leading-relaxed text-foreground/90">
              ChatGPT, Perplexity e Google AI Overviews já viraram a porta de entrada do consumidor brasileiro.
              <strong className="text-foreground"> Empresas que não aparecem nesses mecanismos estão sumindo do mapa</strong> —
              não em 5 anos, em 18 meses.
            </p>
            <p className="text-base md:text-lg leading-relaxed text-foreground/90 mt-3">
              Você não precisa ser programador. Não precisa de portfólio gigante. Não precisa de seguidores.{" "}
              <strong className="text-foreground">Precisa entender o método e entrar antes da onda.</strong>{" "}
              É exatamente isso que o Negócio.IA entrega.
            </p>
          </div>
        </section>

        {/* COMPARAÇÃO sem método vs com método */}
        <section className="container mx-auto px-4 py-16 md:py-24 max-w-6xl">
          <h2 className="text-3xl md:text-5xl font-extrabold text-center mb-14 leading-tight">
            IA genérica entrega resultado genérico.
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
              O método certo entrega clientes reais.
            </span>
          </h2>
          <div className="grid md:grid-cols-2 gap-6 mb-14">
            {/* sem método */}
            <div className="bg-card/60 border border-border rounded-2xl p-7">
              <p className="font-mono text-xs text-muted-foreground mb-2">// sem método</p>
              <h3 className="text-xl font-bold mb-5">O que acontece sem o método</h3>
              <ul className="space-y-3">
                {[
                  "Usa IA sem método e entrega resultado igual ao de qualquer um — preço caindo no chão",
                  "Tenta abordar empresário sem credibilidade e a proposta vai pro lixo na hora",
                  "Acha que precisa de currículo gigante antes de cobrar — fica preso, mês após mês",
                  "Consome conteúdo de IA todo dia mas não converte uma única hora em PIX na conta",
                  "Vê os primeiros 1% entrarem no mercado de R$47 bilhões e fica olhando de fora",
                ].map((it, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                    <XCircle className="w-5 h-5 text-red-500/70 flex-shrink-0 mt-0.5" />
                    <span>{it}</span>
                  </li>
                ))}
              </ul>
            </div>
            {/* com método */}
            <div className="bg-gradient-to-br from-primary/10 via-card to-card border border-primary/40 rounded-2xl p-7 relative overflow-hidden">
              <Sparkles className="absolute top-4 right-4 w-5 h-5 text-primary/60" />
              <p className="font-mono text-xs text-primary mb-2">// com negócio.ia</p>
              <h3 className="text-xl font-bold mb-5">O que muda com o método certo</h3>
              <ul className="space-y-3">
                {[
                  "Claude Code gera site profissional em 30 minutos com prompts prontos do Módulo 02",
                  "3 caminhos validados pra fechar primeiro cliente — do imediato ao escalável",
                  "Script de fechamento que faz empresário pedir boleto antes de você falar preço",
                  "Credibilidade construída em 7 dias — sem precisar inventar histórico de mercado",
                  "R$3K a R$15K/mês entregando o que o mercado AI Search é obrigado a comprar AGORA",
                ].map((it, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                    <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                    <span>{it}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* TERMINAL MOCKUP */}
          <div className="bg-black border border-border rounded-2xl overflow-hidden font-mono text-sm shadow-2xl">
            <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-card/50">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <div className="w-3 h-3 rounded-full bg-[#FF5C39]/80" />
              </div>
              <span className="ml-3 text-xs text-muted-foreground">claude-code — terminal</span>
              <Terminal className="ml-auto w-4 h-4 text-muted-foreground" />
            </div>
            <div className="p-6 space-y-2 text-xs md:text-sm leading-relaxed">
              <div className="flex flex-wrap items-baseline gap-x-2">
                <span className="text-primary">➜</span>
                <span className="text-muted-foreground">~</span>
                <span className="text-foreground">claude "Crie um site para uma clínica odontológica com foco em implantes, otimizado pra ChatGPT e Google AI Overviews."</span>
              </div>
              <div className="text-muted-foreground">... processando requisição</div>
              <div className="text-muted-foreground">[==================================] 100%</div>
              <div className="text-primary">✓ Site gerado com sucesso (8 min 34 seg)</div>
              <div className="text-primary">✓ Otimizado pra AI Search (schema.org + meta semântica)</div>
              <div className="text-primary">✓ Valor de mercado estimado: R$1.500 – R$3.500</div>
              <div className="flex items-baseline gap-x-2 pt-2">
                <span className="text-primary">➜</span>
                <span className="text-muted-foreground">~</span>
                <span className="text-foreground animate-pulse">_</span>
              </div>
            </div>
          </div>
        </section>

        {/* MÓDULOS */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-4xl">
          <div className="text-center mb-12">
            <p className="font-mono text-xs text-primary mb-3">// o treinamento</p>
            <h2 className="text-3xl md:text-5xl font-extrabold mb-4">7 módulos cronometrados — você dá play hoje, fecha cliente essa semana</h2>
            <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto">
              Cada módulo termina com o próximo passo. Sem teoria solta. Sem encheção.
            </p>
          </div>
          <Accordion type="single" collapsible className="bg-card border border-border rounded-2xl px-6 md:px-8">
            {modules.map((m) => (
              <AccordionItem key={m.n} value={m.n}>
                <AccordionTrigger>
                  <div className="flex flex-col md:flex-row md:items-center gap-2 md:gap-4 text-left">
                    <span className="font-mono text-primary text-sm flex-shrink-0">Módulo {m.n}</span>
                    <span className="text-base md:text-lg font-bold">{m.title}</span>
                    <span className="font-mono text-xs text-muted-foreground hidden md:inline">| {m.tag}</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent>{m.body}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>

        {/* 3 CAMINHOS */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-6xl">
          <div className="text-center mb-12">
            <p className="font-mono text-xs text-primary mb-3">// 3 caminhos para clientes</p>
            <h2 className="text-3xl md:text-5xl font-extrabold mb-4">Você escolhe como quer começar</h2>
            <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto">
              Do mais rápido ao mais escalável — os três caminhos estão no Módulo 04.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { icon: Rocket, n: "01", title: "Lista Quente", body: "Contatos que já confiam em você. O caminho mais rápido pra fechar ainda esta semana — sem histórico, sem experiência, sem ad spend.", tag: "primeiro PIX em dias" },
              { icon: Target, n: "02", title: "Prospecção Ativa", body: "Mapeie empresas sem site no Google Maps e aborde direto com o script do Bônus 1. Funciona em qualquer cidade do Brasil. Previsível e consistente.", tag: "consistência garantida" },
              { icon: TrendingUp, n: "03", title: "Funil com Anúncios", body: "Anuncie no Meta pra atrair empresários interessados em site. R$300-500 inicial. O caminho da escala real — clientes chegando no piloto automático.", tag: "escala real" },
            ].map((c) => (
              <div key={c.n} className="bg-card border border-border rounded-2xl p-7 hover:border-primary/40 transition-colors">
                <c.icon className="w-9 h-9 text-primary mb-4" />
                <p className="font-mono text-xs text-muted-foreground mb-2">{c.n}</p>
                <h3 className="text-xl font-bold mb-3">{c.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed mb-4">{c.body}</p>
                <p className="font-mono text-xs text-primary">{c.tag}</p>
              </div>
            ))}
          </div>
        </section>

        {/* PRA QUEM É */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-5xl">
          <div className="text-center mb-12">
            <p className="font-mono text-xs text-primary mb-3">// pra quem é?</p>
            <h2 className="text-3xl md:text-5xl font-extrabold leading-tight">
              Se você se identifica:
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                negócio.ia foi feito para você!
              </span>
            </h2>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-card border border-border rounded-2xl p-7">
              <h3 className="text-lg font-bold mb-5 flex items-center gap-2"><CheckCircle2 className="w-5 h-5 text-primary" /> Pra quem é:</h3>
              <ul className="space-y-3">
                {[
                  "Quer trabalhar de casa e ter o primeiro negócio digital com receita real",
                  "Já usa ou quer usar Claude Code e IA com método (não com prompts soltos)",
                  "Busca renda de R$3K a R$15K/mês entregando serviço — não promessa",
                  "Profissional de marketing querendo expandir com mecanismo novo",
                  "Topa trabalhar 2-3h por dia pra construir negócio em 60-90 dias",
                ].map((it, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                    <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" /> <span>{it}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-card/60 border border-border rounded-2xl p-7">
              <h3 className="text-lg font-bold mb-5 flex items-center gap-2"><XCircle className="w-5 h-5 text-red-500/70" /> Pra quem NÃO é:</h3>
              <ul className="space-y-3">
                {[
                  "Acha que IA vai fazer tudo sozinha sem você dar direção",
                  "Procura curso teórico de \"como ganhar dinheiro online\"",
                  "Busca shortcut sem aplicar — método exige que você faça os passos",
                  "Não tem 2-3h por dia pra dedicar nas primeiras semanas",
                ].map((it, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                    <XCircle className="w-5 h-5 text-red-500/70 flex-shrink-0 mt-0.5" /> <span>{it}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* SOBRE ALEX — story Halbert */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-5xl">
          <div className="text-center mb-12">
            <p className="font-mono text-xs text-primary mb-3">// quem vai te ensinar</p>
            <h2 className="text-3xl md:text-5xl font-extrabold">Construído por quem usa Claude Code todo dia</h2>
          </div>
          <div className="grid md:grid-cols-[280px_1fr] gap-8 items-start bg-card border border-border rounded-2xl p-7 md:p-10">
            <div>
              <img src="/images/alex.jpg" alt="Alex Priete" className="w-full rounded-2xl object-cover aspect-square shadow-xl" />
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-1">Alex Priete</h3>
              <p className="font-mono text-xs text-muted-foreground mb-5">// Founder · Marketing Digital · Atende EUA e Brasil</p>
              <div className="space-y-4 text-muted-foreground leading-relaxed mb-6">
                <p>
                  Em 2018, eu trabalhava 100 km de casa, mal via meus filhos. Tentei afiliado, dropshipping, lançamento — e tudo que vinha era complexidade, dependência de algoritmo e venda que travava todo mês.
                </p>
                <p>
                  Descobri o que funciona quando parei de procurar fórmula mágica e olhei pra o que <strong className="text-foreground">empresário paga DE VERDADE</strong>: serviço que resolve um problema visível AGORA. Vender sites — antes complicado — virou o atalho mais limpo no momento em que IA mudou as regras do jogo.
                </p>
                <p>
                  Testei. Refinei. Transformei em método. Hoje atendo clientes nos EUA e no Brasil, ajudei a vender +R$187 milhões em consultoria, e estou montando o caminho pra você não precisar levar 8 anos descobrindo o que eu descobri.
                </p>
              </div>
              <ul className="space-y-2 text-sm">
                {[
                  "8 anos refinando o método de marketing digital",
                  "Atende clientes nos EUA e no Brasil",
                  "Já ajudou a vender +R$187 milhões em consultoria",
                  "Usuário diário do Claude Code (esse curso é o que eu USO, não teoria)",
                ].map((it, i) => (
                  <li key={i} className="flex items-start gap-2 text-muted-foreground">
                    <span className="font-mono text-primary">//</span> <span>{it}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* OFERTA */}
        <section id="oferta" className="container mx-auto px-4 py-16 md:py-20 max-w-3xl">
          <div className="text-center mb-10">
            <p className="font-mono text-xs text-primary mb-3">// tudo que você recebe</p>
            <h2 className="text-3xl md:text-5xl font-extrabold">O que está incluso no seu acesso</h2>
          </div>
          <div className="bg-card border-2 border-primary/40 rounded-2xl p-6 md:p-10 animate-card-glow">
            <h3 className="text-2xl font-bold mb-2">negócio.ia — Treinamento Completo</h3>
            <p className="font-mono text-xs text-muted-foreground mb-7">
              // 7 módulos + 2 bônus exclusivos · acesso imediato
            </p>
            <ul className="space-y-2 mb-7 text-sm md:text-base">
              {[
                ["Módulo 0 — A Corrida do Ouro do AI Search", "R$47"],
                ["Módulo 1 — O Arsenal Claude Code", "R$97"],
                ["Módulo 2 — Site em 30 Minutos", "R$97"],
                ["Módulo 3 — Especialista Instantâneo", "R$67"],
                ["Módulo 4 — R$1.000 em 7 Dias", "R$127"],
                ["Módulo 5 — Você Não Precisa Ser Vendedor", "R$97"],
                ["Módulo 6 — 1 Cliente Vale por 5", "R$97"],
              ].map(([item, price]) => (
                <li key={item} className="flex justify-between items-center py-1 border-b border-border/50 gap-3">
                  <span className="flex items-start gap-2"><CheckCircle2 className="w-4 h-4 text-primary flex-shrink-0 mt-0.5" /> {item}</span>
                  <span className="text-muted-foreground line-through flex-shrink-0">{price}</span>
                </li>
              ))}
              {[
                ["🎁 Bônus 1 — A Máquina Social Selling (script + lista de 50 empresas)", "R$197"],
                ["🎁 Bônus 2 — Workshop Ponte ConsultorIA (ao vivo)", "R$547"],
              ].map(([item, price]) => (
                <li key={item} className="flex justify-between items-center py-1 border-b border-border/50 gap-3">
                  <span className="flex items-start gap-2 flex-wrap">
                    <Zap className="w-4 h-4 text-orange-500 flex-shrink-0 mt-0.5" />
                    <span>{item}</span>
                    <span className="text-[10px] font-bold bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded-full">BÔNUS</span>
                  </span>
                  <span className="text-muted-foreground line-through flex-shrink-0">{price}</span>
                </li>
              ))}
            </ul>
            <div className="flex justify-between items-center mb-6">
              <span className="text-sm text-muted-foreground">Valor real do conteúdo</span>
              <span className="text-lg text-muted-foreground line-through">R$1.373</span>
            </div>
            <div className="text-center mb-7">
              <p className="text-sm text-foreground mb-2">Hoje você leva tudo por</p>
              <p className="text-xs text-muted-foreground tracking-wider uppercase mb-1">Em até</p>
              <p className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39] leading-none">
                7x de R$ 6,16
              </p>
              <p className="text-base md:text-lg text-foreground mt-3">
                ou <strong className="text-foreground">R$ 37,00</strong> à vista
              </p>
              <p className="font-mono text-xs text-muted-foreground mt-2">// pagamento único · sem mensalidade</p>
              <p className="text-xs text-primary mt-3 font-medium">
                Menos que um almoço de domingo. Pra um método que pode te tirar da CLT em 90 dias.
              </p>
            </div>
            <Button
              size="lg"
              onClick={() => setModalOpen(true)}
              className="w-full h-auto min-h-14 md:min-h-16 py-3 md:py-4 px-6 text-base sm:text-lg md:text-xl font-bold bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.6)] whitespace-normal text-center leading-tight"
            >
              <span className="break-words">→ Quero Meu Acesso Agora</span>
              <ArrowRight className="w-5 h-5 ml-2 flex-shrink-0" />
            </Button>
            <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 mt-5 text-xs text-muted-foreground font-mono">
              <span className="inline-flex items-center gap-1.5"><CreditCard className="w-3 h-3" /> Cartão ou PIX</span>
              <span className="inline-flex items-center gap-1.5"><Lock className="w-3 h-3" /> Pagamento 100% seguro</span>
              <span className="inline-flex items-center gap-1.5"><CheckCircle2 className="w-3 h-3" /> Acesso imediato</span>
            </div>
          </div>
        </section>

        {/* GARANTIA — Halbert: o risco é meu */}
        <section className="container mx-auto px-4 py-12 max-w-4xl">
          <div className="bg-gradient-to-br from-[#1f0f09]/30 via-card to-card border-2 border-primary/40 rounded-2xl p-7 md:p-9 flex flex-col md:flex-row items-start gap-6">
            <div className="flex-shrink-0 w-16 h-16 md:w-20 md:h-20 rounded-full bg-primary/20 border-2 border-primary/40 flex items-center justify-center">
              <Shield className="w-9 h-9 md:w-11 md:h-11 text-primary" />
            </div>
            <div>
              <h3 className="text-2xl md:text-3xl font-bold mb-3">Garantia incondicional de 7 dias — o risco é todo meu</h3>
              <p className="text-muted-foreground leading-relaxed text-sm md:text-base">
                Você compra agora, abre os módulos e tem <strong className="text-foreground">7 dias inteiros pra dar uma volta no método</strong>. Se em qualquer momento você sentir que isso aqui <em>não é</em> o atalho que prometi — manda um email e eu devolvo seus R$37. Sem perguntas. Sem burocracia. Sem precisar provar nada.
              </p>
              <p className="text-foreground leading-relaxed text-sm md:text-base mt-3 font-medium">
                Você só fica se concordar que faz sentido pra você.
              </p>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-3xl">
          <div className="text-center mb-12">
            <p className="font-mono text-xs text-primary mb-3">// dúvidas frequentes</p>
            <h2 className="text-3xl md:text-5xl font-extrabold">"Mas Alex, e se..."</h2>
          </div>
          <Accordion type="single" collapsible className="bg-card border border-border rounded-2xl px-6 md:px-8">
            {faqs.map((f, i) => (
              <AccordionItem key={i} value={`q-${i}`}>
                <AccordionTrigger className="text-base md:text-lg font-bold text-left">{f.q}</AccordionTrigger>
                <AccordionContent>{f.a}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>

        {/* LAST CHANCE — Schwartz recap matemático + identidade */}
        <section className="container mx-auto px-4 py-16 md:py-20 text-center max-w-3xl">
          <p className="font-mono text-xs text-primary mb-3">// última chance</p>
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4">A janela do AI Search é AGORA.</h2>
          <p className="text-xl text-muted-foreground mb-6">Você vai surfar ou assistir?</p>
          <div className="text-left bg-card/60 border border-border rounded-2xl p-6 md:p-8 mb-10">
            <p className="text-base md:text-lg text-muted-foreground leading-relaxed mb-3">
              Em cada revolução tecnológica, uma minoria age cedo e domina.
            </p>
            <p className="text-base md:text-lg text-muted-foreground leading-relaxed mb-3">
              <strong className="text-foreground">R$3K-15K/mês</strong> entregando sites que o Claude Code cria em 30 minutos, pra um mercado de <strong className="text-foreground">R$47 bilhões</strong> que tá pedindo isso AGORA.
            </p>
            <p className="text-base md:text-lg text-foreground leading-relaxed font-medium">
              Em 18 meses essa janela fecha. Você pode entrar por R$37 hoje (ou 7x de R$6,16) — ou continuar onde tá esperando a próxima oportunidade aparecer.
            </p>
          </div>
          <Button
            size="lg"
            onClick={() => setModalOpen(true)}
            className="w-full sm:w-auto h-auto min-h-14 md:min-h-16 py-3 md:py-4 px-8 sm:px-10 text-base sm:text-lg md:text-xl font-bold bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.6)] whitespace-normal text-center leading-tight"
          >
            <span className="break-words">→ Quero Meu Acesso por R$37 Agora</span>
            <ArrowRight className="w-5 h-5 ml-2 flex-shrink-0" />
          </Button>
          <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 mt-5 text-xs text-muted-foreground font-mono">
            <span className="inline-flex items-center gap-1.5"><CreditCard className="w-3 h-3" /> Cartão ou PIX</span>
            <span className="inline-flex items-center gap-1.5"><Shield className="w-3 h-3" /> Garantia de 7 dias</span>
            <span className="inline-flex items-center gap-1.5"><CheckCircle2 className="w-3 h-3" /> Acesso imediato</span>
          </div>
        </section>

        {/* FOOTER */}
        <footer className="border-t border-border py-10">
          <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
            <p className="font-mono mb-2">
              <span className="text-foreground font-bold">negócio.ia</span> | by Alex Priete
            </p>
            <p className="mb-1">© 2026 Alex Priete. Todos os direitos reservados.</p>
            <p className="text-xs max-w-2xl mx-auto">
              Os resultados mencionados não são garantia de ganhos futuros. Resultados dependem de dedicação e aplicação individual.
            </p>
          </div>
        </footer>
      </main>

      <CaptureModal open={modalOpen} onOpenChange={setModalOpen} />
    </div>
  );
};

export default Index;
