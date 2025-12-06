// InputBar.jsx
import { useState } from "react";
import SendIcon from "../assets/svg/Send.svg";

function InputBar({ onSend }) {
  const [value, setValue] = useState("");

  const handleSend = () => {
    if (!value.trim()) return;
    onSend(value);
    setValue("");
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        width: "100%",
        backgroundColor: "var(--color-secondary)",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-full)",
        padding: "0 var(--space-16)",
        height: "var(--input-height)",
        boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
        gap: "var(--space-16)",
      }}
    >
      <input
        type="text"
        placeholder="Type a message..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        style={{
          flex: 1,
          border: "none",
          outline: "none",
          fontSize: "16px",
          background: "none",
          color: "#A08FBF",
        }}
      />

      <img
        src={SendIcon}
        onClick={handleSend}
        style={{
          width: "28px",
          height: "28px",
          cursor: "pointer",
          opacity: 0.9,
        }}
      />
    </div>
  );
}

export default InputBar;
