import { useMemo } from "react";
import { AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, MONO, SANS } from "./theme";
import { useSiteFonts } from "./fonts";
import { EndCard } from "./EndCard";
import { Big, Stack } from "./Text";
import { Stat } from "./Card";
import { CAT } from "./catcolors";
import T from "./timeline.json";
import cat from "./catalogue.json";
import stats from "./stats.json";
import { FACTS } from "./facts";

const K = T.catalogue;
const W = 1920, H = 1080;
const DIM = "rgba(122,162,247,0.62)";
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
const ease = Easing.out(Easing.cubic);
const prog = (f: number, a: number, len: number) => ease(clamp01((f - a) / len));
function rng(seed: number) { return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }

type Pkg = { n: string; d: string; c: string };
const ALL = cat as Pkg[];
const COLS = 6, CW = 286, CH = 150, GX = 16, GY = 16, GRID_X = (W - (COLS * CW + (COLS - 1) * GX)) / 2, GRID_Y = 150;
const cell = (i: number) => ({ x: GRID_X + (i % COLS) * (CW + GX), y: GRID_Y + Math.floor(i / COLS) * (CH + GY) });

/* A catalogue card in the site's own styling: storm fill, 1px border, category dot, green version. */
const Card: React.FC<{ p: Pkg; x: number; y: number; w?: number; scale?: number; opacity?: number; hi?: boolean; isNew?: boolean; big?: boolean }> =
  ({ p, x, y, w = CW, scale = 1, opacity = 1, hi = false, isNew = false, big = false }) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, minHeight: CH, opacity, transform: `scale(${scale})`, transformOrigin: "top left",
    background: C.storm, border: `1px solid ${hi ? CAT[p.c] : "rgba(65,72,104,0.8)"}`, borderTop: isNew ? `2px solid ${C.orange}` : undefined, borderRadius: 7, padding: big ? "22px 26px" : "14px 16px",
    fontFamily: MONO, fontSize: big ? 26 : 17, color: C.blue, display: "flex", flexDirection: "column", gap: big ? 12 : 7 }}>
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 10 }}>
      <b style={{ color: hi ? C.turq : C.white, fontSize: big ? 34 : 18, overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis" }}>{p.n}</b>
      {isNew ? <span style={{ color: C.orange, fontSize: big ? 20 : 13, whiteSpace: "nowrap" }}>new</span> : <span style={{ color: C.green, fontSize: big ? 20 : 13, opacity: 0.9 }}>1.0.0</span>}
    </div>
    <div style={{ color: "rgba(122,162,247,0.85)", lineHeight: 1.4, overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" }}>{p.d}</div>
    <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: big ? 20 : 13, color: DIM }}>
      <span style={{ width: big ? 12 : 8, height: big ? 12 : 8, borderRadius: 6, background: CAT[p.c] ?? C.tblack }} />{p.c}
    </div>
  </div>
);

const Chrome: React.FC<{ at: number; y?: number }> = ({ at, y = 0 }) => {
  const f = useCurrentFrame();
  const p = prog(f, at, 20);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, height: 84, borderBottom: "1px solid rgba(65,72,104,0.8)", background: C.night, transform: `translateY(${(1 - p) * -90}px)`,
      display: "flex", alignItems: "center", padding: "0 120px", gap: 40, fontFamily: MONO, fontSize: 22, color: C.blue }}>
      <b style={{ color: C.white, fontSize: 26 }}>Omarchy Apps</b>
      {["Apps", "Top apps", "Guides", "Develop", "Advertise"].map((n) => <span key={n}>{n}</span>)}
      <span style={{ marginLeft: "auto", border: `1px solid ${C.blue}`, borderRadius: 6, padding: "6px 16px", color: C.white }}>Sponsor</span>
    </div>
  );
};

const Search: React.FC<{ typed: string; focus: boolean }> = ({ typed, focus }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: W / 2 - 420, top: 110, width: 840, height: 64, border: `2px solid ${focus ? C.turq : "rgba(65,72,104,0.8)"}`, borderRadius: 8, background: C.storm,
      display: "flex", alignItems: "center", padding: "0 22px", fontFamily: MONO, fontSize: 26, color: typed ? C.white : DIM, boxShadow: focus ? "0 0 0 4px rgba(180,249,248,0.15)" : "none" }}>
      {typed || "Search packages"}{focus && Math.floor(f / 14) % 2 === 0 && <span style={{ display: "inline-block", width: 14, height: 30, background: C.white, marginLeft: 4 }} />}
    </div>
  );
};

const fmt = (n: number) => n.toLocaleString("en-US");

export const Catalogue = () => {
  useSiteFonts();
  const f = useCurrentFrame();
  const st = stats as { visitorsLastMonth: number | null; growthPct: number | null; projectionNextMonth: number | null };
  const audio = <Audio src={staticFile("audio/catalogue.wav")} />;
  const scatter = useMemo(() => { const r = rng(99); return ALL.map(() => ({ dx: (r() - 0.5) * 2600, dy: (r() - 0.5) * 2000, delay: r() * 60 })); }, []);
  const lone: Pkg = { n: "your-omarchy-app", d: "The thing you built. Pushed to a repo. Waiting.", c: "Developer Tools" };
  const videoHits = ALL.filter((p) => /video|screen|record|stream|cut/i.test(p.n + " " + p.d)).slice(0, 12);
  const star = videoHits.find((p) => p.n === "omacut") ?? videoHits[0];

  if (f >= K.endCard) return <AbsoluteFill style={{ background: C.night }}>{audio}<EndCard from={K.endCard} fade /></AbsoluteFill>;

  // ---- act 1: the lone card
  if (f < K.assemble) {
    const px = W / 2 - CW / 2, py = H / 2 - 60;
    return (
      <AbsoluteFill style={{ background: C.night }}>{audio}
        <Card p={lone} x={px} y={py} opacity={1 - clamp01((f - K.hoping) / 20)} />
        <div style={{ position: "absolute", left: px, top: py + CH + 14, fontFamily: MONO, fontSize: 17, color: DIM, opacity: 1 - clamp01((f - K.hoping) / 20) }}>stars 1 · day {Math.min(30, Math.floor(1 + f / 4))}</div>
        <Big at={K.hoped[0]} until={K.hoped[1]} size={64} color={C.blue} y={-260}>You built it.</Big>
        <Big at={K.hoped[1]} until={K.hoped[2]} size={64} color={C.blue} y={-260}>You pushed it to a repo.</Big>
        <Big at={K.hoped[2]} until={K.hoping} size={64} color={C.blue} y={-260}>Then you hoped someone would find it.</Big>
        <Big at={K.hoping} until={K.assemble} size={128}>Hoping is not a plan.</Big>
      </AbsoluteFill>
    );
  }

  // ---- act 2: the catalogue assembles and scrolls
  if (f < K.search) {
    const scroll = -prog(f, K.scroll, K.search - K.scroll) * 2600;
    const shown = Math.min(ALL.length, Math.floor(interpolate(f, [K.counters, K.counters + 50], [0, FACTS.packages], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
    return (
      <AbsoluteFill style={{ background: C.night }}>{audio}
        <div style={{ position: "absolute", inset: 0, transform: `translateY(${scroll}px)` }}>
          {ALL.map((p, i) => {
            const t = prog(f, K.assemble + scatter[i].delay, 40); const c = cell(i);
            return <Card key={p.n} p={p} x={c.x + scatter[i].dx * (1 - t)} y={c.y + 120 + scatter[i].dy * (1 - t)} opacity={t} />;
          })}
        </div>
        <Chrome at={K.chrome} />
        {f >= K.counters && (
          <div style={{ position: "absolute", left: 0, right: 0, bottom: 70, textAlign: "center", fontFamily: MONO, fontSize: 40, color: C.white, background: "linear-gradient(transparent, rgba(26,27,38,0.95) 30%)", padding: "60px 0 0" }}>
            <b style={{ color: C.cyan }}>{shown}</b> packages · <b style={{ color: C.cyan }}>{FACTS.categories}</b> categories · <span style={{ color: DIM }}>synced from pkgs.omarchy.org</span>
          </div>
        )}
      </AbsoluteFill>
    );
  }

  // ---- act 3: search, filter, one command
  if (f < K.leaderboard) {
    const typed = "video".slice(0, K.searchKeys.filter((k) => f >= k).length);
    const filtered = f >= K.filtered;
    const zoom = prog(f, K.zoom, 30);
    const cmd = "omarchy pkg add " + star.n;
    const cmdTyped = cmd.slice(0, K.cmdKeys.filter((k) => f >= k).length);
    return (
      <AbsoluteFill style={{ background: C.night }}>{audio}
        <Chrome at={0} />
        <Search typed={typed} focus={f < K.zoom} />
        {ALL.slice(0, 24).map((p, i) => {
          const hit = videoHits.includes(p); const c = cell(i); const j = videoHits.indexOf(p);
          const to = hit ? cell(j) : c; const t = filtered ? prog(f, K.filtered, 24) : 0;
          const x = c.x + (to.x - c.x) * t, y = c.y + 60 + (to.y - c.y) * t;
          const op = hit ? 1 - zoom : 1 - t;
          return <Card key={p.n} p={p} x={x} y={y} opacity={op} hi={hit && filtered && f < K.zoom} />;
        })}
        {videoHits.slice(4).map((p, j) => { const c = cell(j + 4); const t = filtered ? prog(f, K.filtered, 24) : 0; return <Card key={p.n} p={p} x={c.x} y={c.y + 60} opacity={t * (1 - zoom)} hi={f < K.zoom} />; })}
        {zoom > 0 && (
          <>
            <Card p={star} x={W / 2 - 330} y={H / 2 - 230} w={660} big scale={0.8 + 0.2 * zoom} opacity={zoom} hi />
            <div style={{ position: "absolute", left: W / 2 - 330, top: H / 2 + 20, width: 660, opacity: zoom, fontFamily: MONO, fontSize: 28, display: "flex", alignItems: "center", gap: 16,
              background: C.night, border: "1px solid rgba(65,72,104,0.8)", borderRadius: 7, padding: "16px 20px" }}>
              <span style={{ color: C.green }}>$</span><span style={{ color: C.white, flex: 1 }}>{cmdTyped}{f < K.copied && Math.floor(f / 12) % 2 === 0 && <span style={{ display: "inline-block", width: 14, height: 30, background: C.white, verticalAlign: -4 }} />}</span>
              <span style={{ color: f >= K.copied ? C.night : C.blue, background: f >= K.copied ? C.turq : "transparent", border: `1px solid ${f >= K.copied ? C.turq : C.blue}`, borderRadius: 6, padding: "6px 14px", fontSize: 20 }}>{f >= K.copied ? "copied" : "copy"}</span>
            </div>
            <Big at={K.oneCommand} until={K.leaderboard} size={72} y={300}>One command away.</Big>
          </>
        )}
        {f >= K.filtered && f < K.zoom && <div style={{ position: "absolute", left: GRID_X, top: 192, fontFamily: MONO, fontSize: 20, color: DIM }}>{videoHits.length} results for "video"</div>}
      </AbsoluteFill>
    );
  }

  // ---- act 4: the leaderboard
  if (f < K.builders) {
    const rows = ALL.slice(0, 10);
    const climb = prog(f, K.climb, 40);
    const ours = 7, dest = 1;
    return (
      <AbsoluteFill style={{ background: C.night }}>{audio}
        <Chrome at={0} />
        <div style={{ position: "absolute", left: W / 2 - 520, top: 150, width: 1040 }}>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: C.white, marginBottom: 6 }}>The Top {FACTS.top}</div>
          <div style={{ fontFamily: MONO, fontSize: 20, color: DIM, marginBottom: 22 }}>Ranked by upvotes</div>
          {rows.map((p, i) => {
            const isOurs = i === ours;
            let pos = i; if (isOurs) pos = i + (dest - i) * climb; else if (i >= dest && i < ours) pos = i + climb;
            const t = prog(f, K.leaderboard + i * 4, 18);
            return (
              <div key={p.n} style={{ position: "absolute", left: 0, right: 0, top: 80 + pos * 64, height: 56, display: "flex", alignItems: "center", gap: 20, padding: "0 18px", opacity: t, transform: `translateX(${(1 - t) * 40}px)`,
                background: isOurs && climb > 0 ? "rgba(65,72,104,0.28)" : "transparent", border: `1px solid ${isOurs && climb > 0 ? CAT[p.c] : "rgba(65,72,104,0.5)"}`, borderRadius: 7, fontFamily: MONO, fontSize: 24 }}>
                <span style={{ color: DIM, width: 40 }}>{String(Math.round(pos) + 1).padStart(2, "0")}</span>
                <span style={{ width: 10, height: 10, borderRadius: 5, background: CAT[p.c] }} />
                <b style={{ color: isOurs && climb > 0 ? C.turq : C.white, flex: 1 }}>{p.n}</b>
                <span style={{ color: DIM, fontSize: 18 }}>{p.c}</span>
                <span style={{ color: isOurs && f >= K.climb && Math.floor(f / 6) % 2 === 0 ? C.turq : C.blue, border: "1px solid rgba(65,72,104,0.8)", borderRadius: 6, padding: "4px 12px" }}>▲</span>
              </div>
            );
          })}
        </div>
        <Big at={K.ranked} until={K.builders} size={88} y={400}>Ranked by readers, not ads.</Big>
      </AbsoluteFill>
    );
  }

  // ---- act 5: builders
  if (f < K.stats) {
    const panel = (i: number) => prog(f, K.panels[i], 22);
    const px = (i: number) => 120 + i * 580;
    return (
      <AbsoluteFill style={{ background: C.night }}>{audio}
        <Chrome at={0} />
        {[0, 1, 2].map((i) => (
          <div key={i} style={{ position: "absolute", left: px(i), top: 250, width: 540, height: 520, opacity: panel(i), transform: `translateY(${(1 - panel(i)) * 60}px)`, border: "1px solid rgba(65,72,104,0.8)", borderRadius: 10, background: "rgba(36,40,59,0.5)", padding: 28, fontFamily: MONO }}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: C.white, lineHeight: 1.1, marginBottom: 26, letterSpacing: "-0.02em" }}>
              {["Listed the day you ship.", `Voted up the Top ${FACTS.top}.`, "Found by people who install."][i]}
            </div>
            {i === 0 && <div style={{ position: "relative", height: 170 }}><Card p={lone} x={0} y={0} w={480} isNew /></div>}
            {i === 1 && <div style={{ display: "grid", gap: 10 }}>{["03", "02", "01"].map((r, j) => (
              <div key={r} style={{ display: "flex", gap: 14, alignItems: "center", padding: "10px 14px", border: `1px solid ${j === 2 && f >= K.panels[1] + 30 ? C.turq : "rgba(65,72,104,0.6)"}`, borderRadius: 7, fontSize: 22 }}>
                <span style={{ color: DIM }}>{r}</span><b style={{ color: j === 2 && f >= K.panels[1] + 30 ? C.turq : C.white, flex: 1 }}>{j === 2 ? lone.n : [ALL[5].n, ALL[9].n][j]}</b><span style={{ color: C.blue }}>▲</span>
              </div>))}</div>}
            {i === 2 && <div style={{ background: C.night, border: "1px solid rgba(65,72,104,0.8)", borderRadius: 7, padding: "18px 20px", fontSize: 24, color: C.white, lineHeight: 1.6 }}>
              <span style={{ color: C.green }}>~ $</span> omarchy pkg add {lone.n}<br /><span style={{ color: DIM }}>installing</span> <span style={{ color: C.blue }}>{"█".repeat(Math.min(12, Math.floor((f - K.panels[2]) / 4)))}</span><br /><span style={{ color: C.green }}>✓</span> done</div>}
            <div style={{ marginTop: 22, color: DIM, fontSize: 18, lineHeight: 1.5 }}>
              {["Synced from the official repo. No form, no gatekeeper.", "Readers vote. Rank comes from them, never from ads.", "Readers come to install, not to browse."][i]}
            </div>
          </div>
        ))}
        {f >= K.sponsor && (
          <div style={{ position: "absolute", left: W / 2 - 400, top: 820, width: 800, opacity: prog(f, K.sponsor, 16), border: "1px solid rgba(65,72,104,0.8)", borderRadius: 8, background: C.storm, padding: "14px 20px", fontFamily: MONO, fontSize: 20, color: C.white, display: "flex", gap: 18, alignItems: "center" }}>
            <span style={{ color: DIM, fontSize: 14, border: "1px solid rgba(65,72,104,0.8)", borderRadius: 4, padding: "2px 8px" }}>sponsor</span>
            <b>Your tool, next to {FACTS.packages} packages.</b><span style={{ color: DIM }}>Flat rate. No bidding. Static, labelled.</span>
          </div>
        )}
        <Stack until={K.stats} size={110} lines={[{ text: "Get noticed. Grow.", at: K.grow }, { text: "Get paid.", at: K.grow + 14, color: C.blue }]} />
        {f >= K.grow && <AbsoluteFill style={{ background: "rgba(26,27,38,0.82)", opacity: prog(f, K.grow, 14), zIndex: -1 }} />}
      </AbsoluteFill>
    );
  }

  // ---- act 6 + 7: growth, then the tease
  const dimP = prog(f, K.dim, 30);
  return (
    <AbsoluteFill style={{ background: C.night }}>{audio}
      <div style={{ opacity: 1 - 0.85 * dimP }}>
        <Chrome at={0} />
        {ALL.slice(0, 18).map((p, i) => { const c = cell(i); return <Card key={p.n} p={p} x={c.x} y={c.y + 60} opacity={0.35} />; })}
      </div>
      <AbsoluteFill style={{ background: "rgba(26,27,38,0.7)" }} />
      <Big at={K.stats} until={K.dim} size={96} y={st.visitorsLastMonth ? -200 : 0}>Readers are growing fast.</Big>
      {st.visitorsLastMonth && f >= K.stats && f < K.dim ? (
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <div style={{ display: "flex", gap: 140, marginTop: 120 }}>
            <Stat from={K.stats} at={14} value={fmt(st.visitorsLastMonth)} label="visitors last month" />
            {st.growthPct ? <Stat from={K.stats} at={28} value={`+${st.growthPct}%`} label="month over month" /> : null}
            {st.projectionNextMonth ? <Stat from={K.stats} at={42} value={fmt(st.projectionNextMonth)} label="projected next month" /> : null}
          </div>
        </AbsoluteFill>
      ) : null}
      {f >= K.dim && f < K.every && (
        <div style={{ position: "absolute", left: W / 2 - 330, top: 640, width: 660, height: 200, opacity: prog(f, K.biggest, 16) }}>
          <Card p={ALL[0]} x={0} y={0} w={660} big hi />
          <div style={{ position: "absolute", right: 26, bottom: 22, fontFamily: MONO, fontSize: 22, color: C.night, background: Math.floor(f / 8) % 2 === 0 ? C.turq : C.blue, borderRadius: 6, padding: "8px 16px" }}>??? ▸</div>
        </div>
      )}
      <Big at={K.nextWeek} until={K.every} size={132} color={C.orange} y={-250}>Next week,</Big>
      <Big at={K.biggest} until={K.every} size={80} y={-120}>the store gets its biggest upgrade yet.</Big>
      <Stack until={K.endCard} size={118} lines={[{ text: "Every app.", at: K.every }, { text: "Every maker.", at: K.every + 16 }, { text: "One big upgrade.", at: K.upgrade, color: C.blue }]} />
    </AbsoluteFill>
  );
};
