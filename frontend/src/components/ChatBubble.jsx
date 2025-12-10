import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";

export default function ChatBubble({ sender, text, timestamp, audio_url }) {
  const isUser = sender === "user";
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);

  /* ---------------------------------------------------------
     AUTO-PLAY AUDIO WHEN SARA SENDS A MESSAGE
  --------------------------------------------------------- */
  useEffect(() => {
    if (!isUser && audio_url) {
      const audio = new Audio(audio_url);
      audioRef.current = audio;

      audio.onended = () => setIsPlaying(false);

      setIsPlaying(true);
      audio.play().catch(() => {
        // Autoplay failed (browser restriction)
        setIsPlaying(false);
      });
    }
  }, [audio_url]);

  /* ---------------------------------------------------------
     PLAY / PAUSE BUTTON FOR MANUAL CONTROL
  --------------------------------------------------------- */
  const handlePlayClick = () => {
    if (!audio_url) return;

    if (!audioRef.current) {
      audioRef.current = new Audio(audio_url);
    }

    const audio = audioRef.current;

    if (isPlaying) {
      audio.pause();
      audio.currentTime = 0;
      setIsPlaying(false);
    } else {
      audio.play();
      setIsPlaying(true);
      audio.onended = () => setIsPlaying(false);
    }
  };

  /* ---------------------------------------------------------
     BUBBLE STYLING
  --------------------------------------------------------- */
  const bubbleStyle = {
    alignSelf: isUser ? "flex-end" : "flex-start",
    background: isUser ? "var(--color-accent)" : "var(--color-secondary)",
    color: "#444",
    padding: "12px 18px",
    borderRadius: "20px",
    maxWidth: "80%",
    width: "fit-content",
    boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
    animation: "bubbleEnter 0.35s ease-out",
    whiteSpace: "pre-wrap",
    position: "relative",
  };

  /* ---------------------------------------------------------
     CODE BLOCK COPY BUTTON
  --------------------------------------------------------- */
  const CopyButton = ({ code }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
      navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    };

    return (
      <button
        onClick={handleCopy}
        style={{
          position: "absolute",
          top: "6px",
          right: "6px",
          background: "#FFFFFFCC",
          border: "1px solid #D8B8FF",
          padding: "4px 8px",
          fontSize: "10px",
          borderRadius: "6px",
          cursor: "pointer",
          backdropFilter: "blur(4px)",
          color: "#8A4FBF",
          fontWeight: 600,
        }}
      >
        {copied ? "Copied!" : "Copy"}
      </button>
    );
  };

  /* ---------------------------------------------------------
     CODE BLOCK THEME
  --------------------------------------------------------- */
  const lavenderTheme = {
    'code[class*="language-"], pre[class*="language-"]': {
      color: "#4A2A66",
      background: "none",
      fontFamily: "Consolas, Monaco, monospace",
      fontSize: "14px",
    },
  };

  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div style={bubbleStyle}>
        {/* ----------------- PLAY BUTTON (ONLY FOR SARA) ----------------- */}
        {!isUser && audio_url && (
          <button
            onClick={handlePlayClick}
            style={{
              position: "absolute",
              bottom: "-10px",
              right: "-10px",
              background: "#fff",
              border: "1px solid #D8B8FF",
              borderRadius: "50%",
              width: "34px",
              height: "34px",
              cursor: "pointer",
              boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
              fontSize: "16px",
            }}
          >
            {isPlaying ? "⏸" : "🔊"}
          </button>
        )}

        {/* ----------------- MARKDOWN CONTENT ----------------- */}
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || "");
              const codeText = String(children).replace(/\n$/, "");

              return !inline ? (
                <div style={{ position: "relative", marginTop: 10 }}>
                  <CopyButton code={codeText} />
                  <SyntaxHighlighter
                    language={match ? match[1] : "text"}
                    style={lavenderTheme}
                    PreTag="div"
                    customStyle={{
                      background: "#F7E9FF",
                      border: "1px solid #E5C8FF",
                      color: "#4A2A66",
                      borderRadius: "12px",
                      padding: "14px",
                      fontSize: "14px",
                      overflowX: "auto",
                    }}
                    {...props}
                  >
                    {codeText}
                  </SyntaxHighlighter>
                </div>
              ) : (
                <code
                  style={{
                    background: "#F7E9FF",
                    border: "1px solid #E5C8FF",
                    padding: "2px 4px",
                    borderRadius: "4px",
                    fontSize: "14px",
                    color: "#4A2A66",
                  }}
                  {...props}
                >
                  {children}
                </code>
              );
            },
          }}
        >
          {text}
        </ReactMarkdown>
      </div>

      {/* ----------------- TIMESTAMP ----------------- */}
      <div
        style={{
          marginTop: "4px",
          fontSize: "12px",
          opacity: 0.55,
          color: "#6a5878",
          alignSelf: isUser ? "flex-end" : "flex-start",
          paddingLeft: isUser ? 0 : "6px",
        }}
      >
        {timestamp}
      </div>
    </div>
  );
}
