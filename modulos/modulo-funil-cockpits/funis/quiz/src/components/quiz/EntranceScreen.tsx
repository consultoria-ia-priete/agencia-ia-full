import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2 } from "lucide-react";

interface EntranceScreenProps {
  onStart: () => void;
}

export const EntranceScreen = ({ onStart }: EntranceScreenProps) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] py-6 text-center px-4 animate-in fade-in slide-in-from-bottom-4 duration-700 max-w-5xl mx-auto">
      {/* Eyebrow — Brunson: mecanismo nomeado + curiosidade */}
      <div className="inline-flex flex-wrap items-center justify-center px-3 py-1.5 mb-4 md:mb-5 text-[10px] md:text-xs font-semibold tracking-wider text-primary uppercase border rounded-full border-primary/30 bg-primary/10 max-w-full">
        <span className="flex w-2 h-2 mr-2 rounded-full bg-primary animate-pulse flex-shrink-0"></span>
        <span className="break-words">QUIZ AI SEARCH ERA · DESCUBRA QUAL DOS 4 PERFIS É O SEU · 2 MIN</span>
      </div>

      {/* H1 — Halbert+Hormozi: storytelling visceral + specificity */}
      <h1 className="w-full max-w-4xl mb-3 md:mb-4 text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold md:tracking-tight text-foreground leading-tight break-words [overflow-wrap:anywhere]">
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
          R$3K a R$15K por mês
        </span>{" "}
        vendendo sites que o Claude Code cria em 30 minutos
        <span className="block mt-2 text-lg sm:text-xl md:text-2xl lg:text-3xl text-foreground/90 font-bold">
          — pra empresas que precisam aparecer no ChatGPT antes de sumir do mapa
        </span>
      </h1>

      {/* Subheadline — Halbert+Hormozi: matemática clara da promessa */}
      <p className="w-full max-w-3xl mb-5 md:mb-6 text-base md:text-lg text-muted-foreground leading-relaxed break-words">
        99% dos sites brasileiros vão sumir do AI Search nos próximos{" "}
        <strong className="text-foreground">18 meses</strong>. As empresas que descobrirem isso vão pagar{" "}
        <strong className="text-foreground">R$1.000 a R$5.000 por site</strong>.
        <span className="block mt-1 text-foreground font-semibold">
          3 a 5 sites no mês = R$3K a R$15K na sua conta.
        </span>
      </p>

      {/* Bullets — Schwartz: "sem X" (quebra os 3 modelos que decepcionaram) */}
      <ul className="max-w-2xl mb-5 md:mb-6 space-y-2 md:space-y-2.5 text-left">
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

      {/* Qualifier — Schwartz: identification + caminho mais curto (compactado) */}
      <div className="max-w-3xl mb-5 md:mb-6 px-5 py-3 md:py-4 bg-card/60 border border-border rounded-xl text-left">
        <p className="text-sm md:text-base text-muted-foreground leading-relaxed">
          Esse diagnóstico é pra quem quer um negócio digital{" "}
          <strong className="text-foreground">de verdade</strong> — receita real, cliente real, entrega real. Sem promessa de fácil. Sem dependência de algoritmo.{" "}
          <span className="text-foreground">Em 2 minutos eu te mostro se você tem o perfil — e qual o caminho mais curto pro seu primeiro cliente.</span>
        </p>
      </div>

      {/* CTA — Brunson: mecanismo direto + "Grátis" (Russell Brunson testou: converte +) */}
      <Button
        size="lg"
        onClick={onStart}
        className="w-full sm:w-auto h-auto min-h-14 md:min-h-16 py-3 md:py-4 px-6 sm:px-10 text-base sm:text-lg md:text-xl font-bold transition-all hover:scale-105 shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.5)] bg-gradient-to-r from-primary to-[#D97757] hover:from-primary hover:to-[#FF5C39] border-none whitespace-normal text-center leading-tight"
      >
        <span className="break-words">→ Quero meu diagnóstico Grátis agora</span>
        <ArrowRight className="w-5 h-5 ml-2 flex-shrink-0" />
      </Button>

      {/* Badges */}
      <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 mt-5 md:mt-6 text-xs md:text-sm text-muted-foreground">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-primary" />
          <span>Leva 2 minutos</span>
        </div>
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-primary" />
          <span>100% Grátis</span>
        </div>
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-primary" />
          <span>Resultado personalizado</span>
        </div>
      </div>
    </div>
  );
};
