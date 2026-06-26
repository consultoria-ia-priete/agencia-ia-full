// Cloudflare Pages Function: POST /api/group-click
//
// Disparado pelo botão "Entrar no Grupo do WhatsApp" na página /obrigado.
// Encaminha pro webhook GHL que move o opportunity do contato pra stage
// "Entrou no Grupo do Webinar" no pipeline Funil SSCIA.

interface Env {
  DB: D1Database;
  GHL_WEBHOOK_GROUP_CLICK_URL?: string;
}

interface GroupClickPayload {
  email?: string;
  event_id?: string;
  funnel_source?: string;
}

function corsHeaders(origin: string): Record<string, string> {
  const allowed = origin.endsWith(".SEU-DOMINIO.com") || origin === "https://SEU-DOMINIO.com";
  return {
    "Access-Control-Allow-Origin": allowed ? origin : "https://SEU-DOMINIO.com",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}

export const onRequestOptions: PagesFunction<Env> = async ({ request }) => {
  return new Response(null, {
    status: 204,
    headers: corsHeaders(request.headers.get("origin") || ""),
  });
};

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const origin = request.headers.get("origin") || "";
  const cors = corsHeaders(origin);
  const json = (status: number, body: unknown) =>
    new Response(JSON.stringify(body), {
      status,
      headers: { "Content-Type": "application/json", ...cors },
    });

  let body: GroupClickPayload;
  try {
    body = await request.json();
  } catch {
    return json(400, { error: "invalid json" });
  }

  const email = (body.email || "").trim().toLowerCase();
  const eventId = (body.event_id || "").trim();
  const funnelSource = (body.funnel_source || "quiz-negocio-ia").trim();

  if (!email && !eventId) {
    return json(400, { error: "email or event_id required" });
  }

  const ip = request.headers.get("cf-connecting-ip") || "";
  const userAgent = request.headers.get("user-agent") || "";

  const ghlPromise = env.GHL_WEBHOOK_GROUP_CLICK_URL
    ? fetch(env.GHL_WEBHOOK_GROUP_CLICK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          event: "group_click",
          email: email || undefined,
          event_id: eventId || undefined,
          funnel_source: funnelSource,
          clicked_at: new Date().toISOString(),
          ip_address: ip,
          user_agent: userAgent,
        }),
      })
        .then(async (r) => ({ status: r.status, ok: r.ok, body: await r.text() }))
        .catch((err) => ({ status: 0, ok: false, body: `fetch error: ${err.message}` }))
    : Promise.resolve({ status: 0, ok: false, body: "GHL_WEBHOOK_GROUP_CLICK_URL not set" });

  const ghlRes = await ghlPromise;

  try {
    await env.DB.prepare(
      `INSERT INTO quiz_leads (
        funnel, name, phone, email, profile_type,
        ip_address, user_agent,
        ghl_status_code, ghl_response_ok, ghl_response_body,
        meta_event_id
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
      .bind(
        `group-click-${funnelSource}`,
        "[group-click event]",
        "",
        email || "",
        "",
        ip,
        userAgent,
        ghlRes.status,
        ghlRes.ok ? 1 : 0,
        (ghlRes.body || "").slice(0, 500),
        eventId || null
      )
      .run();
  } catch (err) {
    console.error("D1 insert group_click event error:", (err as Error).message);
  }

  return json(200, { ok: true, ghl_ok: ghlRes.ok });
};
