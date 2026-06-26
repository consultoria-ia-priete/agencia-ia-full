// POST /api/dashboard/login
// Validates password against env var DASHBOARD_PASSWORD and sets dash_auth cookie.
// Cookie has 7-day TTL, HttpOnly + SameSite=None so it works inside cross-site iframes
// (e.g. embedded as a CRM Funnels custom menu link).

interface Env {
  DASHBOARD_PASSWORD?: string;
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

async function constantTimeEqual(a: string, b: string): Promise<boolean> {
  // Avoid early-exit timing leaks. Hash both sides and compare.
  const enc = new TextEncoder();
  const ha = await crypto.subtle.digest("SHA-256", enc.encode(a));
  const hb = await crypto.subtle.digest("SHA-256", enc.encode(b));
  const va = new Uint8Array(ha);
  const vb = new Uint8Array(hb);
  if (va.length !== vb.length) return false;
  let diff = 0;
  for (let i = 0; i < va.length; i++) diff |= va[i] ^ vb[i];
  return diff === 0;
}

export const onRequestOptions: PagesFunction = async () =>
  new Response(null, { headers: corsHeaders() });

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  try {
    const body = (await request.json()) as { password?: string };
    const expected = env.DASHBOARD_PASSWORD || "";

    if (!expected) {
      return new Response(
        JSON.stringify({ ok: false, error: "DASHBOARD_PASSWORD not set on server" }),
        { status: 500, headers: { "Content-Type": "application/json", ...corsHeaders() } }
      );
    }

    if (!body.password) {
      return new Response(JSON.stringify({ ok: false, error: "password required" }), {
        status: 400,
        headers: { "Content-Type": "application/json", ...corsHeaders() },
      });
    }

    const ok = await constantTimeEqual(body.password, expected);
    if (!ok) {
      return new Response(JSON.stringify({ ok: false, error: "invalid password" }), {
        status: 401,
        headers: { "Content-Type": "application/json", ...corsHeaders() },
      });
    }

    // Issue cookie. Token is the SHA-256 of the password (one-way) — server validates by re-hashing
    // the env var on every request. Not as robust as a JWT but sufficient for a single-user dashboard.
    const enc = new TextEncoder();
    const tokenHash = await crypto.subtle.digest("SHA-256", enc.encode(expected));
    const token = Array.from(new Uint8Array(tokenHash))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");

    const sevenDaysSec = 7 * 24 * 3600;
    const authCookie = `dash_auth=${token}; Path=/; Max-Age=${sevenDaysSec}; HttpOnly; Secure; SameSite=None`;
    // Non-HttpOnly hint cookie so the SPA can detect logged-in state without exposing the token.
    const hintCookie = `dash_logged_in=1; Path=/; Max-Age=${sevenDaysSec}; Secure; SameSite=None`;

    const headers = new Headers({ "Content-Type": "application/json", ...corsHeaders() });
    headers.append("Set-Cookie", authCookie);
    headers.append("Set-Cookie", hintCookie);

    return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return new Response(JSON.stringify({ ok: false, error: msg }), {
      status: 500,
      headers: { "Content-Type": "application/json", ...corsHeaders() },
    });
  }
};
