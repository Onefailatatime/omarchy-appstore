import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { C, MONO, SANS } from "./theme";

const rise = (f: number, at: number, len = 16) => interpolate(f, [at, at + len], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const fade = (f: number, until?: number) => (until === undefined ? 1 : interpolate(f, [until - 12, until], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));

/* One big line that rises in and, optionally, fades out. */
export const Big: React.FC<{ at: number; until?: number; size?: number; color?: string; mono?: boolean; y?: number; upper?: boolean; children: React.ReactNode }> =
  ({ at, until, size = 112, color = C.white, mono = false, y = 0, upper = false, children }) => {
  const f = useCurrentFrame();
  if (f < at || (until !== undefined && f >= until)) return null;
  const p = rise(f, at);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ fontFamily: mono ? MONO : SANS, fontWeight: mono ? 700 : 800, fontSize: size, color, letterSpacing: upper ? "0.08em" : mono ? 0 : "-0.03em",
        textTransform: upper ? "uppercase" : "none", lineHeight: 1.1, textAlign: "center", padding: "0 140px",
        opacity: p * fade(f, until), transform: `translateY(${y + (1 - Easing.out(Easing.cubic)(p)) * 46}px)` }}>{children}</div>
    </AbsoluteFill>
  );
};

export const Stack: React.FC<{ lines: { text: string; at: number; color?: string }[]; until: number; size?: number; mono?: boolean; upper?: boolean }> =
  ({ lines, until, size = 104, mono = false, upper = false }) => {
  const f = useCurrentFrame();
  if (f < lines[0].at || f >= until) return null;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: fade(f, until) }}>
      <div style={{ fontFamily: mono ? MONO : SANS, fontWeight: mono ? 700 : 800, fontSize: size, lineHeight: 1.12, letterSpacing: upper ? "0.08em" : mono ? 0 : "-0.03em", textTransform: upper ? "uppercase" : "none", textAlign: "center" }}>
        {lines.map((l) => {
          const p = rise(f, l.at);
          return <div key={l.text} style={{ color: l.color ?? C.white, opacity: p, transform: `translateY(${(1 - Easing.out(Easing.cubic)(p)) * 40}px)` }}>{l.text}</div>;
        })}
      </div>
    </AbsoluteFill>
  );
};
