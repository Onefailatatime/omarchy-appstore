import { useMemo } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, MONO, SANS } from "./theme";
import { useSiteFonts } from "./fonts";
import { EndCard } from "./EndCard";
import { Big, Stack } from "./Text";
import { Stat } from "./Card";
import { ALL, Card, DIM, LeaderRow, Pkg, SiteBar } from "./ui";
import T from "./timeline.json";
import stats from "./stats.json";
import { FACTS } from "./facts";

const D = T.desktop;
const W = 1920, H = 1080, BAR = 44, GAP = 14;
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
const ease = Easing.out(Easing.cubic);
const prog = (f: number, a: number, len: number) => ease(clamp01((f - a) / len));
const fmt = (n: number) => n.toLocaleString("en-US");
const Cursor: React.FC<{ on: boolean }> = ({ on }) => (on ? <span style={{ display: "inline-block", width: 12, height: 26, background: C.white, verticalAlign: -4 }} /> : null);

/* Waybar: workspaces on the left, clock in the middle, the usual modules on the right. */
const Waybar: React.FC<{ ws: number }> = ({ ws }) => (
  <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: BAR, background: C.night, borderBottom: "1px solid rgba(65,72,104,0.6)", display: "flex", alignItems: "center", padding: "0 18px", fontFamily: MONO, fontSize: 18, color: C.blue }}>
    <div style={{ display: "flex", gap: 6 }}>
      {[1, 2, 3, 4].map((n) => <span key={n} style={{ padding: "2px 10px", borderRadius: 5, background: n === ws ? C.blue : "transparent", color: n === ws ? C.night : DIM, fontWeight: n === ws ? 700 : 400 }}>{n}</span>)}
    </div>
    <div style={{ position: "absolute", left: 0, right: 0, textAlign: "center", color: C.white, pointerEvents: "none" }}>Mon 12 Oct  21:08</div>
    <div style={{ marginLeft: "auto", display: "flex", gap: 22, color: DIM }}><span>wifi</span><span>vol 60%</span><span style={{ color: C.green }}>bat 87%</span></div>
  </div>
);

type Rect = { x: number; y: number; w: number; h: number };
/* Dwindle layout: one window fills, two split left/right, three split the right column. */
function tile(n: number, i: number): Rect {
  const x0 = GAP, y0 = BAR + GAP, w = W - 2 * GAP, h = H - BAR - 2 * GAP;
  if (n === 1) return { x: x0, y: y0, w, h };
  if (n === 2) return i === 0 ? { x: x0, y: y0, w: (w - GAP) / 2, h } : { x: x0 + (w + GAP) / 2, y: y0, w: (w - GAP) / 2, h };
  if (i === 0) return { x: x0, y: y0, w: (w - GAP) / 2, h };
  const rh = (h - GAP) / 2;
  return { x: x0 + (w + GAP) / 2, y: i === 1 ? y0 : y0 + rh + GAP, w: (w - GAP) / 2, h: rh };
}
const cols = (n: number, i: number): Rect => { const x0 = GAP, y0 = BAR + GAP, w = (W - 2 * GAP - (n - 1) * GAP) / n; return { x: x0 + i * (w + GAP), y: y0, w, h: H - BAR - 2 * GAP }; };

/* A Hyprland window: no decorations, a 2px border that goes turquoise with focus, scale-in on open. */
const Win: React.FC<{ r: Rect; openAt: number; focus?: boolean; closeAt?: number; children: React.ReactNode }> = ({ r, openAt, focus = false, closeAt, children }) => {
  const f = useCurrentFrame();
  if (f < openAt || (closeAt !== undefined && f >= closeAt + 12)) return null;
  const o = prog(f, openAt, 12);
  const c = closeAt !== undefined ? 1 - clamp01((f - closeAt) / 12) : 1;
  const s = (0.92 + 0.08 * o) * (0.96 + 0.04 * c);
  return (
    <div style={{ position: "absolute", left: r.x, top: r.y, width: r.w, height: r.h, opacity: o * c, transform: `scale(${s})`, borderRadius: 10, border: `2px solid ${focus ? C.turq : "rgba(65,72,104,0.9)"}`,
      background: C.night, overflow: "hidden", boxSizing: "border-box", boxShadow: focus ? "0 0 0 1px rgba(180,249,248,0.25), 0 20px 60px rgba(0,0,0,0.5)" : "0 20px 60px rgba(0,0,0,0.45)" }}>
      {children}
    </div>
  );
};

/* Notification in the top right, the way mako shows them. */
const Notify: React.FC<{ at: number; until: number; title: string; body: string; accent?: string }> = ({ at, until, title, body, accent = C.blue }) => {
  const f = useCurrentFrame();
  if (f < at || f >= until) return null;
  const p = prog(f, at, 14), out = 1 - clamp01((f - (until - 10)) / 10);
  return (
    <div style={{ position: "absolute", right: 24, top: BAR + 20, width: 560, opacity: p * out, transform: `translateX(${(1 - p) * 80}px)`, background: C.storm, border: `1px solid rgba(65,72,104,0.9)`, borderLeft: `4px solid ${accent}`, borderRadius: 8, padding: "16px 20px", fontFamily: MONO, zIndex: 5 }}>
      <div style={{ color: DIM, fontSize: 15, marginBottom: 6 }}>{title}</div>
      <div style={{ color: C.white, fontSize: 24, lineHeight: 1.3 }}>{body}</div>
    </div>
  );
};

const Term: React.FC<{ size?: number; children: React.ReactNode }> = ({ size = 24, children }) => (
  <div style={{ padding: "22px 26px", fontFamily: MONO, fontSize: size, lineHeight: 1.55, color: C.white, whiteSpace: "pre-wrap" }}>{children}</div>
);
const Label: React.FC<{ children: string }> = ({ children }) => <span style={{ color: DIM }}>{children.padEnd(11)}</span>;

export const Desktop = () => {
  useSiteFonts();
  const f = useCurrentFrame();
  const st = stats as { visitorsLastMonth: number | null; growthPct: number | null; projectionNextMonth: number | null };
  const audio = <Audio src={staticFile("audio/desktop.wav")} />;
  const lone: Pkg = { n: "your-omarchy-app", d: "The thing you built. Pushed to a repo. Waiting.", c: "Developer Tools" };
  const videoHits = useMemo(() => ALL.filter((p) => /video|screen|record|stream|cut/i.test(p.n + " " + p.d)).slice(0, 12), []);
  const star = videoHits.find((p) => p.n === "omacut") ?? videoHits[0];
  if (f >= D.endCard) return <AbsoluteFill style={{ background: C.night }}>{audio}<EndCard from={D.endCard} fade /></AbsoluteFill>;

  const ws = f < D.ws2 ? 1 : f < D.ws3 ? 2 : f < D.ws4 ? 3 : 4;
  const wsStart = [0, 0, D.ws2, D.ws3, D.ws4][ws];
  const slide = (1 - prog(f, wsStart, 14)) * (ws === 1 ? 0 : W);          // workspaces slide in from the right
  const day = Math.min(30, Math.floor(1 + f / 4));
  const typed = "video".slice(0, D.searchKeys.filter((k) => f >= k).length);
  const cmd = "omarchy pkg add " + star.n;
  const cmdTyped = cmd.slice(0, D.cmdKeys.filter((k) => f >= k).length);
  const climb = prog(f, D.climb, 40);

  return (
    <AbsoluteFill style={{ background: C.night }}>
      {audio}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, rgba(36,40,59,0.9), rgba(26,27,38,1) 70%)" }} />
      <Waybar ws={ws} />
      <div style={{ position: "absolute", inset: 0, transform: `translateX(${slide}px)` }}>
        {/* workspace 1: the problem, one terminal */}
        {ws === 1 && (
          <Win r={tile(1, 0)} openAt={0} focus>
            <Term size={30}>
              <span style={{ color: C.green }}>~ $</span> git push origin main<Cursor on={f < 10} />{"\n"}
              {f >= 10 && <><Label>→</Label>github.com/you/{lone.n}   <span style={{ color: C.green }}>done</span>{"\n"}</>}
              {f >= 30 && <><span style={{ color: C.green }}>~ $</span> watch stars{"\n"}</>}
              {f >= 40 && <><Label>stars</Label>{day >= 30 ? 1 : 0}        <span style={{ color: DIM }}>day {day}</span>{"\n"}</>}
              {f >= 100 && <>{"\n"}<span style={{ color: DIM }}># hoping someone finds your repo is not a plan</span></>}
            </Term>
          </Win>
        )}
        {/* workspace 2: the store, three windows */}
        {ws === 2 && (
          <>
            <Win r={tile(3, 0)} openAt={D.open[0]} focus={f >= D.focusBrowser && f < D.focusTerm}>
              <div style={{ height: 40, background: C.storm, display: "flex", alignItems: "center", padding: "0 16px", gap: 12, fontFamily: MONO, fontSize: 16, color: DIM }}>
                <span>‹ ›</span><span style={{ flex: 1, background: C.night, borderRadius: 6, padding: "4px 12px", color: C.white }}>omarchyapps.com</span>
              </div>
              <SiteBar size={15} />
              <div style={{ padding: "14px 18px 0" }}>
                <div style={{ height: 44, border: `2px solid ${f >= D.focusBrowser && f < D.filtered + 20 ? C.turq : "rgba(65,72,104,0.8)"}`, borderRadius: 7, background: C.storm, display: "flex", alignItems: "center", padding: "0 14px", fontFamily: MONO, fontSize: 18, color: typed ? C.white : DIM }}>
                  {typed || "Search packages"}<Cursor on={f >= D.focusBrowser && f < D.filtered && Math.floor(f / 12) % 2 === 0} />
                </div>
                {f >= D.filtered && <div style={{ fontFamily: MONO, fontSize: 14, color: DIM, marginTop: 8 }}>{videoHits.length} results for "video"</div>}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10, padding: "12px 18px" }}>
                {(f >= D.filtered ? videoHits : ALL.slice(0, 15)).slice(0, 15).map((p, i) => (
                  <div key={p.n} style={{ opacity: prog(f, (f >= D.filtered ? D.filtered : D.open[0] + 10) + i * 2, 12), transform: "scale(0.86)", transformOrigin: "top left", width: "116%" }}>
                    <Card p={p} hi={f >= D.filtered && f < D.focusTerm} />
                  </div>
                ))}
              </div>
            </Win>
            <Win r={tile(3, 1)} openAt={D.open[1]} focus={f >= D.focusTerm && f < D.focusLeader}>
              <Term>
                <span style={{ color: C.green }}>~ $</span> {f >= D.focusTerm ? cmdTyped : ""}<Cursor on={f >= D.focusTerm && f < D.installed && Math.floor(f / 12) % 2 === 0} />{"\n"}
                {f >= D.cmdKeys[D.cmdKeys.length - 1] + 8 && <><Label>resolving</Label>{star.n}  <span style={{ color: DIM }}>{star.s}</span>{"\n"}<Label>installing</Label><span style={{ color: C.blue }}>{"█".repeat(Math.max(0, Math.min(14, Math.floor((f - D.cmdKeys[D.cmdKeys.length - 1] - 8) / 2))))}</span>{"\n"}</>}
                {f >= D.installed && <><span style={{ color: C.green }}>✓</span> installed {star.n}{"\n"}<span style={{ color: C.green }}>~ $</span> <Cursor on={Math.floor(f / 12) % 2 === 0} /></>}
              </Term>
            </Win>
            <Win r={tile(3, 2)} openAt={D.open[2]} focus={f >= D.focusLeader}>
              <div style={{ padding: "18px 22px", fontFamily: SANS, fontWeight: 800, fontSize: 26, color: C.white }}>The Top {FACTS.top} <span style={{ fontFamily: MONO, fontWeight: 400, fontSize: 15, color: DIM, marginLeft: 10 }}>ranked by upvotes</span></div>
              <div style={{ padding: "0 22px", position: "relative", height: 400 }}>
                {ALL.slice(0, 7).map((p, i) => {
                  const ours = i === 6, dest = 1;
                  let pos = i; if (ours) pos = i + (dest - i) * climb; else if (i >= dest && i < 6) pos = i + climb;
                  return <div key={p.n} style={{ position: "absolute", left: 22, right: 22, top: pos * 54 }}><LeaderRow p={ours ? { ...lone, c: p.c } : p} rank={Math.round(pos) + 1} hi={ours && climb > 0} pulse={ours && f >= D.climb && Math.floor(f / 6) % 2 === 0} size={19} /></div>;
                })}
              </div>
            </Win>
          </>
        )}
        {/* workspace 3: builders, three columns */}
        {ws === 3 && (
          <>
            <Win r={cols(3, 0)} openAt={D.panels[0]} focus={f < D.panels[1]}>
              <div style={{ padding: 26, fontFamily: SANS, height: "100%", display: "flex", flexDirection: "column", justifyContent: "center", boxSizing: "border-box" }}>
                <div style={{ fontWeight: 800, fontSize: 36, color: C.white, lineHeight: 1.1, letterSpacing: "-0.02em", marginBottom: 24 }}>Listed the day you ship.</div>
                <Card p={lone} isNew />
                <div style={{ marginTop: 22, fontFamily: MONO, color: DIM, fontSize: 18, lineHeight: 1.5 }}>Synced from the official repo. No form, no gatekeeper.</div>
              </div>
            </Win>
            <Win r={cols(3, 1)} openAt={D.panels[1]} focus={f >= D.panels[1] && f < D.panels[2]}>
              <div style={{ padding: 26, fontFamily: SANS, height: "100%", display: "flex", flexDirection: "column", justifyContent: "center", boxSizing: "border-box" }}>
                <div style={{ fontWeight: 800, fontSize: 36, color: C.white, lineHeight: 1.1, letterSpacing: "-0.02em", marginBottom: 24 }}>Voted up the Top {FACTS.top}.</div>
                <div style={{ display: "grid", gap: 10 }}>
                  {[ALL[5], ALL[9], lone].map((p, j) => <LeaderRow key={p.n} p={p} rank={3 - j} hi={j === 2 && f >= D.panels[1] + 30} pulse={j === 2 && f >= D.panels[1] + 30 && Math.floor(f / 6) % 2 === 0} />)}
                </div>
                <div style={{ marginTop: 22, fontFamily: MONO, color: DIM, fontSize: 18, lineHeight: 1.5 }}>Readers vote. Rank comes from them and nobody else.</div>
              </div>
            </Win>
            <Win r={cols(3, 2)} openAt={D.panels[2]} focus={f >= D.panels[2]}>
              <div style={{ padding: 26, fontFamily: SANS, height: "100%", display: "flex", flexDirection: "column", justifyContent: "center", boxSizing: "border-box" }}>
                <div style={{ fontWeight: 800, fontSize: 36, color: C.white, lineHeight: 1.1, letterSpacing: "-0.02em", marginBottom: 24 }}>Found by people who install.</div>
                <Term size={22}><span style={{ color: C.green }}>~ $</span> omarchy pkg add {lone.n}{"\n"}<Label>installing</Label><span style={{ color: C.blue }}>{"█".repeat(Math.max(0, Math.min(12, Math.floor((f - D.panels[2]) / 4))))}</span>{"\n"}{f >= D.panels[2] + 50 && <><span style={{ color: C.green }}>✓</span> done</>}</Term>
                <div style={{ marginTop: 10, fontFamily: MONO, color: DIM, fontSize: 18, lineHeight: 1.5 }}>Readers come to install, not to browse.</div>
              </div>
            </Win>
          </>
        )}
        {/* workspace 4: everything closes, one notification */}
        {ws === 4 && (
          <Notify at={D.ws4 + 16} until={D.every} title="omarchyapps · update" body={`omarchyapps 1.x → 2.0 · lands next week`} accent={C.orange} />
        )}
      </div>

      {/* statements over the desktop */}
      {ws === 1 && (
        <>
          <Big at={D.hoped[0]} until={D.hoped[1]} size={64} color={C.blue} y={260}>You built it.</Big>
          <Big at={D.hoped[1]} until={D.hoped[2]} size={64} color={C.blue} y={260}>You pushed it to a repo.</Big>
          <Big at={D.hoped[2]} until={D.hoping} size={64} color={C.blue} y={260}>Then you hoped someone would find it.</Big>
          {f >= D.hoping && <AbsoluteFill style={{ background: "rgba(26,27,38,0.86)", opacity: prog(f, D.hoping, 10) }} />}
          <Big at={D.hoping} until={D.ws2} size={128}>Hoping is not a plan.</Big>
        </>
      )}
      {ws === 2 && (
        <>
          <Notify at={D.facts} until={D.focusBrowser} title="omarchyapps.com" body={`${FACTS.packages} packages · ${FACTS.categories} categories · synced from pkgs.omarchy.org`} />
          <Notify at={D.notes[0]} until={D.notes[1]} title="omarchyapps.com" body="Every package in the official repo. Searchable. One command away." accent={C.turq} />
          <Notify at={D.notes[1]} until={D.notes[2]} title="omarchyapps.com" body="Guides that get people installing. No trackers. Ever." accent={C.turq} />
          <Notify at={D.notes[2]} until={D.ws3} title="omarchyapps.com" body="Ranked by readers. Votes come from them and nobody else." accent={C.turq} />
        </>
      )}
      {ws === 3 && (
        <>
          {f >= D.grow && <AbsoluteFill style={{ background: "rgba(26,27,38,0.86)", opacity: prog(f, D.grow, 12) }} />}
          <Stack until={D.stats} size={118} lines={[{ text: "Get noticed. Grow.", at: D.grow }, { text: "Get paid.", at: D.grow + 14, color: C.blue }]} />
          <Big at={D.stats} until={D.ws4} size={96} y={st.visitorsLastMonth ? -200 : 0}>Readers are growing fast.</Big>
          {st.visitorsLastMonth && f >= D.stats ? (
            <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
              <div style={{ display: "flex", gap: 140, marginTop: 120 }}>
                <Stat from={D.stats} at={14} value={fmt(st.visitorsLastMonth)} label="visitors last month" />
                {st.growthPct ? <Stat from={D.stats} at={28} value={`+${st.growthPct}%`} label="month over month" /> : null}
                {st.projectionNextMonth ? <Stat from={D.stats} at={42} value={fmt(st.projectionNextMonth)} label="projected next month" /> : null}
              </div>
            </AbsoluteFill>
          ) : null}
        </>
      )}
      {ws === 4 && (
        <>
          <Big at={D.nextWeek} until={D.every} size={132} color={C.orange} y={-70}>Next week,</Big>
          <Big at={D.biggest} until={D.every} size={84} y={70}>the store gets its biggest upgrade yet.</Big>
          <Big at={D.hints} until={D.every} size={34} mono color={DIM} y={200}>./guides   ./support</Big>
          <Stack until={D.endCard} size={118} lines={[{ text: "Every app.", at: D.every }, { text: "Every maker.", at: D.every + 16 }, { text: "One big upgrade.", at: D.upgrade, color: C.blue }]} />
        </>
      )}
    </AbsoluteFill>
  );
};
