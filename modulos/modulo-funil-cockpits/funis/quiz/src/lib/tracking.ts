// Quiz funnel event tracking utility.
// Dispatches step-by-step events to /api/quiz-progress for dashboard analytics.

const SESSION_KEY = "krob_quiz_sid";

function getOrCreateSessionId(): string {
  // Prefer the same _krob_sid cookie used by the tracking stack middleware,
  // so quiz_step events join naturally with PageView/Lead events.
  if (typeof document !== "undefined") {
    const match = document.cookie.match(/(?:^|;\s*)_krob_sid=([^;]+)/);
    if (match) return decodeURIComponent(match[1]);
  }
  if (typeof localStorage !== "undefined") {
    let sid = localStorage.getItem(SESSION_KEY);
    if (!sid) {
      sid = crypto.randomUUID();
      localStorage.setItem(SESSION_KEY, sid);
    }
    return sid;
  }
  return crypto.randomUUID();
}

export interface QuizEventPayload {
  step_number?: number;
  metadata?: Record<string, unknown>;
}

export function dispatchQuizEvent(eventName: string, payload: QuizEventPayload = {}): void {
  if (typeof window === "undefined") return;

  const body = {
    session_id: getOrCreateSessionId(),
    event_name: eventName,
    event_id: crypto.randomUUID(),
    step_number: payload.step_number,
    metadata: payload.metadata,
  };

  // sendBeacon is fire-and-forget and survives page unload — perfect for analytics.
  // Falls back to fetch keepalive if sendBeacon isn't available.
  try {
    const blob = new Blob([JSON.stringify(body)], { type: "application/json" });
    if (navigator.sendBeacon && navigator.sendBeacon("/api/quiz-progress", blob)) {
      return;
    }
  } catch {
    // fall through to fetch
  }

  fetch("/api/quiz-progress", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    keepalive: true,
  }).catch(() => {
    // analytics failure is non-fatal — never block the user's quiz flow
  });
}
