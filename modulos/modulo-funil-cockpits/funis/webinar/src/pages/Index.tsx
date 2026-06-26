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
  Zap,
  Clock,
  CalendarClock,
  Target,
  TrendingUp,
  ShieldCheck,
  Users,
  CheckCircle2,
  ChevronDown,
  ArrowRight,
  Sparkles,
  Brain,
  Building2,
  Quote,
  Ban,
} from "lucide-react";

/* ------------------------------------------------------------------ */
/* Countdown — aponta sempre para o próximo 14:30 BRT (17:30 UTC).     */
/* Brasil é UTC-3 fixo (sem horário de verão desde 2019).              */
/* ------------------------------------------------------------------ */
function nextWebinarMs(): number {
  const now = new Date();
  // 14:30 BRT == 17:30 UTC
  const target = new Date(now);
  target.setUTCHours(17, 30, 0, 0);
  if (target.getTime() <= now.getTime()) {
    target.setUTCDate(target.getUTCDate() + 1);
  }
  return target.getTime();
}

function pad(n: number) {
  return String(n).padStart(2, "0");
}

const Countdown = () => {
  const [target, setTarget] = useState<number>(nextWebinarMs());
  const [remaining, setRemaining] = useState<number>(target - Date.now());

  useEffect(() => {
    const id = setInterval(() => {
      let diff = target - Date.now();
      if (diff <= 0) {
        const next = nextWebinarMs();
        setTarget(next);
        diff = next - Date.now();
      }
      setRemaining(diff);
    }, 1000);
    return () => clearInterval(id);
  }, [target]);

  const totalSec = Math.max(0, Math.floor(remaining / 1000));
  const h = Math.floor(totalSec / 3600);
  const m = Math.floor((totalSec % 3600) / 60);
  const s = totalSec % 60;

  const Box = ({ value, label }: { value: string; label: string }) => (
    <div className="flex flex-col items-center">
      <div className="w-16 h-16 md:w-20 md:h-20 flex items-center justify-center rounded-xl bg-card border border-primary/30 font-mono text-2xl md:text-4xl font-extrabold text-primary tabular-nums shadow-[0_0_24px_-8px_hsl(var(--primary)_/_0.5)]">
        {value}
      </div>
      <span className="mt-2 text-[10px] md:text-xs uppercase tracking-widest text-muted-foreground">
        {label}
      </span>
    </div>
  );

  return (
    <div className="flex items-center justify-center gap-3 md:gap-4">
      <Box value={pad(h)} label="Horas" />
      <span className="text-2xl md:text-4xl font-extrabold text-primary/50 -mt-5">:</span>
      <Box value={pad(m)} label="Min" />
      <span className="text-2xl md:text-4xl font-extrabold text-primary/50 -mt-5">:</span>
      <Box value={pad(s)} label="Seg" />
    </div>
  );
};

/* ------------------------------------------------------------------ */

const SECRETS = [
  {
    icon: Target,
    tag: "Segredo #1",
    title: "Posicionamento Certeiro B2B",
    body:
      "Por que vender IA pra “qualquer um” te deixa quebrado — e como mirar em empresas que já têm o dinheiro e a dor, prontas pra pagar de R$1K a R$3K por mês.",
  },
  {
    icon: Zap,
    tag: "Segredo #2",
    title: "O Funil do Consultor (Caixa Rápido)",
    body:
      "O caminho mais curto entre “não conheço ninguém” e o primeiro contrato fechado — sem precisar aparecer, sem audiência e sem gravar reels todo dia.",
  },
  {
    icon: TrendingUp,
    tag: "Segredo #3",
    title: "Serviço Recorrente Irresistível",
    body:
      "Como entregar IA como Serviço de um jeito que o cliente fica meses pagando porque resolve a vida dele — não porque assinou um contrato que prende.",
  },
];

const FOR_WHO = [
  "Você já fez curso, comprou ferramenta, testou prompt — e ainda não virou um negócio que paga as contas.",
  "Você sente que a IA é a sua chance, mas não sabe como transformar isso em contrato fechado com empresa de verdade.",
  "Você está cansado de guru vendendo sonho e quer um método que funcione com cliente real pagando todo mês.",
  "Você quer parar de depender de audiência, sorte ou “ficar famoso” pra finalmente faturar com o que aprendeu.",
];

const TESTIMONIALS = [
  {
    name: "Rafael M.",
    role: "Ex-afiliado · hoje Consultor de IA",
    quote:
      "Passei 2 anos comprando curso e não saía do lugar. Em 6 semanas fechei meu primeiro contrato de R$2K/mês. Hoje tenho 4.",
  },
  {
    name: "Juliana S.",
    role: "Saiu do CLT",
    quote:
      "Eu achava que precisava de audiência. Não precisava. Precisava de método e de uma empresa pra resolver. Mudou tudo.",
  },
  {
    name: "Diego A.",
    role: "Consultor de IA · interior de SP",
    quote:
      "O webinar abriu minha cabeça em 1 hora mais do que cursos inteiros. Saí com clareza do que fazer na segunda de manhã.",
  },
];

const FAQ = [
  {
    q: "Quanto custa para participar do webinar?",
    a: "Nada. A aula ao vivo é 100% gratuita. Você só precisa se inscrever para receber o link no WhatsApp e no e-mail.",
  },
  {
    q: "Que horas começa e quanto tempo dura?",
    a: "Todos os dias às 14:30 (horário de Brasília). A aula dura cerca de 1 hora, com tempo para tirar dúvidas ao vivo.",
  },
  {
    q: "Preciso já saber de IA ou programação?",
    a: "Não. O método ConsultorIA é sobre vender IA como Serviço para empresas — você vai entender o caminho mesmo começando do zero.",
  },
  {
    q: "É mais um curso de guru prometendo dinheiro fácil?",
    a: "O oposto. A proposta é fechar contratos B2B reais, recorrentes, com empresas que já têm dinheiro e dor. Sem palco, sem fórmula mágica.",
  },
  {
    q: "Vou receber o link de qual forma?",
    a: "Assim que você se inscrever, o link da sala é enviado no seu WhatsApp e e-mail, junto com um lembrete antes das 14:30.",
  },
];

const Index = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const open = () => setModalOpen(true);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30 overflow-x-hidden">
      {/* glow de fundo */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-15%] left-[-10%] w-[50%] h-[50%] bg-primary/15 rounded-full blur-[140px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[45%] h-[45%] bg-primary/10 rounded-full blur-[140px]" />
      </div>

      {/* barra de urgência fixa */}
      <div className="sticky top-0 z-40 w-full bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 py-2 flex items-center justify-center gap-2 text-xs md:text-sm font-bold text-center">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-foreground/60" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary-foreground" />
          </span>
          WEBINAR AO VIVO · TODO DIA ÀS 14:30 · VAGAS LIMITADAS
        </div>
      </div>

      <main className="relative z-10">
        {/* HERO */}
        <section className="container mx-auto px-4 pt-12 md:pt-20 pb-16 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-6 text-xs font-bold tracking-wider uppercase border rounded-full border-primary/40 bg-primary/10 text-primary">
            <Sparkles className="w-3.5 h-3.5" />
            Aula ao vivo e gratuita
          </div>

          <h1 className="max-w-4xl mx-auto text-3xl md:text-6xl font-extrabold tracking-tight leading-[1.1]">
            Descubra os{" "}
            <span className="text-primary">3 Segredos</span> para ter um negócio de
            IA como Serviço e{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF8A5C]">
              faturar acima de R$33K/mês em 90 dias
            </span>
          </h1>

          <p className="max-w-2xl mx-auto mt-6 text-lg md:text-xl text-muted-foreground leading-relaxed">
            Sem ser influencer, sem aparecer, sem vender curso. Só você, a IA e
            empresas reais pagando todo mês pelo que você entrega.
          </p>

          {/* countdown */}
          <div className="mt-10 mb-6">
            <p className="flex items-center justify-center gap-2 text-sm uppercase tracking-widest text-muted-foreground mb-4">
              <CalendarClock className="w-4 h-4 text-primary" />
              A próxima aula começa em
            </p>
            <Countdown />
          </div>

          <Button
            onClick={open}
            size="lg"
            className="h-16 px-10 text-base md:text-lg font-bold tracking-wider uppercase bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.6)] hover:scale-[1.02] transition-transform animate-pulse-glow"
          >
            <Clock className="w-5 h-5 mr-2" />
            Quero participar
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
          <p className="mt-4 text-xs text-muted-foreground font-mono">
            Inscrição gratuita · link enviado no seu WhatsApp e e-mail
          </p>

          <div className="flex justify-center mt-12">
            <ChevronDown className="w-7 h-7 text-primary/60 animate-arrow-bounce" strokeWidth={2.5} />
          </div>
        </section>

        {/* 3 SEGREDOS */}
        <section className="container mx-auto px-4 py-16">
          <h2 className="text-center text-2xl md:text-4xl font-extrabold tracking-tight mb-3">
            O que você vai destravar nessa aula
          </h2>
          <p className="text-center text-muted-foreground max-w-2xl mx-auto mb-12">
            Os 3 pilares da Tríade AIAAS — o mesmo caminho que tira o consultor do
            “testo prompt e não acontece nada” para contrato fechado.
          </p>
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {SECRETS.map(({ icon: Icon, tag, title, body }) => (
              <div
                key={tag}
                className="relative p-7 rounded-2xl bg-card border border-border hover:border-primary/40 transition-colors"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 mb-5 rounded-xl bg-primary/10 border border-primary/30">
                  <Icon className="w-6 h-6 text-primary" />
                </div>
                <span className="block text-xs font-bold uppercase tracking-widest text-primary mb-2">
                  {tag}
                </span>
                <h3 className="text-xl font-extrabold mb-3 leading-snug">{title}</h3>
                <p className="text-muted-foreground leading-relaxed text-sm">{body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* PARA QUEM É */}
        <section className="container mx-auto px-4 py-16">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-center text-2xl md:text-4xl font-extrabold tracking-tight mb-3">
              Essa aula é pra você se…
            </h2>
            <p className="text-center text-muted-foreground mb-10">
              Pensa comigo — se você se reconhece em alguma dessas, seu lugar é lá dentro.
            </p>
            <div className="space-y-3">
              {FOR_WHO.map((item, i) => (
                <div
                  key={i}
                  className="flex items-start gap-4 p-5 rounded-xl bg-card border border-border"
                >
                  <CheckCircle2 className="w-6 h-6 text-primary flex-shrink-0 mt-0.5" />
                  <p className="text-foreground/90 leading-relaxed">{item}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ANTI-GURU */}
        <section className="container mx-auto px-4 py-16">
          <div className="max-w-3xl mx-auto p-8 md:p-10 rounded-2xl bg-card border border-primary/30 text-center">
            <div className="inline-flex items-center justify-center w-14 h-14 mb-5 rounded-full bg-primary/10 border border-primary/30">
              <Ban className="w-7 h-7 text-primary" />
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-4">
              Diga não aos gurus do digital
            </h2>
            <p className="text-muted-foreground leading-relaxed text-lg">
              Isso não é mais um curso prometendo R$10K na primeira semana vendendo
              pra ninguém. É outra coisa, totalmente. É IA como Serviço para empresas
              reais, com contrato recorrente, do jeito que dá pra fazer começando hoje
              — mesmo que a sua família já tenha desistido de te ouvir falar disso.
            </p>
          </div>
        </section>

        {/* MENTOR */}
        <section className="container mx-auto px-4 py-16">
          <div className="max-w-4xl mx-auto grid md:grid-cols-[280px_1fr] gap-8 md:gap-12 items-center">
            <div className="relative mx-auto md:mx-0">
              <div className="absolute -inset-3 rounded-2xl bg-primary/20 blur-2xl" />
              <img
                src="/images/alex.jpg"
                alt="Alex Priete"
                className="relative w-56 h-56 md:w-full md:h-auto object-cover rounded-2xl border border-primary/30"
                loading="lazy"
              />
            </div>
            <div>
              <span className="block text-xs font-bold uppercase tracking-widest text-primary mb-2">
                Quem conduz a aula
              </span>
              <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-4">
                Alex Priete
              </h2>
              <p className="text-muted-foreground leading-relaxed mb-4">
                Criador do método ConsultorIA e fundador da SSCIA — a Sociedade
                Secreta dos Consultores de IA. Ajuda pessoas comuns a transformarem
                IA e automação em contratos B2B recorrentes, sem precisar de
                audiência, palco ou nome conhecido.
              </p>
              <div className="flex flex-wrap gap-3">
                <span className="inline-flex items-center gap-2 px-3 py-1.5 text-sm rounded-full bg-secondary border border-border">
                  <Building2 className="w-4 h-4 text-primary" /> Foco em empresas reais
                </span>
                <span className="inline-flex items-center gap-2 px-3 py-1.5 text-sm rounded-full bg-secondary border border-border">
                  <Brain className="w-4 h-4 text-primary" /> IA aplicada como serviço
                </span>
                <span className="inline-flex items-center gap-2 px-3 py-1.5 text-sm rounded-full bg-secondary border border-border">
                  <Users className="w-4 h-4 text-primary" /> Comunidade SSCIA
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* DEPOIMENTOS */}
        <section className="container mx-auto px-4 py-16">
          <h2 className="text-center text-2xl md:text-4xl font-extrabold tracking-tight mb-12">
            Quem entrou já está fazendo acontecer
          </h2>
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {TESTIMONIALS.map(({ name, role, quote }) => (
              <div key={name} className="p-7 rounded-2xl bg-card border border-border">
                <Quote className="w-8 h-8 text-primary/40 mb-4" />
                <p className="text-foreground/90 leading-relaxed mb-6">“{quote}”</p>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/15 border border-primary/30 flex items-center justify-center font-bold text-primary">
                    {name.charAt(0)}
                  </div>
                  <div>
                    <p className="font-bold text-sm">{name}</p>
                    <p className="text-xs text-muted-foreground">{role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* FAQ */}
        <section className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto">
            <h2 className="text-center text-2xl md:text-4xl font-extrabold tracking-tight mb-10">
              Perguntas frequentes
            </h2>
            <Accordion type="single" collapsible className="space-y-3">
              {FAQ.map(({ q, a }, i) => (
                <AccordionItem
                  key={i}
                  value={`item-${i}`}
                  className="bg-card border border-border rounded-xl px-5"
                >
                  <AccordionTrigger className="text-left font-bold hover:no-underline">
                    {q}
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground leading-relaxed">
                    {a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </section>

        {/* CTA FINAL */}
        <section className="container mx-auto px-4 py-20 text-center">
          <div className="max-w-3xl mx-auto p-10 md:p-14 rounded-3xl bg-gradient-to-b from-primary/10 to-transparent border border-primary/30">
            <ShieldCheck className="w-12 h-12 text-primary mx-auto mb-6" />
            <h2 className="text-3xl md:text-5xl font-extrabold tracking-tight mb-5 leading-tight">
              A próxima aula é hoje às 14:30
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-xl mx-auto">
              Garanta sua vaga agora. É gratuito, é ao vivo, e pode ser o dia em que
              tudo finalmente começa a fazer sentido pra você.
            </p>
            <div className="mb-8">
              <Countdown />
            </div>
            <Button
              onClick={open}
              size="lg"
              className="h-16 px-10 text-base md:text-lg font-bold tracking-wider uppercase bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.6)] hover:scale-[1.02] transition-transform"
            >
              <Clock className="w-5 h-5 mr-2" />
              Quero garantir minha vaga
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <p className="mt-4 text-xs text-muted-foreground font-mono">
              Vaga 100% gratuita · link no WhatsApp e e-mail
            </p>
          </div>
        </section>

        <footer className="container mx-auto px-4 py-10 text-center border-t border-border">
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} Alex Priete · ConsultorIA. Todos os direitos reservados.
          </p>
          <p className="mt-2 text-xs text-muted-foreground/60 max-w-2xl mx-auto">
            Este site não é afiliado ao Facebook ou a qualquer entidade do Facebook.
            Os resultados citados são individuais e não representam promessa de ganho.
          </p>
        </footer>
      </main>

      <CaptureModal open={modalOpen} onOpenChange={setModalOpen} />
    </div>
  );
};

export default Index;
