import { useState } from "react";
import { Button } from "@/components/ui/button";
import { CheckCircle2, ChevronDown, Gift, AlertTriangle, ArrowRight, Loader2 } from "lucide-react";
import { toast } from "sonner";

const WHATSAPP_GROUP_URL = "https://SEU-DOMINIO.com/grupos";
const FUNNEL_SOURCE = "funil-consultor-ia";
const PRODUCT_LABEL = "ConsultorIA";

const readCookie = (key: string): string => {
  if (typeof document === "undefined") return "";
  const m = document.cookie.match(new RegExp("(?:^|; )" + key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "=([^;]*)"));
  return m ? decodeURIComponent(m[1]) : "";
};

const parseIdentity = (raw: string) => {
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    return {
      email: parsed.email || "",
      event_id: parsed.event_id || "",
      funnel_source: parsed.funnel_source || FUNNEL_SOURCE,
    };
  } catch {
    return null;
  }
};

const readLeadIdentity = () => {
  if (typeof window === "undefined") return { email: "", event_id: "", funnel_source: FUNNEL_SOURCE };
  // Cookie cross-domain (.SEU-DOMINIO.com) é o caminho principal — funciona quando o lead
  // veio de outro subdomínio (LP NegocioIA → /obrigado em quiznegocioia, etc).
  const fromCookie = parseIdentity(readCookie("krob_lead_identity"));
  if (fromCookie) return fromCookie;
  // Fallback: localStorage (mesmo subdomínio)
  try {
    const fromLs = parseIdentity(localStorage.getItem("krob_lead_identity") || "");
    if (fromLs) return fromLs;
  } catch {
    // ignora
  }
  return { email: "", event_id: "", funnel_source: FUNNEL_SOURCE };
};

const Obrigado = () => {
  const [submitting, setSubmitting] = useState(false);

  const handleGroupClick = async (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    if (submitting) return;
    setSubmitting(true);

    const identity = readLeadIdentity();

    try {
      // Pixel custom event (intent forte de engajamento pós-compra)
      if (typeof window !== "undefined" && (window as any).fbq) {
        (window as any).fbq("trackCustom", "JoinGroup", {
          content_name: PRODUCT_LABEL,
          source: identity.funnel_source,
        });
      }

      // Server-side: dispara webhook GHL pra mover stage do opportunity pra "Entrou no Grupo do Webinar"
      await fetch("/api/group-click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          email: identity.email,
          event_id: identity.event_id,
          funnel_source: identity.funnel_source,
        }),
      }).catch(() => {
        // Falha silenciosa — não bloqueia redirect (lead vai pro grupo mesmo assim)
      });
    } catch {
      // ignora
    }

    // Pequeno atraso pra eventos saírem antes do redirect
    setTimeout(() => {
      window.location.href = WHATSAPP_GROUP_URL;
    }, 200);
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none hidden md:block">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]" />
      </div>

      <main className="relative z-10 container mx-auto px-4 py-10 md:py-16 min-h-screen flex flex-col items-center justify-center">
        <div className="w-full max-w-2xl mx-auto text-center animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div className="inline-flex items-center justify-center w-20 h-20 mb-8 rounded-full bg-primary/10 border border-primary/30">
            <CheckCircle2 className="w-12 h-12 text-primary" strokeWidth={2} />
          </div>

          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight mb-4">
            Parabéns! Sua compra foi confirmada.
          </h1>

          <p className="text-lg text-muted-foreground mb-12">
            O acesso ao{" "}
            <span className="font-mono text-primary bg-primary/10 px-2 py-0.5 rounded">
              ConsultorIA
            </span>{" "}
            já foi enviado para seu e-mail.
          </p>

          <p className="text-2xl md:text-3xl font-extrabold tracking-wider text-primary mb-2">
            ATENÇÃO!
          </p>
          <div className="flex justify-center gap-3 mb-10">
            <ChevronDown className="w-7 h-7 text-primary animate-arrow-bounce" style={{ animationDelay: "0ms" }} strokeWidth={3} />
            <ChevronDown className="w-7 h-7 text-primary animate-arrow-bounce" style={{ animationDelay: "180ms" }} strokeWidth={3} />
            <ChevronDown className="w-7 h-7 text-primary animate-arrow-bounce" style={{ animationDelay: "360ms" }} strokeWidth={3} />
          </div>

          <div className="bg-card border-2 border-primary/50 rounded-2xl p-6 md:p-8 text-left animate-card-glow">
            <div className="inline-flex items-center gap-2 px-3 py-1 mb-5 text-xs font-bold tracking-wider text-primary uppercase border rounded-full border-primary/40 bg-primary/10">
              <Gift className="w-3.5 h-3.5" />
              Próximo Passo Desbloqueado
            </div>

            <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-4 leading-snug">
              Entre agora na{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#FF5C39]">
                Sociedade Secreta dos Consultores de IA
              </span>
            </h2>

            <p className="text-muted-foreground mb-6 leading-relaxed">
              Comunidade fechada de Consultores de IA aplicando o método em campo.{" "}
              <span className="text-foreground font-bold">
                Cases reais, scripts validados e o link da aula ao vivo exclusiva
              </span>{" "}
              são enviados dentro do grupo.
            </p>

            <div className="flex items-start gap-3 p-4 mb-6 rounded-lg border border-red-500/30 bg-red-950/30">
              <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm md:text-base text-red-200">
                A <span className="font-bold underline decoration-red-400">aula ao vivo</span> e os bônus extras só são compartilhados dentro do grupo. Entra agora pra não perder.
              </p>
            </div>

            <Button
              size="lg"
              asChild
              disabled={submitting}
              className="w-full h-16 text-base md:text-lg font-bold tracking-wider uppercase bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_40px_-5px_hsl(var(--primary)_/_0.6)] hover:scale-[1.02] transition-transform"
            >
              <a href={WHATSAPP_GROUP_URL} onClick={handleGroupClick} target="_blank" rel="noopener noreferrer">
                {submitting ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" /> Redirecionando...
                  </>
                ) : (
                  <>
                    Entrar no Grupo do WhatsApp
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </>
                )}
              </a>
            </Button>

            <p className="text-xs text-center text-muted-foreground mt-4">
              O link da aula será enviado exclusivamente no grupo.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Obrigado;
