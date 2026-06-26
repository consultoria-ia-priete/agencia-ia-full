// Cloudflare Pages Function: POST /api/lead
//
// Handles quiz form submissions:
//   1. Inserts the lead into D1 ({{TRACKING_DB_NAME}}.quiz_leads)
//   2. Fires a Lead event to the tracking stack ({{TRACKING_DOMAIN}}/tracker)
//      so it reaches Meta CAPI with Advanced Matching + fbp/fbc
//   3. Forwards lead data to the GoHighLevel webhook to trigger workflows
//
// All three steps run in parallel; one failure does not block the others.
// The lead row in D1 carries the status of each downstream call.

interface Env {
  DB: D1Database;
  GHL_WEBHOOK_URL?: string;
  TRACKER_URL?: string;
}

interface LeadPayload {
  name: string;
  phone: string;
  email?: string;
  profile_type?: string;
  success_percent?: number;
  answers?: unknown;
  /** Optional: client-generated event_id used by Pixel JS. If present, the
   *  CAPI fire reuses this value so Meta dedupes Pixel + CAPI into one event. */
  event_id?: string;
  utm?: {
    utm_source?: string;
    utm_medium?: string;
    utm_campaign?: string;
    utm_content?: string;
    utm_term?: string;
  };
}

const TRACKER_URL_DEFAULT = "https://{{TRACKING_DOMAIN}}/tracker";

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

function parseCookies(header: string): Record<string, string> {
  const out: Record<string, string> = {};
  for (const part of header.split(";")) {
    const eq = part.indexOf("=");
    if (eq < 0) continue;
    const k = part.slice(0, eq).trim();
    const v = part.slice(eq + 1).trim();
    if (k) out[k] = v;
  }
  return out;
}

function normalizePhoneBR(raw: string): string {
  const digits = (raw || "").replace(/\D/g, "");
  if (!digits) return "";
  if (digits.length >= 12 && digits.startsWith("55")) return digits;
  if (digits.length >= 10) return "55" + digits;
  return digits;
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

  let body: LeadPayload;
  try {
    body = await request.json();
  } catch {
    return json(400, { error: "invalid json" });
  }

  const name = (body.name || "").trim();
  const phone = (body.phone || "").trim();
  if (name.length < 2 || phone.replace(/\D/g, "").length < 10) {
    return json(400, { error: "name and phone are required" });
  }

  const phoneNormalized = normalizePhoneBR(phone);
  const email = (body.email || "").trim().toLowerCase();

  const cookies = parseCookies(request.headers.get("Cookie") || "");
  const sessionId = cookies["_krob_sid"] || "";
  const externalId = cookies["_krob_eid"] || "";
  const fbp = cookies["_fbp"] || "";
  const fbc = cookies["_fbc"] || "";
  const gclid = cookies["_gcl_aw"]?.split(".").pop() || cookies["_krob_gclid"] || "";

  const ip = request.headers.get("cf-connecting-ip") || "";
  const userAgent = request.headers.get("user-agent") || "";
  const referrer = request.headers.get("referer") || "";

  // Reuse client-supplied event_id (from Pixel JS) when present so Meta
  // dedupes browser-side Pixel + server-side CAPI as one event.
  const eventId = (typeof body.event_id === "string" && body.event_id.length > 0)
    ? body.event_id
    : crypto.randomUUID();
  const eventTime = Math.floor(Date.now() / 1000);

  const utm = body.utm || {};
  const profileType = body.profile_type || "";
  const successPercent = Number.isFinite(body.success_percent as number)
    ? (body.success_percent as number)
    : null;
  const answersJson = body.answers ? JSON.stringify(body.answers) : null;

  // ---------------------------------------------------------------------------
  // 1) Tracker: fire Lead event to {{TRACKING_DOMAIN}} (Meta CAPI + GA4 + event_log)
  // ---------------------------------------------------------------------------
  const trackerUrl = env.TRACKER_URL || TRACKER_URL_DEFAULT;
  const trackerPromise = fetch(trackerUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // Forward the original visitor's User-Agent and IP so the tracker's
      // bot detection treats this as a real user (the default Workers UA
      // matches the "headless" pattern and would skip Meta CAPI).
      "User-Agent": userAgent || "Mozilla/5.0",
      "X-Forwarded-For": ip || "",
      "CF-Connecting-IP": ip || "",
    },
    body: JSON.stringify({
      event_name: "Lead",
      event_id: eventId,
      event_time: eventTime,
      // Server-to-server fetch can't forward the visitor's _krob_sid cookie.
      // Pass the session_id explicitly so tracker.js can join with sessions.
      session_id: sessionId,
      external_id: externalId,
      event_source_url: referrer || "https://SEU-DOMINIO.com/",
      action_source: "website",
      user_data: {
        em: email || undefined,
        ph: phoneNormalized,
        fn: name.split(" ")[0] || undefined,
        ln: name.split(" ").slice(1).join(" ") || undefined,
        external_id: externalId || undefined,
        fbp: fbp || undefined,
        fbc: fbc || undefined,
        client_ip_address: ip || undefined,
        client_user_agent: userAgent || undefined,
      },
      custom_data: {
        content_name: "Quiz Negocio.IA",
        content_category: "quiz_funnel",
        profile_type: profileType,
        success_percent: successPercent,
      },
    }),
  })
    .then(async (r) => ({ status: r.status, ok: r.ok, body: await r.text() }))
    .catch((err) => ({ status: 0, ok: false, body: `fetch error: ${err.message}` }));

  // ---------------------------------------------------------------------------
  // 2) GHL webhook: forward lead to trigger workflows
  // ---------------------------------------------------------------------------
  const ghlPromise = env.GHL_WEBHOOK_URL
    ? fetch(env.GHL_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source: "quiz-negocio-ia",
          funnel_source: "quiz-negocio-ia",
          content_name: "Quiz Negocio.IA",
          content_category: "quiz_funnel",
          name,
          first_name: name.split(" ")[0],
          last_name: name.split(" ").slice(1).join(" ") || "",
          phone: "+" + phoneNormalized,
          email: email || undefined,
          profile_type: profileType,
          success_percent: successPercent,
          answers: body.answers,
          utm_source: utm.utm_source || "",
          utm_medium: utm.utm_medium || "",
          utm_campaign: utm.utm_campaign || "",
          utm_content: utm.utm_content || "",
          utm_term: utm.utm_term || "",
          session_id: sessionId,
          fbp,
          fbc,
          external_id: externalId,
          gclid,
          event_id: eventId,
          ip_address: ip,
          user_agent: userAgent,
          referrer,
          submitted_at: new Date().toISOString(),
        }),
      })
        .then(async (r) => ({ status: r.status, ok: r.ok, body: await r.text() }))
        .catch((err) => ({ status: 0, ok: false, body: `fetch error: ${err.message}` }))
    : Promise.resolve({ status: 0, ok: false, body: "GHL_WEBHOOK_URL not set" });

  const [trackerRes, ghlRes] = await Promise.all([trackerPromise, ghlPromise]);

  // ---------------------------------------------------------------------------
  // 3) Persist the lead row in D1 with the status of each downstream call
  // ---------------------------------------------------------------------------
  try {
    await env.DB.prepare(
      `INSERT INTO quiz_leads (
        funnel, session_id, fbp, fbc, external_id,
        name, phone, email, profile_type, success_percent, answers,
        utm_source, utm_medium, utm_campaign, utm_content, utm_term,
        ip_address, user_agent, referrer,
        ghl_status_code, ghl_response_ok, ghl_response_body,
        meta_event_id, meta_status_code, meta_response_ok
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
      .bind(
        "negocio-ia",
        sessionId,
        fbp,
        fbc,
        externalId,
        name,
        phoneNormalized,
        email,
        profileType,
        successPercent,
        answersJson,
        utm.utm_source || "",
        utm.utm_medium || "",
        utm.utm_campaign || "",
        utm.utm_content || "",
        utm.utm_term || "",
        ip,
        userAgent,
        referrer,
        ghlRes.status,
        ghlRes.ok ? 1 : 0,
        (ghlRes.body || "").slice(0, 500),
        eventId,
        trackerRes.status,
        trackerRes.ok ? 1 : 0
      )
      .run();
  } catch (err) {
    console.error("D1 insert quiz_leads error:", (err as Error).message);
    return json(500, {
      error: "lead saved partially — D1 insert failed",
      tracker: trackerRes.ok,
      ghl: ghlRes.ok,
    });
  }

  return json(200, {
    ok: true,
    event_id: eventId,
    tracker_ok: trackerRes.ok,
    ghl_ok: ghlRes.ok,
  });
};
