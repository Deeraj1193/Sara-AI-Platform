import NotesIcon from "../assets/svg/Notes.svg";

function NotesPanel() {
  return (
    <div style={{ paddingRight: "8px", width: "100%" }}>

      {/* HEADER with Icon */}
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
          src={NotesIcon}
          alt="notes icon"
          style={{ width: "26px", height: "26px", opacity: 0.9 }}
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
          Notes
        </h2>
      </div>

      {/* NOTES MOCK DATA */}
      {[
        {
          title: "Meeting – Dec 3",
          text: "Sara learned new preferences today while talking to the user.",
        },
        {
          title: "Reminder",
          text: "User prefers a gentle tone and soft UI styling.",
        },
      ].map((note, index) => (
        <div
          key={index}
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
          {/* Note Title */}
          <h3
            style={{
              margin: 0,
              fontSize: "18px",
              fontWeight: 600,
              color: "rgba(120, 70, 100, 0.9)",
            }}
          >
            {note.title}
          </h3>

          {/* Note Description */}
          <p
            style={{
              marginTop: "8px",
              fontSize: "14px",
              color: "rgba(120, 70, 100, 0.75)",
              lineHeight: "1.4",
            }}
          >
            {note.text}
          </p>
        </div>
      ))}
    </div>
  );
}

export default NotesPanel;
