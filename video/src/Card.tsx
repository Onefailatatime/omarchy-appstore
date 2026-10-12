import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { C, SANS } from "./theme";

/* Full-screen statement between acts. Hard cut in, lines rise one after another. */
export const Card: React.FC<{ from: number; lines: { text: string; at: number; color?: string }[]; size?: number }> = ({ from, lines, size = 128 }) => {
  const f = useCurrentFrame() - from;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", background: C.night }}>
      <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: size, lineHeight: 1.08, letterSpacing: "-0.03em", textAlign: "center", padding: "0 120px" }}>
        {lines.map((l) => {
          const p = interpolate(f, [l.at, l.at + 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return <div key={l.text} style={{ color: l.color ?? C.white, opacity: p, transform: `translateY(${(1 - Easing.out(Easing.cubic)(p)) * 50}px)` }}>{l.text}</div>;
        })}
      </div>
    </AbsoluteFill>
  );
};

export const Stat: React.FC<{ at: number; from: number; label: string; value: string }> = ({ at, from, label, value }) => {
  const f = useCurrentFrame() - from;
  const p = interpolate(f, [at, at + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ opacity: p, transform: `translateY(${(1 - p) * 30}px)`, display: "grid", justifyItems: "center", gap: 6 }}>
      <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 112, color: C.white, letterSpacing: "-0.03em", lineHeight: 1 }}>{value}</div>
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 30, color: C.blue }}>{label}</div>
    </div>
  );
};
