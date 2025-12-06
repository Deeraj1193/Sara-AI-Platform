// RightNav.jsx
import MemoryIcon from "../assets/svg/memory.svg";
import NotesIcon from "../assets/svg/notes.svg";
import PersonaIcon from "../assets/svg/persona.svg";
import StarIcon from "../assets/svg/star.svg";
import SettingsIcon from "../assets/svg/setting.svg";

function RightNav({ onSelect }) {
  const commonButton = {
    width: "48px",
    height: "48px",
    borderRadius: "50%",
    background: "rgba(255,255,255,0.55)",
    backdropFilter: "blur(12px)",
    boxShadow: "0 4px 18px rgba(0,0,0,0.12)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    cursor: "pointer",
    transition: "0.25s ease",
  };

  return (
    <div
      style={{
        width: "88px",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-evenly",
        alignItems: "center",
        padding: "20px 0",
      }}
    >
      {/* Memory */}
      <div className="nav-button" style={commonButton} onClick={() => onSelect("memory")}>
        <img src={MemoryIcon} style={{ width: 24, height: 24 }} />
      </div>

      {/* Notes */}
      <div className="nav-button" style={commonButton} onClick={() => onSelect("notes")}>
        <img src={NotesIcon} style={{ width: 22, height: 22 }} />
      </div>

      {/* Persona */}
      <div className="nav-button" style={commonButton} onClick={() => onSelect("persona")}>
        <img src={PersonaIcon} style={{ width: 24, height: 24 }} />
      </div>

      {/* Star */}
      <div className="nav-button" style={commonButton}>
        <img src={StarIcon} style={{ width: 22, height: 22 }} />
      </div>

      {/* Settings */}
      <div className="nav-button" style={commonButton}>
        <img src={SettingsIcon} style={{ width: 22, height: 22 }} />
      </div>
    </div>
  );
}

export default RightNav;
