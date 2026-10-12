import { useLayoutEffect, useMemo, useRef } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, MONO } from "./theme";
import { useSiteFonts } from "./fonts";
import { EndCard } from "./EndCard";
import { Big, Stack } from "./Text";
import T from "./timeline.json";
import pkgs from "./packages.json";
import stats from "./stats.json";
import { FACTS } from "./facts";

const R = T.arcade;
const W = 1920, H = 1080;
const DIM = "rgba(122,162,247,0.62)";
const GHOSTS = [C.pink, C.magenta, C.cyan, C.green];
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
const blink = (f: number, period = 16) => Math.floor(f / period) % 2 === 0;

/* CRT: scanlines plus a soft vignette, over everything. */
const CRT = () => (
  <>
    <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0 2px, transparent 2px 5px)", pointerEvents: "none" }} />
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)", pointerEvents: "none" }} />
  </>
);

const Arc: React.FC<{ size?: number; color?: string; style?: React.CSSProperties; children: React.ReactNode }> = ({ size = 34, color = C.white, style, children }) => (
  <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: size, color, letterSpacing: "0.1em", textTransform: "uppercase", ...style }}>{children}</div>
);

const KATA = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789";
function rng(seed: number) { return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }

const Rain: React.FC = () => {
  const ref = useRef<HTMLCanvasElement>(null);
  const f = useCurrentFrame();
  const cols = useMemo(() => {
    const r = rng(4242), cell = 22, n = Math.ceil(W / cell), out = [];
    for (let i = 0; i < n; i++) {
      const glyphs = []; for (let g = 0; g < 80; g++) glyphs.push(KATA[Math.floor(r() * KATA.length)]);
      out.push({ y0: -r() * 60, v: 0.5 + r() * 1.1, len: 8 + Math.floor(r() * 18), glyphs });
    }
    return { cell, n, out };
  }, []);
  useLayoutEffect(() => {
    const ctx = ref.current?.getContext("2d"); if (!ctx) return;
    ctx.clearRect(0, 0, W, H);
    const t = Math.min(f, R.rainEnd);                                        // freezes at rainEnd
    const fadeOut = 1 - clamp01((f - R.rainEnd) / 30);
    ctx.font = `700 ${cols.cell - 2}px 'JetBrains Mono', monospace`; ctx.textBaseline = "top";
    cols.out.forEach((c, i) => {
      const head = c.y0 + c.v * t;
      for (let k = 0; k < c.len; k++) {
        const row = Math.floor(head) - k; if (row < 0 || row * cols.cell > H) continue;
        const a = (k === 0 ? 1 : 0.75 * (1 - k / c.len)) * fadeOut;
        ctx.fillStyle = k === 0 ? `rgba(192,202,245,${a})` : `rgba(158,206,106,${a})`;
        ctx.fillText(c.glyphs[(row + i) % c.glyphs.length], i * cols.cell, row * cols.cell);
      }
    });
  }, [f, cols]);
  return <canvas ref={ref} width={W} height={H} style={{ position: "absolute", inset: 0 }} />;
};

/* Pac-Man sprite: an orange disc with a chomping wedge. */
const Pac: React.FC<{ x: number; y: number; size?: number; chomp?: boolean; style?: React.CSSProperties }> = ({ x, y, size = 64, chomp = true, style }) => {
  const f = useCurrentFrame();
  const open = chomp ? 12 + 30 * (0.5 + 0.5 * Math.sin(f * 0.9)) : 20;
  const r = size / 2, a1 = (open * Math.PI) / 180, a2 = ((360 - open) * Math.PI) / 180;
  const d = `M${r},${r} L${r + r * Math.cos(a1)},${r + r * Math.sin(a1)} A${r},${r} 0 1 1 ${r + r * Math.cos(a2)},${r + r * Math.sin(a2)} Z`;
  return (
    <svg width={size} height={size} style={{ position: "absolute", left: x - r, top: y - r, ...style }}>
      <path d={d} fill={C.orange} />
      <circle cx={r + 2} cy={r * 0.5} r={size * 0.07} fill={C.night} />
    </svg>
  );
};

const Ghost: React.FC<{ x: number; y: number; color: string; size?: number; scared?: boolean }> = ({ x, y, color, size = 56, scared = false }) => {
  const f = useCurrentFrame();
  const s = size, wob = Math.floor(f / 6) % 2;
  const fill = scared ? (blink(f, 8) ? C.blue : C.white) : color;
  return (
    <svg width={s} height={s} viewBox="0 0 56 56" style={{ position: "absolute", left: x - s / 2, top: y - s / 2 }}>
      <path d={`M4 56 V28 A24 24 0 0 1 52 28 V56 L44 ${wob ? 48 : 52} L36 56 L28 ${wob ? 48 : 52} L20 56 L12 ${wob ? 48 : 52} Z`} fill={fill} />
      {!scared && <><circle cx="19" cy="26" r="7" fill={C.white} /><circle cx="37" cy="26" r="7" fill={C.white} /><circle cx="21" cy="27" r="3.5" fill={C.night} /><circle cx="39" cy="27" r="3.5" fill={C.night} /></>}
      {scared && <><rect x="14" y="22" width="6" height="6" fill={C.night} /><rect x="36" y="22" width="6" height="6" fill={C.night} /><path d="M12 42 l6 -5 l6 5 l6 -5 l6 5 l6 -5 l6 5" stroke={C.night} strokeWidth="3" fill="none" /></>}
    </svg>
  );
};

/* A lane of dots and app names that Pac-Man eats left to right over `len` frames. */
const Lane: React.FC<{ y: number; start: number; len: number; names: string[]; ghost: string; onScore?: (eaten: number) => void }> = ({ y, start, len, names, ghost }) => {
  const f = useCurrentFrame();
  const p = clamp01((f - start) / len);
  if (f < start - 10 || f > start + len + 30) return null;
  const x0 = 140, x1 = W - 140, px = x0 + (x1 - x0) * p;
  const slots = 18;
  return (
    <>
      {Array.from({ length: slots }, (_, i) => {
        const sx = x0 + 60 + ((x1 - x0 - 120) * i) / (slots - 1);
        if (sx < px) return null;
        const name = i % 3 === 1 ? names[Math.floor(i / 3) % names.length] : null;
        return name
          ? <Arc key={i} size={32} color={C.white} style={{ position: "absolute", left: sx, top: y - 20, transform: "translateX(-50%)", letterSpacing: "0.04em", textTransform: "none" }}>{name}</Arc>
          : <div key={i} style={{ position: "absolute", left: sx - 6, top: y - 6, width: 14, height: 14, borderRadius: 7, background: C.white, opacity: 0.85 }} />;
      })}
      <Pac x={px} y={y} />
      <Ghost x={px - 150 - 40 * Math.sin(f / 7)} y={y} color={ghost} />
    </>
  );
};

const fmt4 = (n: number) => String(Math.round(n)).padStart(4, "0");
const fmt = (n: number) => n.toLocaleString("en-US");

export const Arcade = () => {
  useSiteFonts();
  const f = useCurrentFrame();
  const st = stats as { visitorsLastMonth: number | null; growthPct: number | null; projectionNextMonth: number | null };
  const audio = <Audio src={staticFile("audio/arcade.wav")} />;
  if (f >= R.endCard) return <AbsoluteFill style={{ background: C.night }}>{audio}<EndCard from={R.endCard} /><CRT /></AbsoluteFill>;

  const credit = f >= R.coin ? 1 : 0;
  const score = f < R.lanes ? 0 : f < R.levelUp ? interpolate(f, [R.lanes, R.levelUp - 10], [0, FACTS.packages], { extrapolateRight: "clamp" }) : FACTS.packages;
  const day = f >= R.lone && f < R.gameOver ? Math.min(30, Math.floor(interpolate(f, [R.lone, R.gameOver - 20], [1, 30], { extrapolateRight: "clamp" }))) : null;
  const dark = f >= R.dark ? 1 - 0.85 * clamp01((f - R.dark) / 20) : 1;
  const lanesOn = f >= R.lanes && f < R.levelUp;
  const names = pkgs.slice(0, 18);
  const hintWord = (w: string) => { const r = rng(f * 7 + 1); return f < R.hints + 40 && blink(f, 3) ? w.replace(/[a-z]/g, (ch) => (r() < 0.5 ? ch : KATA[Math.floor(r() * 10)])) : w; };

  return (
    <AbsoluteFill style={{ background: C.night, overflow: "hidden" }}>
      {audio}
      <AbsoluteFill style={{ opacity: dark }}>
        {f < R.rainEnd + 30 && <Rain />}
        {/* HUD */}
        {f >= R.ready && (
          <div style={{ position: "absolute", left: 120, right: 120, top: 70, display: "flex", justifyContent: "space-between" }}>
            <Arc color={C.white}>1UP <span style={{ color: C.orange }}>{fmt4(score)}</span></Arc>
            <Arc color={C.white}>HIGH <span style={{ color: C.orange }}>{fmt4(FACTS.packages)}</span></Arc>
            <Arc color={C.white}>CREDIT <span style={{ color: C.orange }}>{credit}</span></Arc>
          </div>
        )}
        {f >= R.ready && f < R.lone && blink(f, 10) && <Big at={R.ready} mono upper size={64}>Player 1 Ready</Big>}

        {/* act 1: alone on an empty lane */}
        {f >= R.lone && f < R.gameOver && (
          <>
            <div style={{ position: "absolute", left: 140, right: 140, top: H / 2 - 1, height: 2, background: C.tblack }} />
            <Pac x={W / 2} y={H / 2} chomp={false} />
            {day !== null && <Arc size={30} color={DIM} style={{ position: "absolute", right: 120, top: 150 }}>Day {String(day).padStart(2, "0")} · Stars {day >= 30 ? 1 : 0}</Arc>}
            <Big at={R.lines[0]} until={R.lines[1]} mono upper size={54} color={C.blue} y={300}>You shipped an app.</Big>
            <Big at={R.lines[1]} until={R.lines[2]} mono upper size={54} color={C.blue} y={300}>You pushed it to a repo.</Big>
            <Big at={R.lines[2]} until={R.gameOver} mono upper size={54} color={C.blue} y={300}>No dots. No players. Just hope.</Big>
          </>
        )}
        {f >= R.gameOver && f < R.insertCoin && <Big at={R.gameOver} mono upper size={120} color={C.pink}>Game over?</Big>}
        {f >= R.insertCoin && f < R.stage1 && blink(f, 9) && <Big at={R.insertCoin} mono upper size={96}>Insert coin</Big>}

        {/* stage 1 title */}
        {f >= R.stage1 && f < R.lanes && (
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 18 }}>
            <Arc size={34} color={C.green}>Stage 1</Arc>
            <pre style={{ fontFamily: MONO, color: C.white, fontSize: 40, lineHeight: 1.05, margin: "8px 0" }}>{"▄▄▄▄▄▄▄▄▄\n█ "}<span style={{ color: C.turq }}>▄▄▄▄▄</span>{" █\n█ "}<span style={{ color: C.turq }}>█   █</span>{" █\n█ "}<span style={{ color: C.turq }}>▀▀▀▀▀</span>{" █\n▀▀▀▀▀▀▀▀▀"}</pre>
            <Arc size={84} color={C.white} style={{ letterSpacing: "0.04em" }}>omarchy<span style={{ color: C.blue }}>apps</span>.com</Arc>
            <Arc size={30} color={C.cyan}>Every package in the official repo · {FACTS.packages} · {FACTS.categories} categories</Arc>
          </AbsoluteFill>
        )}

        {/* stage 1: three lanes */}
        {lanesOn && (
          <>
            <Lane y={H / 2 - 220} start={R.lanes} len={R.laneLen} names={names.slice(0, 6)} ghost={GHOSTS[0]} />
            <Lane y={H / 2} start={R.lanes + R.laneLen} len={R.laneLen} names={names.slice(6, 12)} ghost={GHOSTS[1]} />
            <Lane y={H / 2 + 220} start={R.lanes + 2 * R.laneLen} len={R.laneLen} names={names.slice(12, 18)} ghost={GHOSTS[2]} />
            <Big at={R.ticker[0]} until={R.ticker[1]} mono upper size={44} color={C.turq} y={400}>Ranked by readers, not ads</Big>
            <Big at={R.ticker[1]} until={R.ticker[2]} mono upper size={44} color={C.turq} y={400}>Guides that get people installing</Big>
            <Big at={R.ticker[2]} until={R.levelUp} mono upper size={44} color={C.turq} y={400}>No trackers. Ever.</Big>
          </>
        )}
        {f >= R.levelUp && f < R.stage2 && (blink(f, 5) ? <AbsoluteFill style={{ background: C.storm }} /> : null)}
        {f >= R.levelUp && f < R.stage2 && <Big at={R.levelUp} mono upper size={128} color={C.orange}>Level up</Big>}
        {f >= R.stage2 && f < R.pellets[0] && <Stack until={R.pellets[0]} mono upper size={64} lines={[{ text: "Stage 2", at: R.stage2, color: C.green }, { text: "Builders", at: R.stage2 + 8 }]} />}

        {/* stage 2: power pellets */}
        {f >= R.pellets[0] && f < R.scores && (
          <>
            {R.pellets.map((at, i) => {
              const x = 420 + i * 540, eaten = f >= at;
              return (
                <div key={at} style={{ position: "absolute", left: x - 22, top: 300, width: 44, height: 44, borderRadius: 22, background: C.white, opacity: eaten ? 0 : blink(f, 8) ? 1 : 0.4, boxShadow: `0 0 30px ${C.white}` }} />
              );
            })}
            {(() => { const i = R.pellets.filter((a) => f >= a - 30).length; const target = 420 + Math.min(2, Math.max(0, i - 1)) * 540; const prev = i <= 1 ? 140 : 420 + (i - 2) * 540; const at = i === 0 ? R.pellets[0] - 30 : R.pellets[i - 1] - 30; const p = Easing.out(Easing.cubic)(clamp01((f - at) / 30)); return <Pac x={prev + (target - prev) * p} y={322} size={72} />; })()}
            {GHOSTS.map((g, i) => <Ghost key={g} x={1300 + i * 140 + 20 * Math.sin(f / 8 + i)} y={322} color={g} scared={f >= R.paid} />)}
            <Big at={R.pellets[0]} until={R.pellets[1]} mono upper size={64} y={120}>Listed the day you ship</Big>
            <Big at={R.pellets[1]} until={R.pellets[2]} mono upper size={64} y={120}>Voted up the Top {FACTS.top}</Big>
            <Big at={R.pellets[2]} until={R.paid} mono upper size={64} y={120}>Found by people who install</Big>
            <Stack until={R.scores} mono upper size={72} lines={[{ text: "Get noticed.", at: R.paid }, { text: "Grow.", at: R.paid + 8 }, { text: "Get paid.", at: R.paid + 16, color: C.orange }]} />
          </>
        )}

        {/* high scores */}
        {f >= R.scores && f < R.dark && (
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 26 }}>
            <Arc size={40} color={C.pink}>High scores</Arc>
            {[["1", "Readers", "growing fast", C.turq],
              ...(st.visitorsLastMonth ? [["2", "Visitors last month", fmt(st.visitorsLastMonth), C.white]] : []),
              ...(st.growthPct ? [["3", "Month over month", `+${st.growthPct}%`, C.white]] : []),
              ...(st.projectionNextMonth ? [["4", "Projected next month", fmt(st.projectionNextMonth), C.white]] : [])]
              .map(([rk, name, val, col], i) => (
                <div key={rk} style={{ display: "grid", gridTemplateColumns: "80px 760px 420px", opacity: f >= R.scores + 10 + i * 14 ? 1 : 0 }}>
                  <Arc size={40} color={C.orange}>{rk}</Arc><Arc size={40}>{name}</Arc><Arc size={40} color={col} style={{ textAlign: "right" }}>{val}</Arc>
                </div>
              ))}
          </AbsoluteFill>
        )}
      </AbsoluteFill>

      {/* stage 3: dark, the tease */}
      <Big at={R.nextWeek} until={R.every} mono upper size={110} color={C.orange} y={-120}>Next week,</Big>
      <Big at={R.nextWeek + 20} until={R.every} mono upper size={58} y={10}>Stage 3 unlocks</Big>
      {f >= R.hints && f < R.every && <Big at={R.hints} mono size={34} color={DIM} y={120}>{hintWord("./guides")}   {hintWord("./support")}   {hintWord("./sponsors")}</Big>}
      {f >= R.player2 && f < R.every && blink(f, 10) && <Big at={R.player2} mono upper size={44} color={C.pink} y={230}>Player 2 wanted</Big>}
      <Stack until={R.endCard} mono upper size={88} lines={[{ text: "Every app.", at: R.every }, { text: "Every maker.", at: R.every + 16 }, { text: "One big upgrade.", at: R.upgrade, color: C.orange }]} />
      <CRT />
    </AbsoluteFill>
  );
};
