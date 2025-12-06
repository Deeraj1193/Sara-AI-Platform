import { useState, useEffect } from "react";
import MemoryIcon from "../assets/svg/Memory.svg";

function MemoryPanel({ refreshKey }) {
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch memory from backend
  const loadMemories = async () => {
    try {
      setLoading(true);

      const res = await fetch("http://127.0.0.1:8000/api/memory");
      const data = await res.json();

      setMemories(data.items || []);
    } catch (err) {
      console.error("Memory fetch failed:", err);
    } finally {
      setLoading(false);
    }
  };

  // Load whenever refreshKey changes
  useEffect(() => {
    loadMemories();
  }, [refreshKey]);

  return (
    <div style={{ paddingRight: "8px", width: "100%" }}>
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "10px",
          marginBottom: "24px",
        }}
      >
        <img
          src={MemoryIcon}
          alt="memory icon"
          style={{ width: "28px", height: "28px", opacity: 0.9 }}
        />
        <h2
          style={{
            fontSize: "24px",
            fontWeight: 600,
            margin: 0,
            color: "rgba(210, 120, 160, 0.9)",
            letterSpacing: "0.4px",
            textAlign: "center",
          }}
        >
          Memory
        </h2>
      </div>

      {/* LOADING */}
      {loading && (
        <p style={{ textAlign: "center", opacity: 0.6 }}>
          Loading memories...
        </p>
      )}

      {/* EMPTY */}
      {!loading && memories.length === 0 && (
        <p style={{ textAlign: "center", opacity: 0.6 }}>
          No memories stored yet.
        </p>
      )}

      {/* MEMORY CARDS */}
      {memories.map((m) => (
        <div
          key={m.id}
          style={{
            background: "rgba(255, 240, 250, 0.85)",
            borderRadius: "20px",
            padding: "20px",
            marginBottom: "24px",
            border: "1px solid rgba(255, 200, 225, 0.6)",
            boxShadow: "0 8px 24px rgba(255,180,220,0.25)",
            backdropFilter: "blur(10px)",
          }}
        >
          <h3
            style={{
              margin: 0,
              fontSize: "18px",
              fontWeight: 600,
              color: "rgba(120, 70, 100, 0.9)",
            }}
          >
            Memory #{m.id}
          </h3>

          <p
            style={{
              marginTop: "8px",
              fontSize: "14px",
              color: "rgba(120, 70, 100, 0.75)",
              lineHeight: "1.4",
              whiteSpace: "pre-wrap",
            }}
          >
            {m.text}
          </p>
        </div>
      ))}
    </div>
  );
}

export default MemoryPanel;
