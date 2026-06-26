import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

// ─────────────────────────────────────────────────────────────────────────────
// CRM Funnels Dashboard — Quiz Funnel Analytics
// Parametrized for whitelabel reuse via CLIENT_* constants below.
// To clone for another client, change these constants + redeploy.
// ─────────────────────────────────────────────────────────────────────────────
const CLIENT_BRAND_NAME = "Negócio.IA";
const CLIENT_TOTAL_QUESTIONS = 17; // master Alex quiz: 5 triagem + 12 diagnóstico (P7 condicional) — Allan/others may differ

interface DashboardStats {
  ok: boolean;
  period: { from: string; to: string; from_unix: number; to_unix: number };
  kpis: {
    total_access: { value: number; change_pct: number };
    started: { value: number; conversion_pct: number };
    completed: { value: number; retention_pct: number };
    leads: { value: number; conversion_pct: number };
  };
  per_question: { step: number; count: number }[];
  leads_by_day: { day: string; count: number }[];
  top_leads: {
    id: number;
    name: string;
    email: string;
    phone: string;
    profile_type: string;
    success_percent: number;
    completed_at: number;
    max_step: number;
    status: "quente" | "morno" | "frio";
  }[];
}

function fmtDateISO(d: Date): string {
  return d.toISOString().slice(0, 10);
}
function todayMinus(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return fmtDateISO(d);
}
function fmtBR(dateISO: string): string {
  if (!dateISO) return "";
  const [y, m, d] = dateISO.split("-");
  return `${d}/${m}/${y}`;
}
function fmtDateTimeBR(unix: number): string {
  if (!unix) return "";
  const d = new Date(unix * 1000);
  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const hours = String(d.getHours()).padStart(2, "0");
  const minutes = String(d.getMinutes()).padStart(2, "0");
  const now = new Date();
  if (d.toDateString() === now.toDateString()) {
    return `Hoje, ${hours}:${minutes}`;
  }
  const yesterday = new Date(now);
  yesterday.setDate(now.getDate() - 1);
  if (d.toDateString() === yesterday.toDateString()) {
    return `Ontem, ${hours}:${minutes}`;
  }
  return `${day}/${month}, ${hours}:${minutes}`;
}

const Q_COLORS = [
  "#9ca3af", "#ef4444", "#f59e0b", "#fb923c", "#facc15", "#84cc16",
  "#FF5C39", "#D97757", "#CC785C", "#06b6d4", "#0ea5e9", "#3b82f6",
  "#6366f1", "#8b5cf6", "#a855f7", "#d946ef", "#ec4899",
];

const Dashboard = () => {
  const navigate = useNavigate();
  const [from, setFrom] = useState(todayMinus(7));
  const [to, setTo] = useState(todayMinus(0));
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const hasAuth = document.cookie.split(";").some((c) =>
      c.trim().startsWith("dash_logged_in=1")
    );
    if (!hasAuth) navigate("/dashboard/login", { replace: true });
  }, [navigate]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetch(`/api/dashboard/stats?from=${from}&to=${to}`)
      .then((r) => r.json())
      .then((data: DashboardStats) => {
        if (cancelled) return;
        if (!data.ok) throw new Error("API returned not ok");
        setStats(data);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err.message || "Erro ao carregar dados");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [from, to]);

  const perQuestionChartData = useMemo(() => {
    if (!stats) return [];
    const access = stats.kpis.total_access.value;
    const leads = stats.kpis.leads.value;
    const stepMap = new Map<number, number>();
    for (const r of stats.per_question) stepMap.set(r.step, r.count);

    const rows: { label: string; count: number; pct: number; color: string }[] = [];
    rows.push({ label: "Acessos", count: access, pct: 0, color: Q_COLORS[0] });
    for (let i = 1; i <= CLIENT_TOTAL_QUESTIONS; i++) {
      const count = stepMap.get(i) || 0;
      const prev = rows[rows.length - 1].count;
      const pct = prev > 0 ? Math.round((count / prev) * 100) : 0;
      rows.push({
        label: `Q${i}`,
        count,
        pct,
        color: Q_COLORS[(i % (Q_COLORS.length - 2)) + 1],
      });
    }
    const finalQCount = rows[rows.length - 1].count;
    const leadsPct = finalQCount > 0 ? Math.round((leads / finalQCount) * 100) : 0;
    rows.push({
      label: "Leads",
      count: leads,
      pct: leadsPct,
      color: Q_COLORS[Q_COLORS.length - 1],
    });
    return rows;
  }, [stats]);

  const funilRetencaoData = useMemo(() => {
    if (!stats) return [];
    const halfStep = Math.ceil(CLIENT_TOTAL_QUESTIONS / 2);
    const halfCount =
      stats.per_question.find((r) => r.step === halfStep)?.count || 0;
    return [
      { label: "Acessos", count: stats.kpis.total_access.value, color: "#3b82f6" },
      { label: "Iniciaram (Q1)", count: stats.kpis.started.value, color: "#a855f7" },
      { label: `Chegaram Q${halfStep}`, count: halfCount, color: "#f59e0b" },
      { label: "Leads (Whats)", count: stats.kpis.leads.value, color: "#FF5C39" },
    ];
  }, [stats]);

  const leadsByDayData = useMemo(() => {
    if (!stats) return [];
    const map = new Map<string, number>();
    for (const r of stats.leads_by_day) map.set(r.day, r.count);
    const days: { label: string; count: number }[] = [];
    const start = new Date(from);
    const end = new Date(to);
    for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
      const iso = fmtDateISO(d);
      const weekday = d.toLocaleDateString("pt-BR", { weekday: "short" }).replace(".", "");
      days.push({ label: weekday[0].toUpperCase() + weekday.slice(1), count: map.get(iso) || 0 });
    }
    return days.slice(-30);
  }, [stats, from, to]);

  function exportCsv() {
    if (!stats) return;
    const lines: string[] = [];
    lines.push("# CRM Funnels Dashboard — Quiz " + CLIENT_BRAND_NAME);
    lines.push(`# Período: ${fmtBR(from)} a ${fmtBR(to)}`);
    lines.push("");
    lines.push("## KPIs");
    lines.push("Total Acessos," + stats.kpis.total_access.value);
    lines.push("Iniciaram Quiz," + stats.kpis.started.value);
    lines.push("Finalizaram," + stats.kpis.completed.value);
    lines.push("Leads Gerados," + stats.kpis.leads.value);
    lines.push("");
    lines.push("## Análise por Pergunta");
    lines.push("Etapa,Sessions");
    for (const row of perQuestionChartData) lines.push(`${row.label},${row.count}`);
    lines.push("");
    lines.push("## Leads");
    lines.push("Nome,Email,WhatsApp,Pontuação,Status,Data");
    for (const lead of stats.top_leads) {
      lines.push(
        `${(lead.name || "").replace(/,/g, " ")},${lead.email},${lead.phone},${lead.max_step}/${CLIENT_TOTAL_QUESTIONS},${lead.status},${fmtDateTimeBR(lead.completed_at)}`
      );
    }
    const blob = new Blob([lines.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `dashboard-${CLIENT_BRAND_NAME.toLowerCase().replace(/\W+/g, "-")}-${from}_${to}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="min-h-screen bg-[#140a08] text-foreground p-6 md:p-10">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p className="text-xs font-medium tracking-wider text-primary uppercase mb-1">
              Painel Interno · Quiz {CLIENT_BRAND_NAME}
            </p>
            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">
              Dashboard Quiz {CLIENT_BRAND_NAME}
            </h1>
            <p className="text-sm text-muted-foreground mt-1">
              Acompanhe a retenção dos usuários em cada etapa do Quiz.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-black/40 border border-white/10 rounded-lg px-3 py-2">
              <input
                type="date"
                value={from}
                onChange={(e) => setFrom(e.target.value)}
                className="bg-transparent text-sm text-white outline-none [color-scheme:dark]"
              />
              <span className="text-white/50 text-xs">—</span>
              <input
                type="date"
                value={to}
                onChange={(e) => setTo(e.target.value)}
                className="bg-transparent text-sm text-white outline-none [color-scheme:dark]"
              />
            </div>
            <button
              onClick={exportCsv}
              disabled={!stats}
              className="bg-[#FF5C39] hover:bg-[#FF8A5C] disabled:opacity-40 text-black font-semibold text-sm rounded-lg px-4 py-2 transition-colors flex items-center gap-2"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" />
              </svg>
              Exportar CSV
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 text-sm text-red-200">
            Erro ao carregar dashboard: {error}
          </div>
        )}

        {loading && !stats && (
          <div className="text-center text-muted-foreground py-20">Carregando...</div>
        )}

        {stats && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <KpiCard
                label="Total de Acessos"
                value={stats.kpis.total_access.value}
                hint={
                  stats.kpis.total_access.change_pct >= 0
                    ? `↗ +${stats.kpis.total_access.change_pct}% vs período anterior`
                    : `↘ ${stats.kpis.total_access.change_pct}% vs período anterior`
                }
                hintColor={stats.kpis.total_access.change_pct >= 0 ? "text-[#FF8A5C]" : "text-red-400"}
                icon="users"
              />
              <KpiCard
                label="Iniciaram o Quiz"
                value={stats.kpis.started.value}
                hint={`${stats.kpis.started.conversion_pct}% de conversão da página inicial`}
                hintColor="text-muted-foreground"
                icon="target"
              />
              <KpiCard
                label={`Finalizaram (Q${CLIENT_TOTAL_QUESTIONS})`}
                value={stats.kpis.completed.value}
                hint={`${stats.kpis.completed.retention_pct}% de retenção no quiz`}
                hintColor="text-muted-foreground"
                icon="zap"
              />
              <KpiCard
                label="Leads Gerados"
                value={stats.kpis.leads.value}
                hint={`${stats.kpis.leads.conversion_pct}% deixaram o contato`}
                hintColor="text-muted-foreground"
                icon="trending"
              />
            </div>

            <div className="bg-black/40 border border-white/10 rounded-xl p-6">
              <h2 className="text-xl font-bold mb-1">Análise Detalhada por Pergunta</h2>
              <p className="text-sm text-muted-foreground mb-6">
                Quantidade de usuários e taxa de conversão passo a passo. Passe o mouse para ver os números exatos.
              </p>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={perQuestionChartData} margin={{ top: 30, right: 10, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff15" />
                  <XAxis dataKey="label" tick={{ fill: "#9ca3af", fontSize: 12 }} />
                  <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} />
                  <Tooltip
                    cursor={{ fill: "transparent" }}
                    contentStyle={{ background: "#000", border: "1px solid #ffffff20", borderRadius: 8 }}
                    formatter={(v: number, _n, item: { payload: { count: number; pct: number } }) => [
                      `${v} (${item.payload.pct}%)`,
                      "Sessions",
                    ]}
                  />
                  <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                    <LabelList dataKey="count" position="top" fill="#fff" fontSize={12} fontWeight={700} />
                    <LabelList
                      dataKey="pct"
                      position="center"
                      formatter={(v: number) => (v > 0 ? `${v}%` : "")}
                      fill="#fff"
                      fontSize={11}
                      fontWeight={700}
                    />
                    {perQuestionChartData.map((entry, i) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                <h2 className="text-xl font-bold mb-1">Funil de Retenção do Quiz</h2>
                <p className="text-sm text-muted-foreground mb-6">
                  Acompanhe a queda de usuários entre as perguntas.
                </p>
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={funilRetencaoData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff15" />
                    <XAxis dataKey="label" tick={{ fill: "#9ca3af", fontSize: 12 }} />
                    <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} />
                    <Tooltip cursor={{ fill: "transparent" }} contentStyle={{ background: "#000", border: "1px solid #ffffff20", borderRadius: 8 }} />
                    <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                      {funilRetencaoData.map((entry, i) => (
                        <Cell key={i} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-black/40 border border-white/10 rounded-xl p-6">
                <h2 className="text-xl font-bold mb-1">Leads Gerados por Dia</h2>
                <p className="text-sm text-muted-foreground mb-6">
                  Evolução da captura de contatos (WhatsApp).
                </p>
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={leadsByDayData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff15" />
                    <XAxis dataKey="label" tick={{ fill: "#9ca3af", fontSize: 12 }} />
                    <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} />
                    <Tooltip cursor={{ fill: "transparent" }} contentStyle={{ background: "#000", border: "1px solid #ffffff20", borderRadius: 8 }} />
                    <Line type="monotone" dataKey="count" stroke="#ef4444" strokeWidth={3} dot={{ r: 5, fill: "#ef4444" }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-black/40 border border-white/10 rounded-xl p-6">
              <h2 className="text-xl font-bold mb-1">Últimos Leads Gerados</h2>
              <p className="text-sm text-muted-foreground mb-6">
                Resumo dos últimos potenciais alunos que finalizaram o quiz.
              </p>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="text-xs uppercase tracking-wider text-muted-foreground">
                    <tr className="border-b border-white/10">
                      <th className="text-left py-3 px-2 font-semibold">Nome</th>
                      <th className="text-left py-3 px-2 font-semibold">WhatsApp</th>
                      <th className="text-left py-3 px-2 font-semibold">Pontuação (Nível)</th>
                      <th className="text-left py-3 px-2 font-semibold">Status</th>
                      <th className="text-right py-3 px-2 font-semibold">Data</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.top_leads.length === 0 && (
                      <tr>
                        <td colSpan={5} className="py-10 text-center text-muted-foreground">
                          Nenhum lead no período selecionado
                        </td>
                      </tr>
                    )}
                    {stats.top_leads.map((lead) => (
                      <tr key={lead.id} className="border-b border-white/5 hover:bg-white/5">
                        <td className="py-3 px-2 font-medium">{lead.name}</td>
                        <td className="py-3 px-2 text-muted-foreground">{lead.phone}</td>
                        <td className="py-3 px-2">{lead.max_step}/{CLIENT_TOTAL_QUESTIONS}</td>
                        <td className="py-3 px-2">
                          <StatusBadge status={lead.status} />
                        </td>
                        <td className="py-3 px-2 text-right text-muted-foreground">
                          {fmtDateTimeBR(lead.completed_at)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

function KpiCard({
  label,
  value,
  hint,
  hintColor,
  icon,
}: {
  label: string;
  value: number;
  hint: string;
  hintColor: string;
  icon: "users" | "target" | "zap" | "trending";
}) {
  return (
    <div className="bg-black/40 border border-white/10 rounded-xl p-5">
      <div className="flex items-start justify-between mb-3">
        <p className="text-sm text-muted-foreground">{label}</p>
        <IconBox icon={icon} />
      </div>
      <p className="text-3xl font-extrabold tracking-tight">{value.toLocaleString("pt-BR")}</p>
      <p className={`text-xs mt-2 ${hintColor}`}>{hint}</p>
    </div>
  );
}

function IconBox({ icon }: { icon: "users" | "target" | "zap" | "trending" }) {
  const path = {
    users: "M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    target: "M22 12h-4M6 12H2M12 6V2M12 22v-4M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10z",
    zap: "M13 2L3 14h9l-1 8 10-12h-9l1-8z",
    trending: "M23 6l-9.5 9.5-5-5L1 18M17 6h6v6",
  }[icon];
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-muted-foreground">
      <path d={path} />
    </svg>
  );
}

function StatusBadge({ status }: { status: "quente" | "morno" | "frio" }) {
  const styles = {
    quente: "bg-red-500 text-white",
    morno: "bg-white/10 text-white border border-white/20",
    frio: "border border-white/20 text-muted-foreground",
  }[status];
  const label = { quente: "Quente", morno: "Morno", frio: "Frio" }[status];
  return (
    <span className={`inline-block px-3 py-0.5 rounded-full text-xs font-semibold ${styles}`}>
      {label}
    </span>
  );
}

export default Dashboard;
