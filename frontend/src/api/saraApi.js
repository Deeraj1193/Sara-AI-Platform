const API_BASE = "http://127.0.0.1:8000";

export async function sendMessage(text, sessionId = "default") {
  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });
    return await res.json();
  } catch (err) {
    return { reply: "[ERROR] Backend unavailable", memory_update: false };
  }
}

/* -------- PERSONA CONFIG API -------- */

export async function savePersonaConfig(cfg) {
  const res = await fetch(`${API_BASE}/api/persona`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cfg),
  });
  return await res.json();
}

export async function fetchPersonaConfig() {
  const res = await fetch(`${API_BASE}/api/persona`);
  if (!res.ok) return null;
  return await res.json();
}
