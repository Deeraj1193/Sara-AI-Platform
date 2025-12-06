import { useState, useEffect } from "react";

export default function PersonaPanel() {
  const [persona, setPersona] = useState(null);
  const [saved, setSaved] = useState(false);

  // ---------------------------------------------------
  // Fetch persona settings from backend on load
  // ---------------------------------------------------
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/persona")
      .then((r) => r.json())
      .then((data) => setPersona(data));
  }, []);

  if (!persona) return <div>Loading...</div>;

  const updatePersona = (updated) => {
    const newState = { ...persona, ...updated };
    setPersona(newState);
  };

  const savePersona = () => {
    fetch("http://127.0.0.1:8000/api/persona", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(persona),
    });

    setSaved(true);
    setTimeout(() => setSaved(false), 1200);
  };

  // ---------------------------------------------------
  // BEAUTIFUL UI STYLES
  // ---------------------------------------------------
  const cardStyle = {
    background: "rgba(255,255,255,0.65)",
    backdropFilter: "blur(14px)",
    borderRadius: "22px",
    padding: "22px 26px",
    boxShadow: "0 4px 20px rgba(255,150,200,0.25)",
    marginBottom: "22px",
  };

  const sectionTitle = {
    fontSize: "18px",
    fontWeight: 700,
    color: "#b44ca0",
    marginBottom: "14px",
  };

  const labelStyle = {
    fontSize: "14px",
    fontWeight: 600,
    marginBottom: "6px",
    color: "#704c78",
  };

  const sliderStyle = {
    width: "100%",
    marginTop: "4px",
    accentColor: "#e88ad6",
    cursor: "pointer",
  };

  // ---------------------------------------------------
  // Mode Selector Button
  // ---------------------------------------------------
  const ModeButton = ({ label }) => {
    const active = persona.mode === label.toLowerCase();

    return (
      <button
        onClick={() =>
          updatePersona({ mode: label.toLowerCase() })
        }
        style={{
          padding: "10px 18px",
          borderRadius: "14px",
          border: active ? "2px solid #ff9adc" : "2px solid #f4ccea",
          background: active ? "#ffd9f2" : "#ffffffaa",
          color: active ? "#cc2a85" : "#7a4a70",
          fontWeight: 600,
          cursor: "pointer",
          transition: "0.25s",
          backdropFilter: "blur(4px)",
        }}
      >
        {label}
      </button>
    );
  };

  // ---------------------------------------------------
  // Toggle Switch Component
  // ---------------------------------------------------
  const Toggle = ({ label, field }) => {
    const value = persona.toggles[field];

    return (
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "10px 0",
        }}
      >
        <span style={labelStyle}>{label}</span>

        <label
          style={{
            position: "relative",
            width: "46px",
            height: "24px",
            display: "inline-block",
          }}
        >
          <input
            type="checkbox"
            checked={value}
            onChange={(e) =>
              updatePersona({
                toggles: {
                  ...persona.toggles,
                  [field]: e.target.checked,
                },
              })
            }
            style={{ display: "none" }}
          />
          <span
            style={{
              position: "absolute",
              cursor: "pointer",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: value ? "#ff9adc" : "#d2b6d8",
              borderRadius: "24px",
              transition: "0.25s",
            }}
          />
          <span
            style={{
              position: "absolute",
              height: "18px",
              width: "18px",
              left: value ? "24px" : "4px",
              bottom: "3px",
              backgroundColor: "white",
              borderRadius: "50%",
              transition: "0.25s",
              boxShadow: "0 2px 4px rgba(0,0,0,0.25)",
            }}
          />
        </label>
      </div>
    );
  };

  // ---------------------------------------------------
  // Slider Component — now fully working
  // ---------------------------------------------------
// ---------------------------------------------------
// SMOOTH SLIDER (fixed clunkiness)
// ---------------------------------------------------
const Slider = ({ label, field }) => {
  const value = persona.sliders[field];

  // Local smooth value (does NOT re-render whole persona)
  const [tempValue, setTempValue] = useState(value);

  // When persona value changes externally, sync it
  useEffect(() => {
    setTempValue(value);
  }, [value]);

  const commitValue = (newVal) => {
    updatePersona({
      sliders: {
        ...persona.sliders,
        [field]: Number(newVal),
      },
    });
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <div
        style={{
          ...labelStyle,
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <span>{label}</span>
        <span style={{ color: "#b44ca0" }}>{tempValue}</span>
      </div>

      <input
        type="range"
        min={0}
        max={100}
        value={tempValue}
        onChange={(e) => {
          // Live update UI smoothly
          setTempValue(e.target.value);
        }}
        onMouseUp={(e) => commitValue(e.target.value)}
        onPointerUp={(e) => commitValue(e.target.value)}
        style={{
          width: "100%",
          accentColor: "#e88ad6",
          cursor: "pointer",
        }}
      />
    </div>
  );
};


  // ---------------------------------------------------
  // RENDER UI
  // ---------------------------------------------------
  return (
    <div style={{ width: "100%", padding: "4px" }}>
      {/* TITLE */}
      <h2 style={{ fontSize: "28px", color: "#c84fbf", marginBottom: "18px" }}>
        Persona
      </h2>

      {/* MODE CARD */}
      <div style={cardStyle}>
        <div style={sectionTitle}>Mode</div>
        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          <ModeButton label="Gremlin" />
          <ModeButton label="Teaching" />
          <ModeButton label="Professional" />
        </div>
      </div>

      {/* TOGGLES CARD */}
      <div style={cardStyle}>
        <div style={sectionTitle}>Behavior Toggles</div>

        <Toggle label="Use Emojis" field="useEmojis" />
        <Toggle label="Formal Tone" field="formalTone" />
        <Toggle label="Child Mode (no swearing)" field="childMode" />
        <Toggle label="Sound (TTS)" field="soundOn" />
        <Toggle label="Free Talk (auto-chat)" field="freeTalk" />
      </div>

      {/* SLIDERS CARD */}
      <div style={cardStyle}>
        <div style={sectionTitle}>Personality Sliders</div>

        <Slider label="Swear Level" field="swearLevel" />
        <Slider label="Roast Level" field="roastLevel" />
        <Slider label="Verbosity" field="verbosity" />
        <Slider label="Spontaneity" field="spontaneity" />
      </div>

      {/* SAVE BUTTON */}
      <button
        onClick={savePersona}
        style={{
          width: "100%",
          marginTop: "10px",
          padding: "14px",
          borderRadius: "14px",
          border: "none",
          background: saved ? "#d477ff" : "#ffb7ef",
          color: "white",
          fontSize: "16px",
          fontWeight: 700,
          cursor: "pointer",
          transition: "0.25s",
          boxShadow: "0 4px 12px rgba(200,100,200,0.3)",
        }}
      >
        {saved ? "Saved ✓" : "Save Persona"}
      </button>
    </div>
  );
}
