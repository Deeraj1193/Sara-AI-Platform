// MainLayout.jsx
import TopBar from "./TopBar";
import ChatBubble from "../components/ChatBubble";
import InputBar from "../components/InputBar";
import MemoryPanel from "../components/MemoryPanel";
import NotesPanel from "../components/NotesPanel";
import PersonaPanel from "../components/PersonaPanel";
import RightNav from "../components/RightNav";
import PinkGlow from "../assets/glow/PinkGlow";

import { useState, useRef, useEffect } from "react";
import { sendMessage } from "../api/saraApi";

function MainLayout() {
  const [activePanel, setActivePanel] = useState("memory");

  // Initial demo messages
  const [messages, setMessages] = useState([
    { sender: "sara", text: "Hello! I'm Sara.", timestamp: "10:01" },
    { sender: "user", text: "Hi Sara, this looks nice!", timestamp: "10:01" },
    { sender: "sara", text: "We are building your UI now!", timestamp: "10:02" },
  ]);

  const [isTyping, setIsTyping] = useState(false);
  const [memoryRefreshKey, setMemoryRefreshKey] = useState(0);

  const chatEndRef = useRef(null);

  // ----------------------------------------------------
  // SMART SCROLL: only scroll after messages settle
  // ----------------------------------------------------
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (!isTyping) {
      scrollToBottom();
    }
  }, [messages, isTyping]);

  // ----------------------------------------------------
  // SEND MESSAGE (NON-STREAMING)
  // ----------------------------------------------------
  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    // Add user message immediately
    setMessages((prev) => [
      ...prev,
      { sender: "user", text, timestamp },
    ]);

    // Show typing indicator
    setIsTyping(true);

    // Call backend
    const response = await sendMessage(text, "default");

    setIsTyping(false);

    // Add Sara reply
    setMessages((prev) => [
      ...prev,
      {
        sender: "sara",
        text: response.reply || "[No reply]",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);

    // Refresh memory panel
    if (response.memory_update) {
      setMemoryRefreshKey((prev) => prev + 1);
    }
  };

  return (
    <div
      style={{
        position: "relative",
        width: "100vw",
        height: "100vh",
        overflow: "hidden",
        background: "transparent",
        isolation: "isolate",
      }}
    >
      <PinkGlow />

      <div
        style={{
          position: "relative",
          zIndex: 10,
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* TOP BAR */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            zIndex: 999,
          }}
        >
          <TopBar />
        </div>

        {/* MAIN LAYOUT */}
        <div
          style={{
            flex: 1,
            display: "flex",
            overflow: "hidden",
            marginTop: "var(--topbar-height)",
          }}
        >
          {/* LEFT CHAT COLUMN */}
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              padding: "16px",
              background: "rgba(255,255,255,0.18)",
              backdropFilter: "blur(8px)",
              borderRight: "1px solid rgba(255,180,220,0.35)",
              overflow: "hidden",
              position: "relative",
            }}
          >
            {/* Divider shimmer */}
            <div
              style={{
                position: "absolute",
                top: 0,
                right: 0,
                width: "4px",
                height: "100%",
                borderRadius: "2px",
                background:
                  "linear-gradient(to bottom, rgba(255,190,225,0.18), rgba(255,150,210,0.55), rgba(255,190,225,0.18))",
                filter: "blur(0.6px)",
                animation: "shimmerFlow 6.5s ease-in-out infinite",
              }}
            />

            {/* CHAT MESSAGES */}
            <div
              style={{
                flex: 1,
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
                gap: "16px",
                paddingRight: "10px",
              }}
            >
              {messages.map((msg, index) => (
                <ChatBubble
                  key={index}
                  sender={msg.sender}
                  text={msg.text}
                  timestamp={msg.timestamp}
                />
              ))}

              {isTyping && (
                <div
                  style={{
                    alignSelf: "flex-start",
                    background: "var(--color-secondary)",
                    padding: "10px 16px",
                    borderRadius: "20px",
                    display: "flex",
                    gap: "4px",
                  }}
                >
                  <span className="dot">•</span>
                  <span className="dot">•</span>
                  <span className="dot">•</span>
                </div>
              )}

              <div ref={chatEndRef} />
            </div>

            <InputBar onSend={handleSendMessage} />
          </div>

          {/* RIGHT PANEL */}
          <div
            style={{
              width: "420px",
              padding: "24px",
              overflowY: "auto",
              background: "rgba(255,255,255,0.12)",
              backdropFilter: "blur(10px)",
            }}
          >
            {activePanel === "memory" && (
              <MemoryPanel refreshKey={memoryRefreshKey} />
            )}
            {activePanel === "notes" && <NotesPanel />}
            {activePanel === "persona" && <PersonaPanel />}
          </div>

          {/* NAV */}
          <div
            style={{
              width: "88px",
              background: "rgba(255,255,255,0.12)",
              backdropFilter: "blur(10px)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <RightNav onSelect={setActivePanel} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default MainLayout;
