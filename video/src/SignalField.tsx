import { useLayoutEffect, useMemo, useRef } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, MONO, SANS } from "./theme";
import { useSiteFonts } from "./fonts";
import { EndCard } from "./EndCard";
import { Stat } from "./Card";
import { Big, Stack } from "./Text";
import T from "./timeline.json";
import pkgs from "./packages.json";
import stats from "./stats.json";
import { FACTS } from "./facts";

const S = T.signal;
const W = 1920, H = 1080, CELL = 14, GAP = 3;

type Tone = [number, number, number, number];
const TONES: [Tone, number][] = [
  [[65, 72, 104, 0.55], 0.4], [[65, 72, 104, 0.55], 0.12], [[122, 162, 247, 0.38], 0.16], [[125, 207, 255, 0.45], 0.08],
  [[187, 154, 247, 0.4], 0.09], [[157, 124, 216, 0.42], 0.07], [[247, 118, 142, 0.38], 0.06], [[180, 249, 248, 0.35], 0.02],
];
const WHITE: Tone = [192, 202, 245, 1], TURQ: Tone = [180, 249, 248, 1];

function rng(seed: number) { return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
const smooth = (v: number) => v * v * (3 - 2 * v);
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
const ramp = (f: number, a: number, b: number) => smooth(clamp01((f - a) / (b - a)));

/* The ASCII box logo from the homepage, rasterised to half-cells: 9 wide, 10 tall. */
const LOGO: { x: number; y: number; inner: boolean }[] = (() => {
  const out: { x: number; y: number; inner: boolean }[] = [];
  for (let x = 0; x < 9; x++) out.push({ x, y: 1, inner: false }, { x, y: 8, inner: false });
  for (let y = 2; y <= 7; y++) out.push({ x: 0, y, inner: false }, { x: 8, y, inner: false });
  for (let x = 2; x <= 6; x++) out.push({ x, y: 3, inner: true }, { x, y: 6, inner: true });
  out.push({ x: 2, y: 4, inner: true }, { x: 6, y: 4, inner: true }, { x: 2, y: 5, inner: true }, { x: 6, y: 5, inner: true });
  return out;
})();
const SUB = 4;

type P = { sx: number; sy: number; tx: number; ty: number; tone: Tone; phase: number; period: number; birth: number; logo: boolean; inner: boolean; ang: number };

function buildParticles(): P[] {
  const r = rng(20261011), out: P[] = [];
  const cols = Math.ceil(W / CELL), rows = Math.ceil(H / CELL);
  const lw = 9 * SUB * CELL, lh = 10 * SUB * CELL, ox = (W - lw) / 2, oy = (H - lh) / 2 - 90;
  const targets: { x: number; y: number; inner: boolean }[] = [];
  for (const c of LOGO) for (let i = 0; i < SUB; i++) for (let j = 0; j < SUB; j++)
    targets.push({ x: ox + (c.x * SUB + i) * CELL, y: oy + (c.y * SUB + j) * CELL, inner: c.inner });
  let ti = 0;
  for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) {
    const dx = (x - cols / 2) / cols * 2, dy = (y - rows * 0.5) / rows * 2.2, d = Math.sqrt(dx * dx + dy * dy);
    const p = Math.max(0, 0.5 - d * 0.42) * (0.65 + r() * 0.7);
    if (r() > p) continue;
    let acc = 0, tone = TONES[0][0]; const pick = r();
    for (const [t, w] of TONES) { acc += w; if (pick <= acc) { tone = t; break; } }
    const logo = ti < targets.length && r() < 0.62;
    const tg = logo ? targets[ti++] : { x: 0, y: 0, inner: false };
    out.push({ sx: x * CELL, sy: y * CELL, tx: tg.x, ty: tg.y, tone, phase: r() * 6.283, period: 60 + r() * 140,
      birth: r() * 90, logo, inner: tg.inner, ang: Math.atan2(tg.y - H / 2, tg.x - W / 2) });
  }
  while (ti < targets.length) {
    const tg = targets[ti++];
    out.push({ sx: r() * W, sy: r() * H, tx: tg.x, ty: tg.y, tone: TONES[2][0], phase: r() * 6.283, period: 90, birth: r() * 90, logo: true, inner: tg.inner, ang: Math.atan2(tg.y - H / 2, tg.x - W / 2) });
  }
  return out;
}

/* Ambient brightness of the field through the whole film. */
function ambient(f: number) {
  if (f < S.lone.t3) return 0;
  if (f < S.ignite) return 0.18 * ramp(f, S.lone.t3, S.lone.t3 + 40);
  if (f < S.pullStart) return 0.18 + 0.82 * ramp(f, S.ignite, S.ignite + 70);
  if (f < S.burstStart) return 1;
  if (f < S.dim) return 0.5;
  if (f < S.every) return 0.5 - 0.44 * ramp(f, S.dim, S.dim + 50);
  return 0.06 + 0.44 * ramp(f, S.every, S.every + 40);
}

const Field: React.FC = () => {
  const ref = useRef<HTMLCanvasElement>(null);
  const f = useCurrentFrame();
  const parts = useMemo(buildParticles, []);
  useLayoutEffect(() => {
    const ctx = ref.current?.getContext("2d"); if (!ctx) return;
    ctx.clearRect(0, 0, W, H);
    const amb = ambient(f);
    const push = 1 + 0.16 * ramp(f, S.ignite, S.lockAt);
    const pull = ramp(f, S.pullStart, S.lockAt - 10);
    const burst = clamp01((f - S.burstStart) / 50);
    const bloom = f >= S.lockAt && f < S.burstStart;
    const logoPhase = f >= S.pullStart && f < S.burstStart + 60;
    for (const p of parts) {
      let x = p.sx, y = p.sy, a: number, col: Tone = p.tone;
      const breathe = smooth(smooth(0.5 + 0.5 * Math.sin((f / p.period) * 6.283 + p.phase)));
      const born = clamp01((f - S.lone.t3 - p.birth) / 40);
      if (p.logo && logoPhase) {
        x = p.sx + (p.tx - p.sx) * pull; y = p.sy + (p.ty - p.sy) * pull;
        col = p.inner ? TURQ : WHITE;
        a = p.tone[3] * breathe * (1 - pull) + pull * 0.95;
        if (f >= S.burstStart) { x += Math.cos(p.ang) * burst * burst * 1400; y += Math.sin(p.ang) * burst * burst * 1400; a *= 1 - burst; }
        x = W / 2 + (x - W / 2) * push; y = H / 2 + (y - H / 2) * push;
      } else {
        const fadeOut = logoPhase && !p.logo ? 1 - ramp(f, S.pullStart, S.pullStart + 60) : 1;
        a = p.tone[3] * breathe * born * amb * fadeOut;
        if (f < S.burstStart + 60) { x = W / 2 + (x - W / 2) * push; y = H / 2 + (y - H / 2) * push; }
      }
      if (a < 0.005) continue;
      ctx.fillStyle = `rgba(${col[0]},${col[1]},${col[2]},${a})`;
      if (bloom && p.logo) { ctx.shadowColor = `rgba(${col[0]},${col[1]},${col[2]},0.9)`; ctx.shadowBlur = 18 * ramp(f, S.lockAt, S.lockAt + 20); } else ctx.shadowBlur = 0;
      ctx.fillRect(x, y, CELL - GAP, CELL - GAP);
    }
    // the lone pixel: one app, alone in the dark
    if (f < S.lone.end + 40) {
      const a = (0.5 + 0.5 * smooth(0.5 + 0.5 * Math.sin(f / 9))) * (1 - ramp(f, S.lone.end, S.lone.end + 40)) * ramp(f, 0, 12);
      ctx.shadowBlur = 0; ctx.fillStyle = `rgba(122,162,247,${a})`;
      ctx.fillRect(W / 2 - 8, H / 2 - 8 - 90, 16, 16);
    }
  }, [f, parts]);
  return <canvas ref={ref} width={W} height={H} style={{ position: "absolute", inset: 0 }} />;
};

const CAT_COLORS = [C.pink, C.magenta, C.cyan, C.green, C.purple];
const Cards: React.FC = () => {
  const f = useCurrentFrame();
  const cards = useMemo(() => {
    const r = rng(77);
    return pkgs.slice(0, 36).map((name, i) => ({ name, ang: r() * 6.283, start: S.burstStart + 6 + i * 3.4 + r() * 6, hi: r() < 0.22, cat: CAT_COLORS[i % 5], ry: (r() - 0.5) * 30 }));
  }, []);
  return (
    <AbsoluteFill style={{ perspective: 1400 }}>
      {cards.map((c) => {
        const p = (f - c.start) / 64; if (p < 0 || p > 1) return null;
        const e = Easing.bezier(0.3, 0, 0.9, 0.6)(p);
        const dist = e * 1500, sc = 0.25 + 1.9 * e, op = Math.min(p * 8, 1) * (1 - Math.pow(p, 3));
        return (
          <div key={c.name} style={{ position: "absolute", left: W / 2, top: H / 2, opacity: op,
            transform: `translate(-50%,-50%) translate(${Math.cos(c.ang) * dist}px, ${Math.sin(c.ang) * dist * 0.62}px) rotateY(${c.ry}deg) scale(${sc})`,
            background: C.storm, border: `2px solid ${c.hi ? C.turq : C.tblack}`, borderRadius: 8, padding: "16px 22px", fontFamily: MONO, fontSize: 28, color: c.hi ? C.turq : C.white, whiteSpace: "nowrap",
            boxShadow: c.hi ? "0 0 40px rgba(180,249,248,0.35)" : "none" }}>
            <span style={{ display: "inline-block", width: 12, height: 12, borderRadius: 6, background: c.cat, marginRight: 12, verticalAlign: 2 }} />{c.name}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const fmt = (n: number) => n.toLocaleString("en-US");

export const SignalField = () => {
  useSiteFonts();
  const f = useCurrentFrame();
  const st = stats as { visitorsLastMonth: number | null; growthPct: number | null; projectionNextMonth: number | null };
  const d = S.different, b = S.builderLines;
  return (
    <AbsoluteFill style={{ background: C.night }}>
      <Audio src={staticFile("audio/signal.wav")} />
      <Field />
      {/* act 1: alone */}
      <Big at={S.lone.t1} until={S.lone.t2} size={76} color={C.blue} y={120}>You built something for Omarchy.</Big>
      <Big at={S.lone.t2} until={S.lone.t3} size={76} color={C.blue} y={120}>You pushed it to a repo.</Big>
      <Big at={S.lone.t3} until={S.hoping} size={76} color={C.blue} y={120}>Then you hoped someone would find it.</Big>
      <Big at={S.hoping} until={S.pullStart} size={132}>Hoping is not a plan.</Big>
      {/* act 2: the store */}
      <Big at={S.logoCopy} until={S.burstStart} size={58} color={C.white} y={330}>Every package in the official Omarchy repo. One place.</Big>
      <Big at={S.logoCopy + 24} until={S.burstStart} size={38} mono color={C.cyan} y={410}>{FACTS.packages} packages · {FACTS.categories} categories · omarchy pkg add &lt;name&gt;</Big>
      {f >= S.burstStart && f < S.burstStart + 140 && <Cards />}
      <Big at={d[0]} until={d[1]} size={108}>Ranked by readers.</Big>
      <Big at={d[1]} until={d[2]} size={108}>Guides that get people installing.</Big>
      <Big at={d[2]} until={S.builders} size={108}>No trackers. Ever.</Big>
      {/* act 3: builders */}
      <Big at={b[0]} until={b[1]} size={104}>Get listed the day you ship.</Big>
      <Big at={b[1]} until={b[2]} size={104}>Get voted up the Top {FACTS.top}.</Big>
      <Big at={b[2]} until={S.grow} size={104}>Get found by people who install.</Big>
      <Stack until={S.stats} size={118} lines={[{ text: "Grow.", at: S.grow }, { text: "Get noticed.", at: S.grow + 14 }, { text: "Get paid.", at: S.grow + 28, color: C.blue }]} />
      {/* act 4: traffic */}
      <Big at={S.stats} until={S.dim} size={96} y={st.visitorsLastMonth ? -200 : 0}>Readers are growing fast.</Big>
      {st.visitorsLastMonth && f >= S.stats && f < S.dim ? (
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <div style={{ display: "flex", gap: 140, marginTop: 120 }}>
            <Stat from={S.stats} at={14} value={fmt(st.visitorsLastMonth)} label="visitors last month" />
            {st.growthPct ? <Stat from={S.stats} at={28} value={`+${st.growthPct}%`} label="month over month" /> : null}
            {st.projectionNextMonth ? <Stat from={S.stats} at={42} value={fmt(st.projectionNextMonth)} label="projected next month" /> : null}
          </div>
        </AbsoluteFill>
      ) : null}
      {/* act 5: the tease */}
      <Big at={S.nextWeek} until={S.every} size={132} color={C.orange} y={-70}>Next week,</Big>
      <Big at={S.biggest} until={S.every} size={88} y={70}>the store gets its biggest upgrade yet.</Big>
      <Big at={S.hints} until={S.every} size={34} mono color={"rgba(122,162,247,0.62)"} y={200}>./guides   ./support</Big>
      <Stack until={S.endCard} size={118} lines={[{ text: "Every app.", at: S.every }, { text: "Every maker.", at: S.every + 16 }, { text: "One big upgrade.", at: S.upgrade, color: C.blue }]} />
      {f >= S.endCard && <EndCard from={S.endCard} fade />}
    </AbsoluteFill>
  );
};
