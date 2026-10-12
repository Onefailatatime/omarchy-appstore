import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { C, MONO, SANS } from "./theme";

/* Shared closing frame so both videos end on the same image. */
export const EndCard: React.FC<{ from: number; fade?: boolean }> = ({ from, fade = false }) => {
  const f = useCurrentFrame() - from;
  const o = fade ? interpolate(f, [0, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  const sub = interpolate(f, [18, 34], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: o }}>
      <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 124, letterSpacing: "-0.03em", color: C.white, lineHeight: 1 }}>
        omarchy<span style={{ color: C.blue }}>apps</span>.com
      </div>
      <div style={{ fontFamily: MONO, fontSize: 40, color: C.orange, marginTop: 34, opacity: sub }}>
        the upgrade lands next week
      </div>
    </AbsoluteFill>
  );
};
