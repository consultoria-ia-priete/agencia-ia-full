import { useState } from "react";
import { useNavigate } from "react-router-dom";

const DashboardLogin = () => {
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/dashboard/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      const data = (await res.json()) as { ok: boolean; error?: string };
      if (data.ok) {
        navigate("/dashboard", { replace: true });
      } else {
        setError(data.error || "Falha no login");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro de rede");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#140a08] text-foreground flex items-center justify-center p-6">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm bg-black/40 border border-white/10 rounded-xl p-8 space-y-6"
      >
        <div className="text-center space-y-2">
          <p className="text-xs font-medium tracking-wider text-primary uppercase">
            Painel Interno
          </p>
          <h1 className="text-2xl font-extrabold tracking-tight">Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Acesso restrito. Informe a senha pra continuar.
          </p>
        </div>

        <div className="space-y-2">
          <label htmlFor="password" className="text-xs uppercase tracking-wider text-muted-foreground font-medium">
            Senha
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
            required
            className="w-full bg-black/60 border border-white/10 rounded-lg px-4 py-3 text-white outline-none focus:border-primary/50 transition-colors"
          />
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-sm text-red-200">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !password}
          className="w-full bg-[#FF5C39] hover:bg-[#FF8A5C] disabled:opacity-40 text-black font-bold tracking-wider uppercase rounded-lg py-3 transition-colors"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
};

export default DashboardLogin;
