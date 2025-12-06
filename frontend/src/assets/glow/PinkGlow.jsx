function PinkGlow() {
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        overflow: "hidden",
        zIndex: -1,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "30%",
          left: "10%",
          width: "550px",
          height: "550px",
          borderRadius: "50%",
          background: "rgba(250,200,230,0.55)",
          filter: "blur(180px)",
        }}
      />
    </div>
  );
}

export default PinkGlow;
