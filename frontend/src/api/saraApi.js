const API_BASE = "http://127.0.0.1:8000";

/* ---------------------------------------------------------
   SEND MESSAGE TO BACKEND (NOW RETURNS audio_url TOO)
--------------------------------------------------------- */
export async function sendMessage(text, sessionId = "default") {
  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });

    const data = await res.json();

    return {
      reply: data.reply,
      memory_update: data.memory_update,
      audio_url: data.audio_url || null,
    };
  } catch (err) {
    return {
      reply: "[ERROR] Backend unavailable",
      memory_update: false,
      audio_url: null,
    };
  }
}

/* ---------------------------------------------------------
   PERSONA SAVE
--------------------------------------------------------- */
export async function savePersonaConfig(cfg) {
  const res = await fetch(`${API_BASE}/api/persona`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cfg),
  });
  return await res.json();
}

/* ---------------------------------------------------------
   PERSONA LOAD
--------------------------------------------------------- */
export async function fetchPersonaConfig() {
  const res = await fetch(`${API_BASE}/api/persona`);
  if (!res.ok) return null;
  return await res.json();
}
