// Middleware: protects /api/dashboard/* (except /login) by validating dash_auth cookie.
// dash_auth = SHA-256(DASHBOARD_PASSWORD), set by /api/dashboard/login on success.

interface Env {
  DASHBOARD_PASSWORD?: string;
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

async function expectedToken(password: string): Promise<string> {
  const enc = new TextEncoder();
  const buf = await crypto.subtle.digest("SHA-256", enc.encode(password));
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

export const onRequest: PagesFunction<Env> = async ({ request, env, next }) => {
  const url = new URL(request.url);

  // Allow login endpoint without auth
  if (url.pathname.endsWith("/api/dashboard/login")) {
    return next();
  }

  // Allow CORS preflight
  if (request.method === "OPTIONS") {
    return next();
  }

  const password = env.DASHBOARD_PASSWORD || "";
  if (!password) {
    return new Response(
      JSON.stringify({ ok: false, error: "DASHBOARD_PASSWORD not configured" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }

  const cookies = parseCookies(request.headers.get("Cookie") || "");
  const provided = cookies["dash_auth"] || "";
  const expected = await expectedToken(password);

  if (provided !== expected) {
    return new Response(JSON.stringify({ ok: false, error: "unauthorized" }), {
      status: 401,
      headers: { "Content-Type": "application/json" },
    });
  }

  return next();
};
