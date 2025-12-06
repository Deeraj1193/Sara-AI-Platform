// TopBar.jsx
import SearchIcon from "../assets/svg/search.svg";
import StarIcon from "../assets/svg/star.svg";
import UserIcon from "../assets/svg/user.svg";

function TopBar() {
  return (
    <div
      style={{
        height: "var(--topbar-height)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 20px",
        background: "rgba(255,255,255,0.85)",
        backdropFilter: "blur(10px)",
        borderBottom: "1px solid rgba(220,180,200,0.4)",
        boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
        position: "relative",
        zIndex: 9999,
      }}
    >
      {/* LEFT SIDE */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <div
          style={{
            width: 40,
            height: 40,
            borderRadius: "50%",
            background: "linear-gradient(135deg,#FFF,#FAD4E8)",
            boxShadow: "0 4px 14px rgba(200,140,180,0.15)",
          }}
        />
        <div>
          <div style={{ fontSize: 18, fontWeight: 700, color: "#C64DA5" }}>Sara</div>
          <div style={{ fontSize: 12, color: "rgba(80,60,80,0.5)" }}>Your assistant</div>
        </div>
      </div>

      {/* RIGHT ICONS */}
      <div style={{ display: "flex", gap: 18 }}>
        <img src={SearchIcon} style={{ width: 20, cursor: "pointer" }} />
        <img src={StarIcon} style={{ width: 20, cursor: "pointer" }} />
        <img src={UserIcon} style={{ width: 20, cursor: "pointer" }} />
      </div>
    </div>
  );
}

export default TopBar;
