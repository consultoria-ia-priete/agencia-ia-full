// Cloudflare Pages Function: POST /api/quiz-progress
// Logs quiz funnel step events directly to D1 event_log table.
// Bypasses Meta CAPI/GA4 (these are funnel analytics, not commercial events).

interface QuizProgressBody {
  session_id?: string;
  event_name: string;     // e.g. "quiz_started", "quiz_step_1", "quiz_completed"
  event_id?: string;      // UUID, frontend generates
  step_number?: number;
  metadata?: Record<string, unknown>;
}

interface Env {
  DB: D1Database;
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function parseCookies(header: string): Record<string, string> {
  const out: Record<string, string> = {};
  if (!header) return out;
  for (const part of header.split(";")) {
    const [k, ...rest] = part.trim().split("=");
    if (k) out[k] = decodeURIComponent(rest.join("="));
  }
  return out;
}

export const onRequestOptions: PagesFunction = async () =>
  new Response(null, { headers: corsHeaders() });

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  try {
    const body = (await request.json()) as QuizProgressBody;

    if (!body.event_name) {
      return new Response(JSON.stringify({ ok: false, error: "event_name required" }), {
        status: 400,
        headers: { "Content-Type": "application/json", ...corsHeaders() },
      });
    }

    const cookies = parseCookies(request.headers.get("Cookie") || "");
    const sessionId = body.session_id || cookies["_krob_sid"] || "";
    const eventId = body.event_id || crypto.randomUUID();
    const timestamp = Math.floor(Date.now() / 1000);

    const userAgent = request.headers.get("user-agent") || "";
    const isMobile = /Mobile|Android|iPhone|iPad/i.test(userAgent) ? 1 : 0;

    if (!env.DB) {
      return new Response(JSON.stringify({ ok: false, error: "DB binding missing" }), {
        status: 500,
        headers: { "Content-Type": "application/json", ...corsHeaders() },
      });
    }

    await env.DB.prepare(
      `INSERT INTO event_log (
        session_id, event_name, event_id, timestamp,
        is_mobile,
        sent_to_meta, sent_to_ga4,
        consent_status
      ) VALUES (?, ?, ?, ?, ?, 0, 0, 'quiz_internal')`
    )
      .bind(sessionId, body.event_name, eventId, timestamp, isMobile)
      .run();

    return new Response(
      JSON.stringify({ ok: true, event_id: eventId, session_id: sessionId }),
      { status: 200, headers: { "Content-Type": "application/json", ...corsHeaders() } }
    );
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return new Response(JSON.stringify({ ok: false, error: msg }), {
      status: 500,
      headers: { "Content-Type": "application/json", ...corsHeaders() },
    });
  }
};
