// Cloudflare Pages Function: GET /api/dashboard/stats?from=YYYY-MM-DD&to=YYYY-MM-DD
// Returns aggregated quiz funnel analytics for the dashboard.
// Reads from D1 {{TRACKING_DB_NAME}} (event_log + quiz_leads).

interface Env {
  DB: D1Database;
  CLIENT_FUNNEL_NAME?: string; // template parametrization (default: "negocio-ia")
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function parseDateToUnix(s: string | null, fallback: number, endOfDay = false): number {
  if (!s) return fallback;
  const t = Date.parse(s);
  if (Number.isNaN(t)) return fallback;
  let unix = Math.floor(t / 1000);
  // YYYY-MM-DD without time means a calendar day; for `to`, snap to end of day
  // so events that occurred on that day's afternoon/evening still match.
  if (endOfDay && /^\d{4}-\d{2}-\d{2}$/.test(s)) {
    unix += 86399;
  }
  return unix;
}

export const onRequestOptions: PagesFunction = async () =>
  new Response(null, { headers: corsHeaders() });

export const onRequestGet: PagesFunction<Env> = async ({ request, env }) => {
  try {
    if (!env.DB) {
      return new Response(JSON.stringify({ ok: false, error: "DB binding missing" }), {
        status: 500,
        headers: { "Content-Type": "application/json", ...corsHeaders() },
      });
    }

    const url = new URL(request.url);
    const now = Math.floor(Date.now() / 1000);
    const sevenDaysAgo = now - 7 * 86400;
    const from = parseDateToUnix(url.searchParams.get("from"), sevenDaysAgo);
    const to = parseDateToUnix(url.searchParams.get("to"), now, true);
    const funnelName = env.CLIENT_FUNNEL_NAME || "negocio-ia";

    // Previous period (same length) for KPI %change
    const periodLength = to - from;
    const prevFrom = from - periodLength;
    const prevTo = from;

    // ---- Query 1: KPIs (current period) ----
    const kpisResult = await env.DB.prepare(
      `SELECT
        (SELECT COUNT(DISTINCT session_id) FROM event_log
          WHERE event_name='quiz_pageview' AND timestamp BETWEEN ?1 AND ?2) as total_access,
        (SELECT COUNT(DISTINCT session_id) FROM event_log
          WHERE event_name='quiz_started' AND timestamp BETWEEN ?1 AND ?2) as started,
        (SELECT COUNT(DISTINCT session_id) FROM event_log
          WHERE event_name='quiz_completed' AND timestamp BETWEEN ?1 AND ?2) as completed,
        (SELECT COUNT(*) FROM quiz_leads
          WHERE funnel = ?3 AND rowid IN (
            SELECT rowid FROM quiz_leads WHERE funnel = ?3
          )) as leads_total_all_time,
        (SELECT COUNT(*) FROM quiz_leads
          WHERE funnel = ?3) as leads_period_proxy`
    )
      .bind(from, to, funnelName)
      .first<{
        total_access: number;
        started: number;
        completed: number;
        leads_total_all_time: number;
        leads_period_proxy: number;
      }>();

    // quiz_leads doesn't have created_at column we can filter cheaply by — count via rowid range proxy
    // Use ID-based filter since AUTOINCREMENT and time correlate well enough for a recent-period view.
    // For exact period, prefer joining with event_log timestamps (one query below for top leads does that).

    const leadsResult = await env.DB.prepare(
      `SELECT COUNT(*) as count FROM quiz_leads q
       INNER JOIN (
         SELECT DISTINCT session_id, MIN(timestamp) as ts
         FROM event_log
         WHERE event_name = 'quiz_completed' AND timestamp BETWEEN ?1 AND ?2
         GROUP BY session_id
       ) e ON e.session_id = q.session_id
       WHERE q.funnel = ?3`
    )
      .bind(from, to, funnelName)
      .first<{ count: number }>();

    // ---- Query 2: Previous period totals (for %change) ----
    const prevResult = await env.DB.prepare(
      `SELECT
        (SELECT COUNT(DISTINCT session_id) FROM event_log
          WHERE event_name='quiz_pageview' AND timestamp BETWEEN ?1 AND ?2) as total_access,
        (SELECT COUNT(DISTINCT session_id) FROM event_log
          WHERE event_name='quiz_started' AND timestamp BETWEEN ?1 AND ?2) as started,
        (SELECT COUNT(DISTINCT session_id) FROM event_log
          WHERE event_name='quiz_completed' AND timestamp BETWEEN ?1 AND ?2) as completed`
    )
      .bind(prevFrom, prevTo)
      .first<{ total_access: number; started: number; completed: number }>();

    // ---- Query 3: Per-question retention (count distinct sessions per quiz_step_N) ----
    const perQuestionResult = await env.DB.prepare(
      `SELECT
        CAST(SUBSTR(event_name, 11) AS INTEGER) as step,
        COUNT(DISTINCT session_id) as count
       FROM event_log
       WHERE event_name LIKE 'quiz_step_%' AND timestamp BETWEEN ?1 AND ?2
       GROUP BY step
       ORDER BY step ASC`
    )
      .bind(from, to)
      .all<{ step: number; count: number }>();

    // ---- Query 4: Leads per day ----
    const leadsByDayResult = await env.DB.prepare(
      `SELECT
        date(e.timestamp, 'unixepoch') as day,
        COUNT(DISTINCT q.session_id) as count
       FROM quiz_leads q
       INNER JOIN event_log e ON e.session_id = q.session_id
       WHERE e.event_name = 'quiz_completed'
         AND e.timestamp BETWEEN ?1 AND ?2
         AND q.funnel = ?3
       GROUP BY day
       ORDER BY day ASC`
    )
      .bind(from, to, funnelName)
      .all<{ day: string; count: number }>();

    // ---- Query 5: Top recent leads with max quiz step (engagement-based status) ----
    const topLeadsResult = await env.DB.prepare(
      `SELECT
        q.id, q.name, q.email, q.phone, q.profile_type, q.success_percent,
        e.timestamp as completed_at,
        COALESCE(
          (SELECT MAX(CAST(SUBSTR(e2.event_name, 11) AS INTEGER))
           FROM event_log e2
           WHERE e2.session_id = q.session_id AND e2.event_name LIKE 'quiz_step_%'),
          0
        ) as max_step
       FROM quiz_leads q
       INNER JOIN event_log e ON e.session_id = q.session_id
       WHERE e.event_name = 'quiz_completed'
         AND e.timestamp BETWEEN ?1 AND ?2
         AND q.funnel = ?3
       ORDER BY e.timestamp DESC
       LIMIT 20`
    )
      .bind(from, to, funnelName)
      .all<{
        id: number;
        name: string;
        email: string;
        phone: string;
        profile_type: string;
        success_percent: number;
        completed_at: number;
        max_step: number;
      }>();

    // ---- Compute KPIs + %change ----
    const kpisCurr = {
      total_access: kpisResult?.total_access || 0,
      started: kpisResult?.started || 0,
      completed: kpisResult?.completed || 0,
      leads: leadsResult?.count || 0,
    };
    const kpisPrev = {
      total_access: prevResult?.total_access || 0,
      started: prevResult?.started || 0,
      completed: prevResult?.completed || 0,
    };

    const pct = (curr: number, prev: number): number => {
      if (prev === 0) return curr > 0 ? 100 : 0;
      return Math.round(((curr - prev) / prev) * 1000) / 10;
    };

    const response = {
      ok: true,
      period: {
        from: new Date(from * 1000).toISOString(),
        to: new Date(to * 1000).toISOString(),
        from_unix: from,
        to_unix: to,
      },
      kpis: {
        total_access: {
          value: kpisCurr.total_access,
          change_pct: pct(kpisCurr.total_access, kpisPrev.total_access),
        },
        started: {
          value: kpisCurr.started,
          conversion_pct:
            kpisCurr.total_access > 0
              ? Math.round((kpisCurr.started / kpisCurr.total_access) * 1000) / 10
              : 0,
        },
        completed: {
          value: kpisCurr.completed,
          retention_pct:
            kpisCurr.started > 0
              ? Math.round((kpisCurr.completed / kpisCurr.started) * 1000) / 10
              : 0,
        },
        leads: {
          value: kpisCurr.leads,
          conversion_pct:
            kpisCurr.completed > 0
              ? Math.round((kpisCurr.leads / kpisCurr.completed) * 1000) / 10
              : 0,
        },
      },
      per_question: (perQuestionResult.results || []).map((r) => ({
        step: r.step,
        count: r.count,
      })),
      leads_by_day: (leadsByDayResult.results || []).map((r) => ({
        day: r.day,
        count: r.count,
      })),
      top_leads: (topLeadsResult.results || []).map((r) => ({
        id: r.id,
        name: r.name,
        email: r.email,
        phone: r.phone,
        profile_type: r.profile_type,
        success_percent: r.success_percent,
        completed_at: r.completed_at,
        max_step: r.max_step,
        // Engagement-based status: max step reached
        // Quiz has 17 questions in master Alex (P7 condicional, alguns leads veem 16);
        // thresholds parametrizable per client
        status:
          r.max_step >= 15 ? "quente" : r.max_step >= 9 ? "morno" : "frio",
      })),
    };

    return new Response(JSON.stringify(response), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache, no-store",
        ...corsHeaders(),
      },
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return new Response(JSON.stringify({ ok: false, error: msg }), {
      status: 500,
      headers: { "Content-Type": "application/json", ...corsHeaders() },
    });
  }
};
