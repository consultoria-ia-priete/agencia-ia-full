import { useState, useEffect } from "react";
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
  Shield,
  CreditCard,
  Lock,
  Gift,
  Sparkles,
} from "lucide-react";

// =====================================================
// CONSTANTES / DATA
// =====================================================

const marqueeItems = [
  "8 ANOS DE CONSULTORIA",
  "R$ 187 MILHÕES FATURADOS POR CLIENTES",
  "3,5 MILHÕES DE CNPJs SEM IA NO BRASIL",
  "CRM FUNNELS EM 4 PAÍSES",
  "10 SQUADS ATIVOS",
  "598 AGENTES DE IA RODANDO AGORA",
];

const pixComprovantes = [
  "/assets/pix/pix-02.jpeg",
  "/assets/pix/pix-03.jpeg",
  "/assets/pix/pix-04.jpeg",
  "/assets/pix/pix-05.jpeg",
  "/assets/pix/pix-06.jpeg",
  "/assets/pix/pix-07.jpeg",
];

const idealFor = [
  "Vê a onda da IA chegando e sabe que tem algo enorme aí — mas ainda não sabe como transformar isso em dinheiro de verdade.",
  "Já tentou afiliado, drop ou infoproduto — e se frustrou. Não porque é incapaz, mas porque esses modelos dependem de uma audiência que você ainda não tem.",
  "Quer renda recorrente. Cliente que paga todo mês. Sem lançamento, sem algoritmo, sem virar refém de conteúdo.",
  "Sente que o mercado de IA está explodindo e quer entrar sem precisar virar programador.",
];

const notFor = [
  "Procura dinheiro fácil sem comprometimento. Aqui não tem atalho mágico.",
  "Gosta de acumular curso e nunca implementar. O método funciona pra quem faz.",
  "Não está disposto a fazer uma reunião com um empresário. O modelo exige conversa com empresa real. Se isso te paralisa, resolva isso antes de comprar.",
];

const cemiterio = [
  {
    title: "AFILIADO",
    img: "/assets/lapide-afiliado.png",
    alt: "Afiliado — modelo morto",
    body:
      "Queima dinheiro pra achar o produto campeão — e nunca encontra.",
  },
  {
    title: "DROPSHIPPING",
    img: "/assets/lapide-drop.png",
    alt: "Dropshipping — modelo morto",
    body:
      "Concorre com a Shopee, o ML e o TikTok Shop. Virou commodity.",
  },
  {
    title: "INFOPRODUTO",
    img: "/assets/lapide-info.png",
    alt: "Infoproduto — modelo morto",
    body:
      "O mercado sofisticou demais. Hoje você investe pesado só pra validar uma promessa e uma oferta — antes mesmo de saber se vende.",
  },
];

const triade = [
  {
    n: "01",
    title: "POSICIONAMENTO CERTEIRO B2B",
    body:
      "Você identifica um nicho específico — clínica, imobiliária, academia, e-commerce — e cria uma proposta de resultado irresistível pra esse setor.",
    why: "Empresas pagam por resultado, não por tecnologia. Quem fala pra todo mundo, não fecha contrato com ninguém.",
  },
  {
    n: "02",
    title: "FUNIL DO CONSULTOR (Método Caixa Rápido)",
    body:
      "Um processo de 7 passos — da prospecção ao fechamento — que transforma uma conversa de diagnóstico de 45 minutos em um contrato recorrente assinado.",
    why: "Você não espera o algoritmo te achar. Você vai atrás da empresa certa, com a dor certa, no momento certo.",
  },
  {
    n: "03",
    title: "SERVIÇO RECORRENTE IRRESISTÍVEL",
    body:
      "Você estrutura pacotes de IA como Serviço com mensalidade de R$1,5K a R$10K+ — onde o ROI é tão óbvio pra empresa que ela renova sem questionar.",
    why: "Vender pra CNPJ gera contratos muito maiores que vender pra CPF. Setup de R$5K na entrada + R$3K/mês de recorrência que empilha mês a mês, sem lançamento.",
  },
];

const modulos = [
  {
    n: "1",
    title: "Claude Code: do 0 aos Squads de Agentes de IA",
    price: "R$ 997",
    body:
      "Sua arma secreta. A mesma tela que eu uso pra rodar 10 clientes e 598 agentes ao mesmo tempo. Você sai sabendo construir squads que entregam o serviço pra você.",
  },
  {
    n: "2",
    title: "O Mapa dos Serviços de IA",
    price: "R$ 997",
    body:
      "Modele exatamente os serviços que eu entrego. Sem chutar. Sem reinventar. Você copia o que já está validado no mercado.",
  },
  {
    n: "3",
    title: "Posicionamento do Consultor de IA (Nicho High Ticket)",
    price: "R$ 997",
    body:
      "Como escolher o nicho certo onde a empresa tem dor, tem verba e tem urgência. Posicionamento que faz o preço sumir como objeção.",
  },
  {
    n: "4",
    title: "Máquina de Recorrência",
    price: "R$ 497",
    body:
      "A estrutura por trás dos contratos que renovam sem pergunta. Como ancorar valor mensal pra que o cliente nunca queira sair.",
  },
  {
    n: "5",
    title: "Funil do Consultor com Scripts Prontos",
    price: "R$ 3.000",
    body:
      "Da prospecção ao fechamento. Scripts testados em campo, e-mails, mensagens de outbound, anúncios. Plug and play.",
  },
  {
    n: "6",
    title: "Script de Reunião de Fechamento High Ticket",
    price: "R$ 997",
    body:
      "O passo-a-passo da reunião onde você sai com contrato assinado. O que dizer, quando dizer, como precificar na hora.",
  },
  {
    n: "7",
    title: "Apresentação Magnética Persuasiva",
    price: "R$ 997",
    body:
      "O deck que faz o empresário pedir pra fechar antes de você terminar de apresentar.",
  },
];

const bonusItems = [
  {
    icon: "lock",
    title: "Comunidade SSCIA",
    price: "INESTIMÁVEL",
    body: "A tribo onde os Consultores de IA trocam casos, fechamentos e bastidores em tempo real.",
  },
  {
    icon: "lock",
    title: "Mentoria Quinzenal Ao Vivo",
    price: "INESTIMÁVEL",
    body: "Tira-dúvidas direto comigo, ao vivo, duas vezes por mês.",
  },
  {
    icon: "gift",
    title: "Treinamentos Extras Ao Vivo Surpresa",
    price: "INESTIMÁVEL",
    body: "Aulas avançadas que aparecem quando o mercado pede.",
  },
  {
    icon: "gift",
    title: "1 Conta CRM Funnels — 30 dias grátis",
    price: "R$ 697",
    body: "A mesma plataforma que eu uso pra entregar o serviço pro cliente. Pra você testar, demonstrar, vender.",
  },
  {
    icon: "gift",
    title: "Modelo de Contrato pronto",
    price: "R$ 300",
    body: "O contrato que eu uso. Adaptado, assinado, recorrente.",
  },
  {
    icon: "gift",
    title: "Aula Bônus — Seu SaaS de ConsultorIA com sua marca",
    price: "BÔNUS",
    body: "Como eu construí a CRM Funnels — e como você pode construir o seu.",
  },
];

const stackValor: Array<[string, string]> = [
  ["Módulo 1 — Claude Code", "R$ 997"],
  ["Módulo 2 — Mapa dos Serviços", "R$ 997"],
  ["Módulo 3 — Posicionamento", "R$ 997"],
  ["Módulo 4 — Recorrência", "R$ 497"],
  ["Módulo 5 — Funil + Scripts", "R$ 3.000"],
  ["Módulo 6 — Fechamento", "R$ 997"],
  ["Módulo 7 — Apresentação", "R$ 997"],
  ["Bônus — CRM Funnels (30d)", "R$ 697"],
  ["Bônus — Contrato modelo", "R$ 300"],
  ["Comunidade SSCIA", "INESTIMÁVEL"],
  ["Mentorias quinzenais", "INESTIMÁVEL"],
  ["Aula SaaS próprio", "BÔNUS"],
];

const telegramCards = [
  {
    name: "Michel Góes",
    text: "Call Montro mais uma vez com o mestre Alex #calltiraduvidas",
    time: "22:09",
  },
  {
    name: "Kelly Korner",
    text: "@{{SEU_INSTAGRAM}} call top 👏👏👏!!!! Surra de conhecimento 👊👊",
    time: "22:05",
  },
  {
    name: "Jessé Pelerano",
    text: "CARA QUE COACHING CALL EXPETACULAR Muito obrigado @{{SEU_INSTAGRAM}} e Lucas Caboclo #praquemVocêVende?",
    time: "13:07",
  },
  {
    name: "Lucimar Santos",
    text: "Mudou minha visão essa call de hoje",
    time: "22:15",
  },
  {
    name: "Luis Fernando Matos",
    text: "Essa call com o Alex e o Marcelo foi sensacional top inesquecível vou rever 1000 vzs obrigado dois monstros de conhecimento e não se apegam de compartilhar só gratidão!!!!!",
    time: "22:36",
  },
  {
    name: "Marciel Matos",
    text: "Resumindo a Call hoje com o Alex @{{SEU_INSTAGRAM}} e @lucascabloco 👇👇 TUDO QUE EU PRECISA OUVIR para ter um norte com o cliente fechado hoje. Gratidão 🙏🙏🙏",
    time: "22:20",
  },
  {
    name: "Ian Santana",
    text: "Ótima a coaching call hj, agregando muito conhecimento à nossa bagagem como consultores, parabéns a Alex e todos os que contribuíram com dicas super importantes",
    time: "22:29",
  },
  {
    name: "Geraldo Cruz",
    text: "Parabens Alex.. Gratidão... Sempre...",
    time: "22:36",
  },
  {
    name: "Eduarda Azevedo",
    text: "Obrigada meninos, bom demais! Call épica, muito valor e conhecimento agregado",
    time: "22:16",
  },
  {
    name: "Rodrigo Kundera",
    text: "Coaching call braba demais hj, @{{SEU_INSTAGRAM}} é um mago",
    time: "22:08",
  },
  {
    name: "Anderson",
    text: "Fala mestre, passando aqui rapidinho só para agradecer o compartilhamento insano de hoje, muito obrigado!",
    time: "13:30",
  },
];

const faqs = [
  {
    q: "Eu preciso saber programar?",
    a: "Não. Você não vai construir IA — você vai entregar o resultado que ela produz. Ferramentas no-code, Claude Code prontinho, scripts mastigados. Se você sabe abrir uma aba do navegador, você consegue.",
  },
  {
    q: "Funciona pra quem não tem audiência nenhuma?",
    a: "Sim — esse é exatamente o ponto. O modelo é B2B outbound. Você vai atrás da empresa certa, não espera ela te achar. Audiência ajuda, mas não é pré-requisito.",
  },
  {
    q: "Quanto tempo até fechar o primeiro contrato?",
    a: "A média da turma fica entre 30 e 90 dias. Depende da sua execução. Tem aluno fechando na primeira semana, tem aluno levando 60 dias. O método está pronto — o ritmo é seu.",
  },
  {
    q: "Esse R$397 é vitalício mesmo?",
    a: "Sim, esse acesso é seu pra sempre. O preço de R$397 que está aberto hoje, não. Quando as vagas dessa janela fecharem, sobe pra R$997 e fica lá.",
  },
  {
    q: "Eu já tentei outros cursos e me frustrei. Por que esse seria diferente?",
    a: "Porque os outros te ensinam o 'o quê'. Aqui você sai com o 'como' — script de reunião, contrato modelo, funil pronto, scripts de prospecção. E com uma comunidade que te puxa pelo braço.",
  },
  {
    q: "Vou ter suporte direto com você?",
    a: "Sim. Mentorias quinzenais ao vivo, comigo. Não é gravado, não é IA respondendo. Você manda sua dúvida, eu respondo na sua frente.",
  },
];

// =====================================================
// HERO CTA REUSÁVEL (3 linhas + animate-pulse-glow)
// =====================================================

const HeroCTA = ({ onClick }: { onClick: () => void }) => (
  <Button
    size="lg"
    onClick={onClick}
    className="h-auto py-4 px-10 bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground hover:scale-[1.02] transition-transform animate-pulse-glow"
  >
    <div className="flex flex-col items-center gap-1 leading-tight">
      <span className="text-xl md:text-2xl font-extrabold tracking-wide">
        Eu quero ser ConsultorIA →
      </span>
      <span className="text-base md:text-lg font-bold">Só 42,28 em 12x</span>
      <span className="text-xs font-medium opacity-80">ou R$ 397,00 à vista</span>
    </div>
  </Button>
);

const LastChanceCTA = ({ onClick }: { onClick: () => void }) => (
  <Button
    size="lg"
    onClick={onClick}
    className="h-auto py-5 px-12 bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground hover:scale-[1.02] transition-transform animate-pulse-glow"
  >
    <div className="flex flex-col items-center gap-1 leading-tight">
      <span className="text-xl md:text-2xl font-extrabold tracking-wide">
        Toque Abaixo Para Garantir Sua Vaga →
      </span>
      <span className="text-base md:text-lg font-bold">Só 42,28 em 12x</span>
      <span className="text-xs font-medium opacity-80">ou R$ 397,00 à vista</span>
    </div>
  </Button>
);

// =====================================================
// COMPONENTE PRINCIPAL
// =====================================================

const Index = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const [revealed, setRevealed] = useState(false);

  useEffect(() => {
    const SRC =
      "https://scripts.converteai.net/5e845e96-a594-4af8-a9e4-9ef0a72ef454/players/6a0f40267366b8dd00bdd4e2/v4/player.js";
    if (document.querySelector(`script[src="${SRC}"]`)) return;
    const script = document.createElement("script");
    script.src = SRC;
    script.async = true;
    document.head.appendChild(script);
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      if (params.get("reveal") === "now") {
        setRevealed(true);
        return;
      }
    }

    // Gate amarrado ao TEMPO DE VÍDEO do vturb-smartplayer:
    // revela quando o player atinge 756s de conteúdo (12min36s — momento
    // exato em que a oferta é revelada no vídeo).
    // Se acelerarem pra 2x, currentTime chega lá em ~6,3 min reais.
    // Atalho de teste: ?gate=N força o disparo em N segundos de vídeo.
    const gateParam =
      typeof window !== "undefined"
        ? Number(new URLSearchParams(window.location.search).get("gate"))
        : NaN;
    const REVEAL_AT = gateParam > 0 ? gateParam : 756; // segundos de vídeo (12:36)
    let pollTimer: ReturnType<typeof setTimeout> | undefined;
    let fallbackTimer: ReturnType<typeof setTimeout> | undefined;
    let attempts = 0;

    const armVideoGate = () => {
      const sp = (window as any).smartplayer;
      if (typeof sp === "undefined" || !(sp.instances && sp.instances.length)) {
        attempts += 1;
        if (attempts >= 15) {
          // player nunca inicializou — fallback de segurança por tempo de página
          // (só dispara se o vturb falhar, pra nunca trancar a oferta de vez)
          fallbackTimer = setTimeout(() => setRevealed(true), REVEAL_AT * 1000);
          return;
        }
        pollTimer = setTimeout(armVideoGate, 1000);
        return;
      }
      const inst = sp.instances[0];
      let done = false;
      inst.on("timeupdate", () => {
        if (done) return; // para de processar depois que revelou
        if (inst.video && inst.video.currentTime >= REVEAL_AT) {
          done = true;
          setRevealed(true);
        }
      });
    };

    armVideoGate();
    return () => {
      if (pollTimer) clearTimeout(pollTimer);
      if (fallbackTimer) clearTimeout(fallbackTimer);
    };
  }, []);

  // Pausa o VSL quando o formulário abre — libera a main thread (digitação
  // sem lag) e silencia o vídeo que tocava atrás do modal.
  useEffect(() => {
    if (!modalOpen) return;
    try {
      const inst = (window as any).smartplayer?.instances?.[0];
      if (inst?.video?.pause) inst.video.pause();
      else if (typeof inst?.pause === "function") inst.pause();
    } catch {
      /* player ainda não pronto — ignora */
    }
  }, [modalOpen]);

  return (
    <div className="min-h-screen overflow-x-hidden bg-background text-foreground font-sans selection:bg-primary/30">
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none hidden md:block">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[140px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#3a1d12]/20 rounded-full blur-[140px]" />
      </div>

      <main className="relative z-10">
        {/* ====================================== */}
        {/* SEÇÃO 1 — NAV [SEMPRE]                  */}
        {/* ====================================== */}
        <nav className="sticky top-0 z-30 backdrop-blur-md bg-background/80 border-b border-border">
          <div className="container mx-auto px-4 py-2.5 flex items-center">
            <div className="font-mono text-sm sm:text-base md:text-lg whitespace-nowrap">
              <span className="font-bold">ConsultorIA</span>
              <span className="text-muted-foreground"> | by Alex Priete</span>
            </div>
          </div>
        </nav>

        {/* ====================================== */}
        {/* SEÇÃO 2 — HERO IDENTITÁRIO [SEMPRE]     */}
        {/* SEÇÃO 3 — VÍDEO VSL [SEMPRE]            */}
        {/* ====================================== */}
        <section className="container mx-auto px-4 py-3 md:py-6 text-center max-w-5xl">
          {/* Badge / pré-headline */}
          <div className="inline-flex items-center gap-2 px-2.5 md:px-3 py-1 mb-3 md:mb-4 text-[10px] sm:text-[11px] md:text-xs font-mono tracking-wide md:tracking-wider text-primary uppercase border rounded-full border-primary/30 bg-primary/10">
            <span className="whitespace-nowrap">NOVO MODELO DE NEGÓCIO DIGITAL · 2026</span>
          </div>

          {/* H1 */}
          <h1 className="text-2xl sm:text-3xl md:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.05] mb-3 md:mb-4">
            <span className="block text-foreground">
              Vire ConsultorIA e fature R$33K/mês em 90 dias
            </span>
            <span className="block text-foreground">vendendo IA como Serviço</span>
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
              para empresas reais.
            </span>
          </h1>

          {/* VTURB VSL — player ID vid-6a0f40267366b8dd00bdd4e2 */}
          <div className="relative max-w-xl md:max-w-2xl mx-auto mb-5 md:mb-6 rounded-2xl overflow-hidden border border-border bg-card/40">
            <vturb-smartplayer
              id="vid-6a0f40267366b8dd00bdd4e2"
              style={{ display: "block", margin: "0 auto", width: "100%" }}
            />
          </div>

        </section>

        {/* ===== GATE: tudo abaixo do vídeo só revela em 12:36 do player ===== */}
        {revealed && (
          <>
          {/* CTA — aparece com o reveal, logo abaixo do vídeo */}
          <section className="container mx-auto px-4 pb-10 text-center max-w-5xl">
            <div className="flex flex-col items-center gap-4">
              <HeroCTA onClick={() => setModalOpen(true)} />
              <div className="flex flex-wrap gap-x-6 gap-y-2 justify-center text-xs text-muted-foreground">
                <span className="inline-flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-primary" /> Acesso imediato
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-primary" /> Garantia incondicional de 7 dias
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <CreditCard className="w-3.5 h-3.5 text-primary" /> 12x no cartão
                </span>
              </div>
            </div>
          </section>

        {/* ====================================== */}
        {/* SEÇÃO 4 — TIRA DE PROVA PIX [SEMPRE]    */}
        {/* ====================================== */}
        <section className="container mx-auto px-4 py-12 md:py-16 max-w-5xl">
          <div className="text-center mb-8">
            <p className="font-mono text-xs text-primary mb-3 tracking-wider">
              // ENQUANTO VOCÊ LÊ ISSO, ESTÁ ENTRANDO:
            </p>
            <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
              Pix de R$1.249, R$4.425, R$2.478, R$4.997.
            </h2>
            <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Não são vendas de curso. É mensalidade entrando de empresas reais que pagam por
              resultado, todo mês.
            </p>
          </div>

          {/* Carrossel auto-scroll horizontal de comprovantes Pix */}
          <div className="relative overflow-hidden py-4 [mask-image:linear-gradient(to_right,transparent,black_10%,black_90%,transparent)]">
            <div
              className="flex gap-4 md:gap-6 animate-marquee whitespace-nowrap"
              style={{ width: "max-content" }}
            >
              {[...pixComprovantes, ...pixComprovantes].map((src, i) => (
                <div
                  key={i}
                  className="flex-shrink-0 h-[360px] md:h-[440px] rounded-2xl overflow-hidden border border-border bg-card shadow-lg shadow-primary/10 flex items-center justify-center"
                >
                  <img
                    src={src}
                    alt={`Comprovante Pix ${(i % pixComprovantes.length) + 1}`}
                    className="h-full w-auto object-contain"
                    loading="lazy"
                  />
                </div>
              ))}
            </div>
          </div>

          <p className="text-sm md:text-base text-muted-foreground/90 max-w-3xl mx-auto leading-relaxed mt-8 text-center">
            A guruzada ignora esse modelo porque não dá pra fazer lançamento gritando em palco. Mas é o
            único modelo digital que paga sua conta no dia 5 sem você refazer o trabalho. É{" "}
            <span className="text-foreground font-semibold">IA como Serviço</span> — recorrente,
            previsível, contratado.
          </p>
        </section>

        {/* ====================================== */}
        {/* SEÇÃO 3.5 — O MOMENTO                   */}
        {/* ====================================== */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-5xl">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <p className="font-mono text-xs text-primary mb-3 tracking-wider">
              // POR QUE AGORA — E NÃO DAQUI A DOIS ANOS:
            </p>
            <h2 className="text-3xl md:text-5xl font-extrabold leading-tight">
              A corrida pra implantar IA já começou nas empresas.{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                Quem entrega ainda não chegou.
              </span>
            </h2>

            <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
              Pensa comigo: empresa nenhuma escapa da IA agora. De todo tamanho, em todo nicho —
              todas precisam implantar, e pra ontem. Só que quando elas saem atrás de quem entrega
              de verdade... não acham quase ninguém.
            </p>

            <div className="space-y-4">
              <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
                As empresas estão prontas pra pagar:
              </p>
              <div className="flex flex-wrap justify-center gap-3">
                <span className="border border-primary/30 bg-primary/10 text-primary rounded-full px-3 py-1 text-sm">
                  têm verba
                </span>
                <span className="border border-primary/30 bg-primary/10 text-primary rounded-full px-3 py-1 text-sm">
                  têm urgência
                </span>
                <span className="border border-primary/30 bg-primary/10 text-primary rounded-full px-3 py-1 text-sm">
                  têm medo de ficar pra trás
                </span>
              </div>
              <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
                E do outro lado da mesa? Ninguém sentado. É esse vazio que te paga. E vazio assim
                não dura — uma hora ele enche.
              </p>
            </div>

            <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
              O caminho pra ocupar essa cadeira não é o que te venderam. Não é{" "}
              <span className="font-semibold text-foreground">virar programador</span>, não é{" "}
              <span className="font-semibold text-foreground">construir audiência</span>, não é{" "}
              <span className="font-semibold text-foreground">postar conteúdo todo dia</span>. É
              outra coisa, totalmente: você monta{" "}
              <span className="font-semibold text-foreground">
                Squads de Agentes de IA com Claude Code
              </span>{" "}
              pra entregar resultado real pras empresas — o mesmo método que já ajudou negócios a
              faturar{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39] font-extrabold">
                R$187 milhões
              </span>
              .
            </p>
          </div>

          <div className="mt-10 md:mt-12 max-w-4xl mx-auto">
            <div className="rounded-2xl overflow-hidden border border-border bg-card/40 shadow-lg shadow-primary/10">
              <img
                src="/assets/agentes-de-ia.png"
                alt="Squads de Agentes de IA orquestrados no Claude Code"
                className="w-full h-auto"
                loading="lazy"
              />
            </div>
            <p className="font-mono text-xs text-muted-foreground text-center mt-3">
              // SEUS SQUADS DE AGENTES, ORQUESTRADOS EM PRODUÇÃO
            </p>
          </div>
        </section>

        {/* ====================================== */}
        {/* SEÇÃO 5 — MARQUEE DE AUTORIDADE [SEMPRE]*/}
        {/* ====================================== */}
        <section className="border-y border-border bg-card/50 overflow-hidden py-4">
          <div className="flex animate-marquee whitespace-nowrap">
            {[...marqueeItems, ...marqueeItems].map((item, i) => (
              <div
                key={i}
                className="flex items-center gap-4 px-6 text-sm text-muted-foreground font-mono"
              >
                <span>{item}</span>
                <span className="text-primary">◆</span>
              </div>
            ))}
          </div>
        </section>

        {/* ====================================== */}
        {/* SEÇÃO 6 — PRA QUEM É / NÃO É [SEMPRE]   */}
        {/* ====================================== */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-6xl">
          <div className="text-center mb-10">
            <p className="font-mono text-xs text-primary mb-3 tracking-wider">
              // PENSA COMIGO ANTES DE SEGUIR:
            </p>
            <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
              Eu não quero todo mundo aqui dentro. <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">Eu quero quem tá pronto pra parar de adiar.</span>
            </h2>
            <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Os 4 itens da esquerda são o retrato de quem entra pra SSCIA e em 90 dias tá faturando de verdade. Os da direita? São o motivo de muita gente nunca sair do lugar. Seja sincero com você.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-10">
            {/* Coluna ESQUERDA — PRA VOCÊ */}
            <div className="bg-gradient-to-br from-primary/10 via-card to-card border border-primary/40 rounded-2xl p-7">
              <h3 className="text-2xl font-extrabold text-primary mb-6 flex items-center gap-2">
                <CheckCircle2 className="w-6 h-6" /> Pra você se:
              </h3>
              <ul className="space-y-4">
                {idealFor.map((it, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm md:text-base text-muted-foreground leading-relaxed">
                    <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                    <span>{it}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Coluna DIREITA — NÃO É PRA VOCÊ */}
            <div className="bg-card/60 border border-red-500/30 rounded-2xl p-7">
              <h3 className="text-2xl font-extrabold text-destructive mb-6 flex items-center gap-2">
                <XCircle className="w-6 h-6" /> NÃO é pra você se:
              </h3>
              <ul className="space-y-4">
                {notFor.map((it, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm md:text-base text-muted-foreground leading-relaxed">
                    <XCircle className="w-5 h-5 text-red-500/70 flex-shrink-0 mt-0.5" />
                    <span>{it}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <p className="text-base md:text-lg text-muted-foreground/90 max-w-3xl mx-auto leading-relaxed text-center">
            Tá tudo bem se não for o seu momento. Mas se os 4 da esquerda bateram em cheio — fica
            comigo. O que vem agora vai mudar a forma como você enxerga o digital.
          </p>
        </section>

        {/* ====================================== */}
        {/* SEÇÃO 7 — CEMITÉRIO DE PROMESSAS        */}
        {/* ====================================== */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-6xl">
          <div className="text-center mb-12">
            <p className="font-mono text-xs text-primary mb-3 tracking-wider">
              // A VERDADE QUE A GURUZADA NÃO TE CONTA:
            </p>
            <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
              O mercado digital virou um{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500">
                cemitério de promessas.
              </span>
            </h2>
            <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Três modelos quebrados, vendidos a peso de ouro. Veja por que cada um te deixa correndo
              no lugar.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-12">
            {cemiterio.map((c) => (
              <div
                key={c.title}
                className="bg-card/60 border border-red-500/20 rounded-2xl p-7 text-center"
              >
                <img
                  src={c.img}
                  alt={c.alt}
                  className="w-full max-w-[220px] mx-auto h-auto object-contain mb-5"
                  loading="lazy"
                />
                <p className="text-sm text-muted-foreground leading-relaxed text-center">{c.body}</p>
              </div>
            ))}
          </div>

          <div className="bg-gradient-to-br from-primary/10 via-card to-card border border-primary/40 rounded-2xl p-7 md:p-10 text-center">
            <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
              Enquanto isso, a maior oportunidade desde a chegada da internet está aberta agora:{" "}
              <span className="text-foreground font-bold">
                3,5 milhões de CNPJs no Brasil precisam de IA — e quase nenhum sabe por onde começar.
              </span>{" "}
              Eles têm verba. Têm urgência. Têm problema real. O gap é gigante. E ele tem nome.
            </p>
          </div>
        </section>

        {/* ====================================== */}
        {/* SEÇÃO 8 — A JANELA ESTÁ ABRINDO         */}
        {/* ====================================== */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-6xl">
          <div className="text-center mb-12">
            <p className="font-mono text-xs text-primary mb-3 tracking-wider">
              // A MATEMÁTICA QUE NINGUÉM TE MOSTROU:
            </p>
            <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
              Setup de R$5K. Recorrência de R$3K.{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                Acumulando.
              </span>
            </h2>
            <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Pensa comigo: cada cliente novo entra com R$5K de setup + R$3K/mês. Os recorrentes do
              mês passado somam com os novos. É assim que você chega nos R$33K.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-card border border-border rounded-2xl p-7 text-center hover:border-primary/40 transition-colors">
              <p className="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39] mb-3 leading-tight">
                R$5K + R$3K/mês
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                <span className="text-foreground font-semibold">setup único de R$5K + R$3K/mês</span>{" "}
                por cliente. Toda vez que você fecha, soma os dois.
              </p>
            </div>
            <div className="bg-card border border-border rounded-2xl p-7 text-center hover:border-primary/40 transition-colors">
              <p className="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39] mb-3 leading-tight">
                Empilha
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                recorrência que <span className="text-foreground font-semibold">EMPILHA mês a mês</span> —
                clientes novos + antigos somando todo mês.
              </p>
            </div>
            <div className="bg-card border border-border rounded-2xl p-7 text-center hover:border-primary/40 transition-colors">
              <p className="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39] mb-3 leading-tight">
                R$33K/mês
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                é o <span className="text-foreground font-semibold">acúmulo</span>, não um número mágico
                de clientes: setups dos novos + mensalidades dos que já entraram.
              </p>
            </div>
          </div>

          <p className="text-base md:text-lg text-muted-foreground/90 max-w-3xl mx-auto leading-relaxed text-center">
            O maior erro dos "consultores de IA" que estão por aí é aparecer na reunião pra vender
            tecnologia. Empresa não quer ChatGPT. Quer o atendimento parar de falhar. Quer o no-show
            cair. Quer o follow-up acontecer sozinho.{" "}
            <span className="text-foreground font-semibold">
              Quando você fala a língua do resultado — não da ferramenta — a objeção de preço some.
            </span>
          </p>
        </section>

        {/* ====================================== */}
        {/* SEÇÃO 9 — SOBRE O ALEX [SEMPRE]         */}
        {/* ====================================== */}
        <section className="container mx-auto px-4 py-16 md:py-20 max-w-5xl">
          <div className="text-center mb-10">
            <p className="font-mono text-xs text-primary mb-3 tracking-wider">
              // QUEM TÁ DO OUTRO LADO:
            </p>
            <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
              Larguei a TI. Errei com afiliado. Errei com drop.{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                Aí descobri o que ninguém estava ensinando.
              </span>
            </h2>
            <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              8 anos depois, são R$187 milhões ajudados a faturar pra empresas no Brasil e nos EUA —
              e uma plataforma própria.
            </p>
          </div>

          <div className="grid md:grid-cols-[280px_1fr] gap-8 items-start bg-card border border-border rounded-2xl p-7 md:p-10">
            <div>
              <img
                src="/images/alex.jpg"
                alt="Alex Priete"
                className="w-full rounded-2xl object-cover aspect-square shadow-xl"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = "none";
                }}
              />
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-1">Alex Priete</h3>
              <p className="font-mono text-xs text-muted-foreground mb-5">
                // Founder · CRM Funnels · SSCIA · ConsultorIA
              </p>
              <div className="space-y-4 text-muted-foreground leading-relaxed">
                <p>
                  Meu nome é Alex Priete. Eu viajava mais de 100km por dia, mal via minha família.
                  Larguei pra empreender no digital. Me frustrei com afiliado. Me frustrei com drop.
                  Cada erro me ensinou algo que nenhum curso me ensinou.
                </p>
                <p>
                  Quando juntei tudo e comecei a vender tecnologia e automação direto pra empresas —
                  funis simples, automação, IA — os resultados vieram de um jeito que eu nunca
                  imaginei. Contratos acima de R$3K/mês. Recorrência. Previsibilidade.
                </p>
                <p>
                  Com essa experiência, eu construí a{" "}
                  <span className="text-foreground font-semibold">CRM Funnels</span> — plataforma de
                  automação, atendimento com IA e CRM hoje usada em vários países. E fundei a{" "}
                  <span className="text-foreground font-semibold">
                    SSCIA — Sociedade Secreta dos Consultores de IA.
                  </span>
                </p>
                <p>
                  Hoje, em vez de guardar esse método, eu decidi ensinar pra quem está pronto pra
                  entrar nessa onda antes que ela feche.
                </p>
              </div>
            </div>
          </div>
        </section>

            {/* ====================================== */}
            {/* SEÇÃO 10 — TRÍADE AIAAS [GATE]         */}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-16 md:py-24 max-w-6xl">
              <div className="text-center mb-12">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // O MECANISMO COMPLETO:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  Tríade AIAAS —{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    Artificial Intelligence As A Service.
                  </span>
                </h2>
                <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                  A evolução do SaaS. O modelo que ninguém no mercado digital está ensinando direito.
                  Três pilares que, juntos, formam um negócio enxuto, escalável e sem depender de
                  seguidores.
                </p>
              </div>

              {/* Cockpit MESTRE */}
              <div className="max-w-4xl mx-auto mb-10 rounded-2xl overflow-hidden border border-border shadow-2xl shadow-primary/10">
                <img
                  src="/assets/cockpit-mestre.png"
                  alt="Cockpit MESTRE — 10 clientes, 598 agentes de IA, 7 squads rodando"
                  className="w-full h-auto"
                  loading="lazy"
                />
              </div>
              <p className="font-mono text-xs text-muted-foreground text-center mb-12">
                // o cockpit que orquestra 598 agentes de IA em produção
              </p>

              <div className="grid md:grid-cols-3 gap-6 mb-10">
                {triade.map((p) => (
                  <div
                    key={p.n}
                    className="bg-card border border-border rounded-2xl p-7 hover:border-primary/40 transition-colors relative overflow-hidden"
                  >
                    <div className="absolute -top-10 -right-10 w-32 h-32 bg-primary/10 rounded-full blur-2xl" />
                    <p className="font-mono text-xs text-muted-foreground mb-2 relative z-10">
                      PILAR {p.n}
                    </p>
                    <h3 className="text-lg md:text-xl font-extrabold mb-4 text-foreground relative z-10 leading-tight">
                      {p.title}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed mb-4 relative z-10">
                      {p.body}
                    </p>
                    <p className="text-xs text-primary leading-relaxed relative z-10">
                      <span className="font-semibold">Por que funciona:</span> {p.why}
                    </p>
                  </div>
                ))}
              </div>

              <p className="text-base md:text-lg text-foreground/90 max-w-3xl mx-auto leading-relaxed text-center font-medium">
                Esses 3 pilares formam o ConsultorIA — IA como Serviço enxuto, escalável e sem
                depender de seguidores.
              </p>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 11 — MÓDULOS 1-7 [GATE]          */}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-16 md:py-20 max-w-6xl">
              <div className="text-center mb-12">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // TUDO QUE VOCÊ LEVA PRA CASA:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  7 módulos. 1 método validado.{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    Zero enrolação.
                  </span>
                </h2>
                <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                  Cada módulo resolve uma etapa específica da sua transformação em ConsultorIA. Nada
                  genérico.
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-5">
                {modulos.map((m) => (
                  <div
                    key={m.n}
                    className="bg-card border border-border rounded-2xl p-6 hover:border-primary/40 transition-colors flex gap-4"
                  >
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-[#FF5C39] flex items-center justify-center font-extrabold text-primary-foreground text-lg">
                        {m.n}
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-3 mb-2">
                        <h3 className="text-base md:text-lg font-bold leading-tight">
                          MÓDULO {m.n} — {m.title}
                        </h3>
                        <span className="font-mono text-xs text-primary whitespace-nowrap font-bold">
                          {m.price}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground leading-relaxed">{m.body}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 12 — BÔNUS + SSCIA [GATE]         */}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-16 md:py-20 max-w-6xl">
              <div className="text-center mb-12">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // E NÃO PARA POR AÍ:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  Você também entra na{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    SSCIA.
                  </span>
                </h2>
                <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                  Sociedade Secreta dos Consultores de IA. Não é grupo de WhatsApp. É o seu novo
                  círculo profissional.
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-5">
                {bonusItems.map((b, i) => (
                  <div
                    key={i}
                    className="bg-card border border-border rounded-2xl p-6 hover:border-primary/40 transition-colors flex gap-4"
                  >
                    <div className="flex-shrink-0">
                      {b.icon === "lock" ? (
                        <Lock className="w-7 h-7 text-primary" />
                      ) : (
                        <Gift className="w-7 h-7 text-orange-400" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-3 mb-2">
                        <h3 className="text-base md:text-lg font-bold leading-tight">{b.title}</h3>
                        <span
                          className={`font-mono text-xs whitespace-nowrap font-bold ${
                            b.price === "INESTIMÁVEL"
                              ? "text-primary"
                              : b.price === "BÔNUS"
                              ? "text-orange-400"
                              : "text-muted-foreground"
                          }`}
                        >
                          {b.price}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground leading-relaxed">{b.body}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 13 — STACK DE VALOR [GATE]        */}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-16 md:py-20 max-w-4xl">
              <div className="text-center mb-10">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // SE VOCÊ FOSSE COMPRAR ISSO EM PARTES:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  Valor total:{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    R$ 9.479,00 + INESTIMÁVEL.
                  </span>
                </h2>
                <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                  Soma só do que tem preço. A comunidade, as mentorias e os treinamentos ao vivo nem
                  entram nessa conta.
                </p>
              </div>

              <div className="bg-card border border-border rounded-2xl p-6 md:p-8">
                <ul className="divide-y divide-border/60">
                  {stackValor.map(([label, price]) => (
                    <li
                      key={label}
                      className="flex justify-between items-center py-3 gap-3 text-sm md:text-base"
                    >
                      <span className="text-muted-foreground">{label}</span>
                      <span
                        className={`font-mono whitespace-nowrap font-semibold text-right ${
                          price === "INESTIMÁVEL"
                            ? "text-primary"
                            : price === "BÔNUS"
                            ? "text-orange-400"
                            : "text-foreground"
                        }`}
                      >
                        {price}
                      </span>
                    </li>
                  ))}
                </ul>
                <div className="flex justify-between items-center pt-5 mt-3 border-t-2 border-primary/40 text-base md:text-lg">
                  <span className="font-extrabold text-foreground">TOTAL</span>
                  <span className="font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39] text-right">
                    R$ 9.479 + INESTIMÁVEL
                  </span>
                </div>
              </div>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 14 — OFERTA R$397 [GATE]          */}
            {/* ====================================== */}
            <section id="oferta" className="container mx-auto px-4 py-16 md:py-20 max-w-3xl">
              <div className="text-center mb-8">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // MAS VOCÊ NÃO VAI PAGAR NEM METADE:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  De{" "}
                  <span className="line-through text-muted-foreground">R$ 9.479</span> por{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    R$ 397.
                  </span>
                </h2>
                <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                  Hoje, em condição única de lançamento. Depois, sobe pra R$ 997 e não volta mais.
                </p>
              </div>

              <div className="bg-card border-2 border-primary/40 rounded-2xl p-7 md:p-10 animate-card-glow">
                <p className="text-sm md:text-base text-muted-foreground leading-relaxed mb-6">
                  Com{" "}
                  <span className="text-foreground font-bold">um único cliente</span>, o setup de R$5K
                  já paga o investimento. Conforme você{" "}
                  <span className="text-foreground font-bold">acumula contratos de R$3K/mês</span>, a
                  recorrência empilha e você chega nos R$33K. O ROI está na sua frente. Você só
                  precisa decidir se vai ou não.
                </p>

                <div className="text-center mb-7">
                  <p className="text-sm text-muted-foreground mb-1">de</p>
                  <p className="text-2xl text-muted-foreground line-through mb-3">R$ 9.479,00</p>
                  <p className="text-sm text-foreground mb-1">por apenas</p>
                  <p className="mb-2">
                    <span className="text-3xl text-muted-foreground align-top">R$</span>
                    <span className="text-7xl md:text-8xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                      397
                    </span>
                    <span className="text-3xl text-muted-foreground align-top">,00</span>
                  </p>
                  <p className="font-mono text-xs text-muted-foreground">
                    // à vista · ou 12x de R$ 42,28
                  </p>
                </div>

                <div className="flex justify-center mb-5">
                  <HeroCTA onClick={() => setModalOpen(true)} />
                </div>

                <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-muted-foreground font-mono">
                  <span className="inline-flex items-center gap-1.5">
                    <CheckCircle2 className="w-3 h-3 text-primary" /> Acesso imediato
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <Lock className="w-3 h-3 text-primary" /> Pagamento seguro
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <Sparkles className="w-3 h-3 text-primary" /> Entra na SSCIA hoje
                  </span>
                </div>
              </div>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 15 — GARANTIA 7d [GATE]           */}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-12 md:py-16 max-w-4xl">
              <div className="text-center mb-8">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // ZERO RISCO PRA VOCÊ:
                </p>
                <h2 className="text-3xl md:text-4xl font-extrabold leading-tight mb-4">
                  7 dias pra decidir.{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    Se não for pra você, devolvo cada centavo.
                  </span>
                </h2>
              </div>

              <div className="bg-card/60 border border-primary/30 rounded-2xl p-7 md:p-9 flex flex-col md:flex-row items-start gap-6">
                <Shield className="w-14 h-14 text-primary flex-shrink-0" />
                <div>
                  <p className="text-base md:text-lg text-muted-foreground leading-relaxed mb-4">
                    Entra agora, assiste tudo, entra na comunidade, vê os scripts. Se nos primeiros 7
                    dias você sentir que isso não é pra você — me manda um email, eu devolvo. Sem
                    pergunta, sem fricção, sem julgamento.
                  </p>
                  <p className="text-sm md:text-base text-foreground/90 leading-relaxed font-medium">
                    Eu prefiro perder o seu dinheiro do que perder o seu tempo. Quem entra na SSCIA
                    tem que estar dentro com vontade — não preso por compra. Esse é o trato.
                  </p>
                </div>
              </div>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 16 — PROVA SOCIAL TELEGRAM [GATE]*/}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-16 md:py-20 max-w-5xl">
              <div className="text-center mb-12">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // O QUE DIZEM DOS ENCONTROS:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  Não tem ator. Não tem script.{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    É o que rolou na call, ao vivo.
                  </span>
                </h2>
                <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                  O que as pessoas disseram logo depois dos nossos encontros ao vivo. Sem edição, sem combinar nada antes.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
                {telegramCards.map((c, i) => (
                  <div
                    key={i}
                    className="bg-card border border-border rounded-2xl p-5 flex items-start gap-3 hover:border-primary/40 transition-colors"
                  >
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-[#FF5C39] flex items-center justify-center font-bold text-primary-foreground flex-shrink-0">
                      {c.name.charAt(0)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-baseline justify-between gap-2 mb-1">
                        <p className="font-bold text-sm text-foreground truncate">{c.name}</p>
                        <p className="font-mono text-xs text-muted-foreground flex-shrink-0">
                          {c.time}
                        </p>
                      </div>
                      <p className="text-sm text-muted-foreground leading-relaxed break-words">
                        {c.text}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 17 — FAQ [GATE]                   */}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-16 md:py-20 max-w-3xl">
              <div className="text-center mb-10">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // AS PERGUNTAS QUE TODO MUNDO FAZ:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  Antes de você decidir,{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    resolve essas 6 aqui.
                  </span>
                </h2>
              </div>
              <Accordion
                type="single"
                collapsible
                className="bg-card border border-border rounded-2xl px-6 md:px-8"
              >
                {faqs.map((f, i) => (
                  <AccordionItem key={i} value={`q-${i}`}>
                    <AccordionTrigger className="text-base md:text-lg font-bold text-left">
                      {f.q}
                    </AccordionTrigger>
                    <AccordionContent className="text-sm md:text-base text-muted-foreground leading-relaxed">
                      {f.a}
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </section>

            {/* ====================================== */}
            {/* SEÇÃO 18 — DUAS OPÇÕES + LAST CHANCE   */}
            {/* ====================================== */}
            <section className="container mx-auto px-4 py-16 md:py-20 max-w-6xl">
              <div className="text-center mb-12">
                <p className="font-mono text-xs text-primary mb-3 tracking-wider">
                  // A PARTIR DAQUI VOCÊ TEM DUAS OPÇÕES:
                </p>
                <h2 className="text-3xl md:text-5xl font-extrabold leading-tight mb-4">
                  Continua tentando sozinho. Ou{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                    entra agora.
                  </span>
                </h2>
                <p className="text-base md:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                  Não tem caminho do meio. Quem fica parado, fica parado.
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-6 mb-12">
                {/* OPÇÃO 1 */}
                <div className="bg-card/60 border border-red-500/30 rounded-2xl p-7">
                  <p className="font-mono text-xs text-destructive mb-3 tracking-wider">// OPÇÃO 1</p>
                  <h3 className="text-2xl font-extrabold text-destructive mb-5 leading-tight">
                    Continua sozinho.
                  </h3>
                  <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
                    Testa método por método. Erra. Perde meses. Perde dinheiro. Torce pra que a janela
                    do mercado de IA ainda esteja aberta quando você descobrir como entrar.
                  </p>
                </div>
                {/* OPÇÃO 2 */}
                <div className="bg-gradient-to-br from-primary/10 via-card to-card border border-primary/40 rounded-2xl p-7">
                  <p className="font-mono text-xs text-primary mb-3 tracking-wider">// OPÇÃO 2</p>
                  <h3 className="text-2xl font-extrabold text-primary mb-5 leading-tight">
                    Entra agora.
                  </h3>
                  <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
                    Implementa um método validado. Scripts prontos. Funis prontos. Comunidade ativa.
                    Suporte ao vivo. Primeiro contrato em 30 a 90 dias.
                  </p>
                </div>
              </div>

              <div className="max-w-3xl mx-auto text-center mb-10">
                <p className="text-base md:text-lg text-muted-foreground leading-relaxed mb-4">
                  É outra coisa, totalmente.{" "}
                  <span className="text-foreground font-semibold">
                    O mercado de IA não vai esperar você decidir.
                  </span>{" "}
                  Os 3,5 milhões de CNPJs sem IA vão ser atendidos por alguém. Pode ser por você.
                </p>
                <p className="text-base md:text-lg text-muted-foreground leading-relaxed">
                  Quando as primeiras vagas dessa janela fecharem, o valor volta pra R$997.{" "}
                  <span className="text-foreground font-semibold">
                    Quem garante agora trava o menor preço que esse treinamento vai ter.
                  </span>
                </p>
              </div>

              <div className="flex flex-col items-center gap-5">
                <LastChanceCTA onClick={() => setModalOpen(true)} />
                <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-muted-foreground font-mono">
                  <span className="inline-flex items-center gap-1.5">
                    <CreditCard className="w-3 h-3 text-primary" /> Cartão ou PIX
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <Shield className="w-3 h-3 text-primary" /> Garantia de 7 dias
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <CheckCircle2 className="w-3 h-3 text-primary" /> Acesso imediato
                  </span>
                </div>
              </div>

              <div className="text-center mt-12">
                <p className="text-lg md:text-xl text-foreground font-medium mb-2">
                  Te vejo do outro lado.
                </p>
                <p className="text-base text-muted-foreground">
                  <span className="text-foreground font-bold">— Alex Priete</span>
                </p>
                <p className="font-mono text-xs text-muted-foreground mt-1">
                  Fundador da SSCIA · CEO da CRM Funnels · @{{SEU_INSTAGRAM}}
                </p>
              </div>
            </section>
          </>
        )}

        {/* ====================================== */}
        {/* SEÇÃO 19 — FOOTER [SEMPRE]              */}
        {/* ====================================== */}
        <footer className="border-t border-border py-10 mt-8">
          <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
            <p className="font-mono mb-2">
              <span className="text-foreground font-bold">ConsultorIA</span> by Alex Priete — SSCIA ·
              @{{SEU_INSTAGRAM}}
            </p>
            <p className="mb-1">© 2026 Alex Priete · CRM Funnels — Todos os direitos reservados.</p>
            <p className="text-xs max-w-2xl mx-auto mb-2">
              Política de Privacidade · Termos · Contato
            </p>
            <p className="text-xs max-w-2xl mx-auto">
              Os resultados mencionados não são garantia de ganhos futuros. Resultados dependem de
              dedicação e aplicação individual.
            </p>
          </div>
        </footer>
      </main>

      <CaptureModal open={modalOpen} onOpenChange={setModalOpen} />
    </div>
  );
};

export default Index;
