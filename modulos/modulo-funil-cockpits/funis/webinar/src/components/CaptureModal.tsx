import { useState } from "react";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { CalendarClock, Clock, Loader2 } from "lucide-react";
import { toast } from "sonner";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const SOURCE = "webinar-ao-vivo";
const WEBINAR_LABEL = "Webinar ConsultorIA";

const formatPhone = (raw: string) => {
  const digits = raw.replace(/\D/g, "").slice(0, 11);
  if (digits.length <= 2) return `(${digits}`;
  if (digits.length <= 7) return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
  return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
};

interface CaptureModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const CaptureModal = ({ open, onOpenChange }: CaptureModalProps) => {
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
      const eventId = crypto.randomUUID();

      // 1. Pixel JS Lead com mesmo eventID — Meta dedupa com CAPI server-side
      if (typeof window !== "undefined" && (window as any).fbq) {
        (window as any).fbq(
          "track",
          "Lead",
          {
            content_name: WEBINAR_LABEL,
            content_category: "webinar_registration",
          },
          { eventID: eventId }
        );
      }

      // 2. Server-side: D1 + Meta CAPI + GHL (workflow envia link + lembrete do webinar)
      const sp = typeof window !== "undefined" ? new URLSearchParams(window.location.search) : new URLSearchParams();
      const res = await fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          name: name.trim(),
          email: emailTrim,
          phone: digits,
          event_id: eventId,
          source: SOURCE,
          utm: {
            utm_source: sp.get("utm_source") || "",
            utm_medium: sp.get("utm_medium") || "",
            utm_campaign: sp.get("utm_campaign") || "",
            utm_content: sp.get("utm_content") || "",
            utm_term: sp.get("utm_term") || "",
          },
        }),
      });

      if (!res.ok) {
        const text = await res.text().catch(() => "");
        console.error("Lead submit failed:", res.status, text);
        toast.error("Não conseguimos registrar sua inscrição. Tente novamente.");
        setSubmitting(false);
        return;
      }

      // 3. Pixel CompleteRegistration (inscrição confirmada no webinar)
      if (typeof window !== "undefined" && (window as any).fbq) {
        (window as any).fbq("track", "CompleteRegistration", {
          content_name: WEBINAR_LABEL,
          status: "registered",
        });
      }

      // 4. Salva identidade do lead em cookie cross-domain (.SEU-DOMINIO.com) + localStorage
      //    pra /obrigado conseguir ler e disparar eventos pós-inscrição.
      const identityPayload = JSON.stringify({
        email: emailTrim,
        event_id: eventId,
        funnel_source: SOURCE,
      });
      try {
        document.cookie = `krob_lead_identity=${encodeURIComponent(identityPayload)}; domain=.SEU-DOMINIO.com; path=/; max-age=3600; SameSite=None; Secure`;
      } catch {
        // ignora
      }
      try {
        localStorage.setItem("krob_lead_identity", identityPayload);
      } catch {
        // localStorage indisponível (modo privado) — cookie cross-domain é o caminho principal
      }

      // 5. Inscrição é grátis — vai direto pra página de confirmação (não há checkout)
      window.location.href = "/obrigado";
    } catch (err) {
      console.error("Lead submit error:", err);
      toast.error("Erro de conexão. Tente novamente.");
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg bg-card border-border">
        <div className="text-center mb-2">
          <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight mb-3">
            Garanta sua vaga no webinar
          </h2>
          <p className="text-muted-foreground">
            Preencha seus dados para receber o link da aula ao vivo do{" "}
            <span className="font-mono text-primary">ConsultorIA</span>
          </p>
        </div>

        <div className="flex items-start gap-3 p-4 rounded-lg border border-primary/40 bg-primary/10">
          <CalendarClock className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
          <p className="text-sm text-foreground leading-relaxed">
            <span className="font-bold text-primary">Hoje às 14:30</span> (horário de Brasília).
            O link é enviado no seu <span className="font-bold">WhatsApp e e-mail</span> assim que você se inscreve.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 mt-2">
          <div className="space-y-2">
            <Label htmlFor="name">Nome Completo</Label>
            <Input
              id="name"
              type="text"
              placeholder="Digite seu nome"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={submitting}
              autoComplete="name"
              required
              className="border-2 focus-visible:ring-primary focus-visible:border-primary"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">E-mail</Label>
            <Input
              id="email"
              type="email"
              placeholder="seu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={submitting}
              autoComplete="email"
              spellCheck={false}
              autoCapitalize="none"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="phone">WhatsApp</Label>
            <Input
              id="phone"
              type="tel"
              inputMode="numeric"
              placeholder="(00) 00000-0000"
              value={phone}
              onChange={(e) => setPhone(formatPhone(e.target.value))}
              disabled={submitting}
              autoComplete="tel"
              required
            />
          </div>

          <Button
            type="submit"
            size="lg"
            disabled={submitting}
            className="w-full h-14 text-base font-bold tracking-wider uppercase bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_30px_-5px_hsl(var(--primary)_/_0.5)]"
          >
            {submitting ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Confirmando...
              </>
            ) : (
              <>
                <Clock className="w-4 h-4 mr-2" />
                Quero participar do webinar
              </>
            )}
          </Button>

          <p className="text-xs text-center text-muted-foreground font-mono">
            Vaga 100% gratuita · seus dados estão seguros
          </p>
        </form>
      </DialogContent>
    </Dialog>
  );
};
