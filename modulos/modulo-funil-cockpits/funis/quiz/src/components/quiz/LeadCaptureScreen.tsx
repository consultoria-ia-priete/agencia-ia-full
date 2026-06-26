import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Lock, ArrowRight, CheckCircle2, Mail } from "lucide-react";
import { toast } from "sonner";
import { profileDescriptions, type ProfileType } from "@/data/quizData";

interface LeadCaptureScreenProps {
  onSubmit: (data: { name: string; email: string; phone: string }) => void;
  profileType: ProfileType;
  answers: Record<number, string[]>;
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const formatPhone = (raw: string) => {
  const digits = raw.replace(/\D/g, "").slice(0, 11);
  if (digits.length <= 2) return `(${digits}`;
  if (digits.length <= 7) return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
  return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
};

const readUtmFromUrl = () => {
  if (typeof window === "undefined") return {};
  const sp = new URLSearchParams(window.location.search);
  return {
    utm_source: sp.get("utm_source") || "",
    utm_medium: sp.get("utm_medium") || "",
    utm_campaign: sp.get("utm_campaign") || "",
    utm_content: sp.get("utm_content") || "",
    utm_term: sp.get("utm_term") || "",
  };
};

export const LeadCaptureScreen = ({
  onSubmit,
  profileType,
  answers,
}: LeadCaptureScreenProps) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const digits = phone.replace(/\D/g, "");
    const emailTrim = email.trim().toLowerCase();

    if (name.trim().length < 2) {
      toast.error("Digite seu nome completo.");
      return;
    }
    if (!EMAIL_REGEX.test(emailTrim)) {
      toast.error("Digite um e-mail válido.");
      return;
    }
    if (digits.length < 10) {
      toast.error("Digite um WhatsApp válido com DDD.");
      return;
    }

    setSubmitting(true);

    try {
      const profile = profileDescriptions[profileType];
      // Single event_id used by both Pixel JS (client) and CAPI (server) so
      // Meta dedupes the two firings into one Lead event.
      const eventId = crypto.randomUUID();

      // Fire Meta Pixel client-side Lead with eventID for dedup
      if (typeof window !== "undefined" && (window as any).fbq) {
        (window as any).fbq(
          "track",
          "Lead",
          {
            content_name: "Quiz Negocio.IA",
            content_category: "quiz_funnel",
            value: 0,
            currency: "BRL",
          },
          { eventID: eventId }
        );
      }

      const res = await fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          name: name.trim(),
          email: emailTrim,
          phone: digits,
          profile_type: profileType,
          success_percent: profile.successPercent,
          answers,
          event_id: eventId,
          utm: readUtmFromUrl(),
        }),
      });

      if (!res.ok) {
        const text = await res.text().catch(() => "");
        console.error("Lead submit failed:", res.status, text);
        toast.error("Não conseguimos enviar seus dados. Tente novamente.");
        setSubmitting(false);
        return;
      }

      // Cross-domain identity cookie + localStorage para o /obrigado correlacionar
      // a compra com este lead. Match keys: email + phone.
      const identityPayload = JSON.stringify({
        email: emailTrim,
        phone: digits,
        event_id: eventId,
        funnel_source: "quiz-negocio-ia",
      });
      try {
        document.cookie = `krob_lead_identity=${encodeURIComponent(identityPayload)}; domain=.SEU-DOMINIO.com; path=/; max-age=3600; SameSite=None; Secure`;
      } catch {
        // ignora
      }
      try {
        localStorage.setItem("krob_lead_identity", identityPayload);
      } catch {
        // localStorage indisponível — cookie cross-domain é o caminho principal
      }

      onSubmit({ name: name.trim(), email: emailTrim, phone: digits });
    } catch (err) {
      console.error("Lead submit error:", err);
      toast.error("Erro de conexão. Verifique sua internet e tente novamente.");
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-6">
          <div className="w-20 h-20 rounded-full bg-primary/10 border-2 border-primary/40 flex items-center justify-center shadow-[0_0_30px_-5px_hsl(var(--primary)_/_0.4)]">
            <CheckCircle2 className="w-12 h-12 text-primary" />
          </div>
        </div>

        <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-4">
          Diagnóstico concluído.
        </h2>

        <p className="text-muted-foreground text-base md:text-lg mb-3">
          Com base nas suas respostas, <span className="text-foreground font-medium">Alex Priete</span> identificou o caminho mais seguro para o seu perfil chegar a R$3K/mês vendendo sites com IA.
        </p>
        <p className="text-muted-foreground text-sm">
          Tem algo específico sobre o seu caso que vai mudar a forma como você vê o digital.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="bg-card border border-border rounded-2xl p-6 md:p-8 space-y-5"
      >
        <p className="text-sm text-foreground text-center mb-2">
          Coloque seus dados abaixo para receber seu resultado personalizado agora.
          <br />
          <span className="text-muted-foreground">
            Também vou te enviar o acesso ao diagnóstico completo direto no WhatsApp.
          </span>
        </p>

        <div className="space-y-2">
          <Label htmlFor="name" className="text-sm font-medium flex items-center gap-2">
            <span>👤</span> Seu nome
          </Label>
          <Input
            id="name"
            type="text"
            placeholder="Como podemos te chamar?"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={submitting}
            autoComplete="name"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="email" className="text-sm font-medium flex items-center gap-2">
            <span>📧</span> Seu melhor e-mail
          </Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
            <Input
              id="email"
              type="email"
              inputMode="email"
              autoCapitalize="none"
              spellCheck={false}
              placeholder="seu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={submitting}
              autoComplete="email"
              className="pl-10"
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="phone" className="text-sm font-medium flex items-center gap-2">
            <span>📱</span> WhatsApp (com DDD)
          </Label>
          <Input
            id="phone"
            type="tel"
            inputMode="numeric"
            placeholder="(11) 90000-0000"
            value={phone}
            onChange={(e) => setPhone(formatPhone(e.target.value))}
            disabled={submitting}
            autoComplete="tel"
          />
        </div>

        <Button
          type="submit"
          size="lg"
          disabled={submitting}
          className="w-full h-14 text-base font-semibold bg-gradient-to-r from-primary to-[#3a1d12] hover:from-primary hover:to-[#5c2f1f] shadow-[0_0_30px_-5px_hsl(var(--primary)_/_0.4)]"
        >
          {submitting ? "Enviando..." : "Ver meu diagnóstico agora"}
          {!submitting && <ArrowRight className="w-5 h-5 ml-2" />}
        </Button>

        <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground pt-2">
          <Lock className="w-3 h-3" />
          <span>Seus dados estão protegidos. Sem spam. Pode cancelar quando quiser.</span>
        </div>
      </form>
    </div>
  );
};
