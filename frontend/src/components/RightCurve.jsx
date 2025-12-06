function RightCurve() {
  return (
    <svg
      width="300"
      height="100%"
      viewBox="0 0 300 1000"
      preserveAspectRatio="none"
      style={{
        position: "absolute",
        right: 0,
        top: 0,
        height: "100%",
        zIndex: 1,
        pointerEvents: "none",
      }}
    >
      <path
        d="M0 0 Q260 500 0 1000"
        fill="none"
        stroke="rgba(255, 200, 220, 0.35)"
        strokeWidth="2"
      />
    </svg>
  );
}

export default RightCurve;
