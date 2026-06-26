import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Lock, CreditCard, Zap, Flame, Sparkles, Target } from "lucide-react";
import { profileDescriptions, offerContent, type ProfileType } from "@/data/quizData";

interface ResultScreenProps {
  name: string;
  profileType: ProfileType;
  email?: string;
  phone?: string;
}

const TRACKER_BASE = "https://{{TRACKING_DOMAIN}}";

const readCookie = (key: string): string => {
  if (typeof document === "undefined") return "";
  for (const part of document.cookie.split(";")) {
    const eq = part.indexOf("=");
    if (eq < 0) continue;
    if (part.slice(0, eq).trim() === key) {
      return decodeURIComponent(part.slice(eq + 1).trim());
    }
  }
  return "";
};

const buildCheckoutUrl = (baseUrl: string, trk: string, urlParams: URLSearchParams): string => {
  const url = new URL(baseUrl);
  url.searchParams.set("utm_content", trk);
  // Pass through originating UTMs so Lastlink echoes them back in the webhook
  for (const k of ["utm_source", "utm_medium", "utm_campaign", "utm_term"]) {
    const v = urlParams.get(k);
    if (v) url.searchParams.set(k, v);
  }
  return url.toString();
};

const COUNTDOWN_MINUTES = 15;
const COUNTDOWN_KEY = "quiz-negocio-ia-deadline";

const useCountdown = () => {
  const [remaining, setRemaining] = useState<number>(() => {
    if (typeof window === "undefined") return COUNTDOWN_MINUTES * 60 * 1000;
    const stored = window.localStorage.getItem(COUNTDOWN_KEY);
    let deadline = stored ? parseInt(stored, 10) : 0;
    if (!deadline || deadline < Date.now()) {
      deadline = Date.now() + COUNTDOWN_MINUTES * 60 * 1000;
      window.localStorage.setItem(COUNTDOWN_KEY, String(deadline));
    }
    return deadline - Date.now();
  });

  useEffect(() => {
    const stored = window.localStorage.getItem(COUNTDOWN_KEY);
    const deadline = stored ? parseInt(stored, 10) : Date.now() + COUNTDOWN_MINUTES * 60 * 1000;
    const tick = () => {
      const diff = deadline - Date.now();
      setRemaining(diff > 0 ? diff : 0);
    };
    tick();
    const id = window.setInterval(tick, 1000);
    return () => window.clearInterval(id);
  }, []);

  const totalSeconds = Math.max(0, Math.floor(remaining / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return {
    minutes: String(minutes).padStart(2, "0"),
    seconds: String(seconds).padStart(2, "0"),
    expired: remaining <= 0,
  };
};

const SuccessGauge = ({ percent }: { percent: number }) => {
  const radius = 90;
  const circumference = Math.PI * radius;
  const offset = circumference - (percent / 100) * circumference;

  return (
    <div className="relative w-full max-w-[280px] mx-auto">
      <svg viewBox="0 0 220 130" className="w-full h-auto">
        <defs>
          <linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(15 63% 60%)" />
            <stop offset="100%" stopColor="hsl(15 63% 70%)" />
          </linearGradient>
          <filter id="gauge-glow">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        {/* Track */}
        <path
          d="M 20 110 A 90 90 0 0 1 200 110"
          fill="none"
          stroke="hsl(20 12% 18%)"
          strokeWidth="14"
          strokeLinecap="round"
        />
        {/* Progress */}
        <path
          d="M 20 110 A 90 90 0 0 1 200 110"
          fill="none"
          stroke="url(#gauge-gradient)"
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          filter="url(#gauge-glow)"
          style={{ transition: "stroke-dashoffset 1.2s ease-out" }}
        />
        {/* Tick labels */}
        <text x="20" y="125" fontSize="10" fill="hsl(20 8% 52%)" textAnchor="middle">
          0
        </text>
        <text x="65" y="35" fontSize="10" fill="hsl(20 8% 52%)" textAnchor="middle">
          25
        </text>
        <text x="110" y="20" fontSize="10" fill="hsl(20 8% 52%)" textAnchor="middle">
          50
        </text>
        <text x="155" y="35" fontSize="10" fill="hsl(20 8% 52%)" textAnchor="middle">
          75
        </text>
        <text x="200" y="125" fontSize="10" fill="hsl(20 8% 52%)" textAnchor="middle">
          100
        </text>
      </svg>
      <div className="absolute inset-x-0 bottom-2 text-center">
        <span className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
          {percent}%
        </span>
      </div>
    </div>
  );
};

const renderBoldMarkdown = (text: string) => {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return (
        <strong key={i} className="text-foreground font-bold">
          {part.slice(2, -2)}
        </strong>
      );
    }
    return <span key={i}>{part}</span>;
  });
};

export const ResultScreen = ({ name, profileType, email, phone }: ResultScreenProps) => {
  void email;
  void phone;
  const profile = profileDescriptions[profileType];
  const firstName = name.split(" ")[0];
  const { minutes, seconds, expired } = useCountdown();
  const [checkoutUrl, setCheckoutUrl] = useState<string>(offerContent.ctaUrl);

  // Generate trk + persist checkout_session in the tracking stack BEFORE
  // the user clicks the buy button. When Lastlink echoes utm_content back
  // in the webhook payload, the adapter looks up this checkout_session row
  // and enriches the purchase with fbp/fbc/session_id → Meta CAPI fires.
  useEffect(() => {
    if (typeof window === "undefined") return;
    const trk = crypto.randomUUID();
    const urlParams = new URLSearchParams(window.location.search);

    setCheckoutUrl(buildCheckoutUrl(offerContent.ctaUrl, trk, urlParams));

    const fbp = readCookie("_fbp");
    const fbc = readCookie("_fbc");
    const externalId = readCookie("_krob_eid");

    fetch(`${TRACKER_BASE}/checkout-session`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        trk,
        fbp,
        fbc,
        external_id: externalId,
        utm_source: urlParams.get("utm_source") || "",
        utm_medium: urlParams.get("utm_medium") || "",
        utm_campaign: urlParams.get("utm_campaign") || "",
        utm_content: trk,
        utm_term: urlParams.get("utm_term") || "",
        event_source_url: window.location.href,
      }),
    }).catch((err) => {
      console.error("checkout-session failed:", err);
    });
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Cronômetro fixo */}
      <div className="sticky top-2 z-20 mb-8">
        <div className="bg-gradient-to-r from-red-950/90 via-red-900/90 to-red-950/90 backdrop-blur border border-red-500/40 rounded-xl px-4 py-3 flex items-center justify-center gap-3 shadow-lg">
          <Flame className="w-5 h-5 text-red-400 flex-shrink-0" />
          <span className="text-sm md:text-base font-medium text-red-100">
            {expired ? "Oferta encerrando" : "Esta oferta especial expira em"}
          </span>
          <span className="text-xl md:text-2xl font-mono font-bold text-white tabular-nums">
            {minutes}:{seconds}
          </span>
        </div>
      </div>

      {/* Diagnóstico */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center px-4 py-1.5 mb-6 text-xs font-medium tracking-wider text-primary uppercase border rounded-full border-primary/30 bg-primary/10">
          <span className="text-primary mr-2">//</span>
          SEU DIAGNÓSTICO: {profile.profileTag}
        </div>
        <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight max-w-3xl mx-auto leading-tight">
          {profile.diagnosisHeadline(firstName)}
        </h1>
      </div>

      {/* Cards lado a lado */}
      <div className="grid md:grid-cols-2 gap-5 mb-14">
        <div className="bg-card border border-border rounded-2xl p-6 md:p-7">
          <h3 className="text-sm font-bold tracking-wider uppercase text-muted-foreground mb-4">
            A Realidade
          </h3>
          <p className="text-muted-foreground leading-relaxed text-sm md:text-base">
            {profile.realityCard}
          </p>
        </div>

        <div className="bg-gradient-to-br from-primary/10 via-card to-card border border-primary/40 rounded-2xl p-6 md:p-7 relative overflow-hidden">
          <Sparkles className="absolute top-4 right-4 w-5 h-5 text-primary/60" />
          <h3 className="text-sm font-bold tracking-wider uppercase text-primary mb-4">
            A Grande Oportunidade — O Oceano Azul
          </h3>
          <p className="text-muted-foreground leading-relaxed text-sm md:text-base">
            {profile.opportunityCard}
          </p>
        </div>
      </div>

      {/* Gauge */}
      <div className="bg-card border border-border rounded-2xl p-8 md:p-10 mb-14 text-center">
        <h3 className="text-xl md:text-2xl font-bold mb-6">Seu Potencial de Sucesso</h3>
        <SuccessGauge percent={profile.successPercent} />
        <p className="text-muted-foreground mt-4 max-w-xl mx-auto leading-relaxed">
          {renderBoldMarkdown(profile.successDescription)}
        </p>
      </div>

      {/* Story Bridge — Halbert: ponte emocional entre diagnóstico e oferta */}
      <div className="mb-12 max-w-3xl mx-auto">
        <p className="text-primary font-medium mb-4 inline-flex items-center gap-2">
          <Target className="w-4 h-4" /> Antes de eu te oferecer qualquer coisa, leia isso.
        </p>
        <div className="space-y-4 text-base md:text-lg leading-relaxed text-foreground/90">
          <p>{firstName}, eu sei o que tá passando na sua cabeça agora.</p>
          <p>
            Você terminou esse quiz e ouviu uma promessa que parece grande demais.{" "}
            <strong>"R$3K-15K/mês vendendo sites com IA?"</strong> Pareceria papo de guru se eu não tivesse vivido o oposto disso.
          </p>
          <p>
            Em 2018, eu trabalhava 100 km de casa, mal via meus filhos. Tentei afiliado, dropshipping, lançamento — e tudo que vinha era complexidade, dependência de algoritmo e venda que travava todo mês.
          </p>
          <p>
            O que mudou foi descobrir que <strong>existe um tipo de negócio digital que não depende de algoritmo, não depende de produto chinês, não depende de webinar de 3 horas vendendo curso de R$2.997.</strong>
          </p>
          <p>
            É um serviço que <strong>toda empresa do Brasil precisa AGORA</strong> — e que com IA você entrega em horas, não em semanas.
          </p>
        </div>
      </div>

      {/* A Revelação — o mecanismo + janela */}
      <div className="mb-12 bg-gradient-to-br from-orange-950/40 via-card to-card border border-orange-500/30 rounded-2xl p-6 md:p-8 max-w-3xl mx-auto">
        <p className="text-sm font-bold tracking-wider uppercase text-orange-400 mb-3 flex items-center gap-2">
          <Flame className="w-4 h-4" /> A parte que ninguém tá te contando
        </p>
        <p className="text-base md:text-lg leading-relaxed">
          99% dos sites brasileiros vão sumir do <strong>ChatGPT, Perplexity e Google AI Overviews</strong> nos próximos 18 meses. Já está acontecendo agora.
        </p>
        <p className="text-base md:text-lg leading-relaxed mt-3">
          As empresas que descobrirem isso primeiro vão pagar <strong>R$1.000 a R$5.000 por site</strong> pra alguém que entenda o jogo. <em>3 a 5 sites no mês = R$3K a R$15K na sua conta.</em> Sem dependência. Sem algoritmo. Sem dropshipping.
        </p>
        <p className="text-base md:text-lg leading-relaxed mt-3">
          O que eu te ofereço agora é o atalho — pra você não levar 8 anos descobrindo isso sozinho como eu levei.
        </p>
      </div>

      {/* Transição pra oferta */}
      <div className="text-center mb-8">
        <p className="text-primary font-medium mb-3 inline-flex items-center gap-2">
          <Target className="w-4 h-4" />
          Aqui está o atalho que eu queria ter tido em 2018
        </p>
        <h2 className="text-3xl md:text-5xl font-extrabold tracking-tight max-w-3xl mx-auto leading-tight">
          O Mini-Curso{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
            Negócio.IA
          </span>
        </h2>
        <p className="text-muted-foreground mt-4 max-w-2xl mx-auto text-base md:text-lg">
          O método cronometrado pra você sair do zero e fechar o primeiro PIX de{" "}
          <strong className="text-foreground">R$1.000 em 7 dias</strong> — vendendo sites que o Claude Code cria em 10 minutos pra empresas que precisam aparecer no AI Search.
        </p>
      </div>

      {/* Card de oferta — bullets com bold markdown + framing renovado */}
      <div className="bg-card border border-border rounded-2xl p-6 md:p-8 mb-8">
        <h3 className="text-lg md:text-xl font-bold mb-2 text-center">
          7 módulos cronometrados — você dá play hoje, fecha cliente essa semana
        </h3>
        <p className="text-sm text-muted-foreground text-center mb-6">
          Cada módulo termina com o próximo passo. Sem teoria solta. Sem encheção.
        </p>
        <ul className="space-y-3 mb-6">
          {offerContent.modules.map((mod) => (
            <li key={mod} className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
              <span className="text-sm md:text-base leading-relaxed">{renderBoldMarkdown(mod)}</span>
            </li>
          ))}
        </ul>

        <div className="bg-gradient-to-br from-primary/10 to-[#3a1d12]/10 border border-primary/30 rounded-xl p-5 mb-6">
          <p className="text-sm font-bold text-primary mb-3 flex items-center gap-2">
            <Zap className="w-4 h-4" /> + 2 Bônus Exclusivos (libera no checkout)
          </p>
          <ul className="space-y-3">
            {offerContent.bonuses.map((bonus) => (
              <li key={bonus.name} className="text-sm flex items-start gap-2">
                <Flame className="w-4 h-4 text-orange-500 flex-shrink-0 mt-0.5" />
                <span className="leading-relaxed">
                  <span className="font-bold">{bonus.name}</span>
                  {" — "}
                  {bonus.detail}{" "}
                  <span className="text-muted-foreground ml-1 inline-block mt-1">
                    (valor real:{" "}
                    <span className="line-through">{bonus.oldPrice}</span>{" "}
                    — sai de graça hoje)
                  </span>
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="text-center mb-6">
          <p className="text-sm text-muted-foreground line-through mb-1">
            Valor real do conteúdo: {offerContent.totalValue}
          </p>
          <p className="text-base text-foreground mb-2">Hoje você leva tudo por</p>
          <p className="text-xs text-muted-foreground tracking-wider uppercase mb-1">
            Em até
          </p>
          <p className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39] leading-none">
            {offerContent.installments}
          </p>
          <p className="text-base md:text-lg text-foreground mt-3">
            ou <strong className="text-foreground">{offerContent.fullPrice}</strong> à vista
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            {offerContent.priceSuffix}
          </p>
          <p className="text-xs text-primary mt-3 font-medium">
            Menos que um almoço de domingo. Pra um método que pode te tirar da CLT em 90 dias.
          </p>
        </div>

        <Button
          size="lg"
          asChild
          className="w-full h-16 text-base md:text-lg font-bold bg-gradient-to-r from-primary to-[#D97757] hover:from-primary hover:to-[#FF5C39] shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.5)] hover:scale-[1.02] transition-transform"
        >
          <a href={checkoutUrl} target="_blank" rel="noopener noreferrer">
            → Quero o método completo por {offerContent.fullPrice}
          </a>
        </Button>

        <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 mt-5 text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1.5">
            <CreditCard className="w-3 h-3" /> Cartão ou PIX
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Lock className="w-3 h-3" /> Pagamento 100% seguro
          </span>
          <span className="inline-flex items-center gap-1.5">
            <CheckCircle2 className="w-3 h-3" /> Acesso imediato
          </span>
        </div>
      </div>

      {/* Inversão de risco — Halbert/Brunson: o risco é meu, não seu */}
      <div className="bg-gradient-to-br from-[#1f0f09]/30 via-card to-card border-2 border-primary/40 rounded-2xl p-6 md:p-8 mb-8 max-w-3xl mx-auto">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-14 h-14 rounded-full bg-primary/20 border-2 border-primary/40 flex items-center justify-center">
            <CheckCircle2 className="w-7 h-7 text-primary" />
          </div>
          <div>
            <h3 className="text-lg md:text-xl font-bold mb-2">Garantia incondicional de 7 dias</h3>
            <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
              Você compra agora, abre os módulos e tem <strong className="text-foreground">7 dias inteiros pra dar uma volta no método</strong>. Se em qualquer momento você sentir que isso aqui <em>não é</em> o atalho que prometi — manda um email e eu devolvo seus R$37. Sem perguntas. Sem burocracia. Sem precisar provar nada.
            </p>
            <p className="text-sm md:text-base text-foreground mt-3 font-medium">
              O risco é meu. Você só topa o método se concordar que ele faz sentido pra você.
            </p>
          </div>
        </div>
      </div>

      {/* FAQ — 3 objeções rápidas (Stefan Georgi: pre-empt) */}
      <div className="mb-10 max-w-3xl mx-auto">
        <p className="text-sm font-bold tracking-wider uppercase text-primary mb-4 text-center">
          "Mas Alex, e se..."
        </p>
        <div className="space-y-3">
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="font-bold mb-1 text-sm md:text-base">"Eu não sei programar."</p>
            <p className="text-sm text-muted-foreground leading-relaxed">
              O Claude Code programa pra você. Você só dá os comandos certos — e eles estão prontos no Módulo 2. <strong className="text-foreground">Em 10 minutos sai um site profissional sem você escrever uma linha de código.</strong>
            </p>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="font-bold mb-1 text-sm md:text-base">"Eu não tenho tempo. Trabalho o dia todo."</p>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Aulas curtas, scripts copy-paste, lista de empresas pronta no Bônus 1. <strong className="text-foreground">2 horas no fim de semana já são suficientes pra mandar a primeira prospecção e começar a fila de clientes.</strong>
            </p>
          </div>
          <div className="bg-card border border-border rounded-xl p-5">
            <p className="font-bold mb-1 text-sm md:text-base">"E se eu não conseguir fechar nenhum cliente?"</p>
            <p className="text-sm text-muted-foreground leading-relaxed">
              7 dias de garantia incondicional. Se você seguir o método e não fechar, devolvo R$37. <strong className="text-foreground">O Bônus 1 entrega lista pronta + script. É copia-cola.</strong>
            </p>
          </div>
        </div>
      </div>

      {/* Recap final + CTA secundário (fechamento Schwartz) */}
      <div className="text-center mb-12 max-w-3xl mx-auto">
        <p className="text-base md:text-lg text-muted-foreground mb-4 leading-relaxed">
          {firstName}, voltando pro seu diagnóstico: você tem{" "}
          <strong className="text-primary text-xl">{profile.successPercent}% de chance</strong> de chegar a R$3K-15K/mês.
        </p>
        <p className="text-base md:text-lg text-muted-foreground mb-6 leading-relaxed">
          A janela do AI Search é <strong className="text-foreground">agora</strong>. Em 18 meses ela fecha. Você pode investir <strong className="text-foreground">R$37 hoje</strong> e ter o método completo — ou continuar onde tá, esperando a próxima oportunidade aparecer.
        </p>
        <Button
          size="lg"
          asChild
          className="w-full md:w-auto px-8 h-14 text-base md:text-lg font-bold bg-gradient-to-r from-primary to-[#D97757] hover:from-primary hover:to-[#FF5C39] shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.5)] hover:scale-[1.02] transition-transform"
        >
          <a href={checkoutUrl} target="_blank" rel="noopener noreferrer">
            → Sim, quero o método por {offerContent.fullPrice}
          </a>
        </Button>
        <p className="text-xs text-muted-foreground mt-4">
          Acesso imediato · 7 dias de garantia incondicional · Pagamento único
        </p>
      </div>
    </div>
  );
};
