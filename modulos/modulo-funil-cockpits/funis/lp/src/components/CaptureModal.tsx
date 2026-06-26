import { useState } from "react";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AlertTriangle, AlertOctagon, Lock } from "lucide-react";
import { toast } from "sonner";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const LASTLINK_URL = "https://lastlink.com/p/{{LASTLINK_PRODUTO_ALT}}/checkout-payment/";

const formatPhone = (raw: string) => {
  const digits = raw.replace(/\D/g, "").slice(0, 11);
  if (digits.length <= 2) return `(${digits}`;
  if (digits.length <= 7) return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
  return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
};

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

const buildCheckoutUrl = (trk: string): string => {
  if (typeof window === "undefined") return LASTLINK_URL;
  const url = new URL(LASTLINK_URL);
  url.searchParams.set("utm_content", trk);
  const sp = new URLSearchParams(window.location.search);
  for (const k of ["utm_source", "utm_medium", "utm_campaign", "utm_term"]) {
    const v = sp.get(k);
    if (v) url.searchParams.set(k, v);
  }
  return url.toString();
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

      // 1. Pixel JS Lead com mesmo eventID — Meta dedupa com CAPI
      if (typeof window !== "undefined" && (window as any).fbq) {
        (window as any).fbq(
          "track",
          "Lead",
          {
            content_name: "LP Negocio.IA",
            content_category: "low_ticket",
            value: 37,
            currency: "BRL",
          },
          { eventID: eventId }
        );
      }

      // 2. Server-side: D1 + Meta CAPI + GHL
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
          source: "lp-negocio-ia",
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
        toast.error("Não conseguimos registrar seus dados. Tente novamente.");
        setSubmitting(false);
        return;
      }

      // 3. Pixel InitiateCheckout (sinaliza intenção forte de compra pra Meta)
      if (typeof window !== "undefined" && (window as any).fbq) {
        (window as any).fbq("track", "InitiateCheckout", {
          content_name: "negocio.ia",
          value: 37,
          currency: "BRL",
        });
      }

      // 4. Salva identidade do lead em cookie cross-domain (.SEU-DOMINIO.com) + localStorage
      //    Lead que comprou pela LP NegocioIA é redirecionado pelo Lastlink pra /obrigado
      //    em SEU-DOMINIO.com — cookie cross-domain garante que a identidade
      //    seja lida nesse subdomínio diferente.
      const identityPayload = JSON.stringify({
        email: emailTrim,
        event_id: eventId,
        funnel_source: "lp-negocio-ia",
      });
      try {
        document.cookie = `krob_lead_identity=${encodeURIComponent(identityPayload)}; domain=.SEU-DOMINIO.com; path=/; max-age=3600; SameSite=None; Secure`;
      } catch {
        // ignora
      }
      try {
        localStorage.setItem("krob_lead_identity", identityPayload);
      } catch {
        // localStorage indisponível
      }

      // 5. Redireciona pro Lastlink com trk = eventId pra atribuição completa
      const checkoutUrl = buildCheckoutUrl(eventId);
      window.location.href = checkoutUrl;
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
            Falta muito pouco!
          </h2>
          <p className="text-muted-foreground">
            Preencha seus dados para liberar seu acesso ao{" "}
            <span className="font-mono text-primary">negócio.ia</span>
          </p>
        </div>

        <div className="flex items-start gap-3 p-4 rounded-lg border border-red-500/40 bg-red-950/30">
          <AlertOctagon className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-100 leading-relaxed">
            <AlertTriangle className="inline w-4 h-4 text-yellow-400 mr-1 -mt-0.5" />
            <span className="font-bold text-red-300">Urgente:</span> Restam poucas vagas com o
            valor promocional de R$37. Garanta a sua agora antes que o preço suba!
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
            className="w-full h-14 text-base font-bold bg-gradient-to-r from-primary to-[#FF5C39] hover:from-primary hover:to-[#FF8A5C] text-primary-foreground shadow-[0_0_30px_-5px_hsl(var(--primary)_/_0.5)]"
          >
            <Lock className="w-4 h-4 mr-2" />
            {submitting ? "Redirecionando..." : "Ir para Pagamento Seguro"}
          </Button>

          <p className="text-xs text-center text-muted-foreground font-mono">
            Ambiente 100% seguro e criptografado
          </p>
        </form>
      </DialogContent>
    </Dialog>
  );
};
