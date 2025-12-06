import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";

export default function ChatBubble({ sender, text, timestamp }) {
  const isUser = sender === "user";

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
  };

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
