import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame } from "remotion";
import { C, MONO } from "./theme";
import { useSiteFonts } from "./fonts";
import { EndCard } from "./EndCard";
import { Card } from "./Card";
import T from "./timeline.json";
import typing from "./typing.json";
import pkgs from "./packages.json";
import stats from "./stats.json";
import { FACTS } from "./facts";

const B = T.boot, A = B.acts, L = B.lines;
const DEPS = pkgs.slice(0, 12);
const PAD = "           ";
const DIM = "rgba(122,162,247,0.62)";

const Cursor = () => <span style={{ display: "inline-block", width: 22, height: 44, background: C.white, verticalAlign: -8 }} />;
const Label: React.FC<{ children: string }> = ({ children }) => <span style={{ color: DIM }}>{children.padEnd(11)}</span>;
const Line: React.FC<{ at: number; children: React.ReactNode }> = ({ at, children }) => (useCurrentFrame() < at ? null : <div>{children}</div>);

/* One typed command. Keystroke frames come from typing.json so the clicks in the soundtrack match. */
const Typed: React.FC<{ seg: number; at: number; cursorUntil: number }> = ({ seg, at, cursorUntil }) => {
  const f = useCurrentFrame();
  const s = typing[seg];
  if (f < at) return null;
  const typed = s.frames.filter((t) => f >= t).length;
  const done = typed >= s.cmd.length;
  const blink = Math.floor(f / 14) % 2 === 0;
  const cursor = !done || (f < cursorUntil && blink);
  return <div><span style={{ color: C.green }}>~ $</span> {s.cmd.slice(0, typed)}{cursor && <Cursor />}</div>;
};

const Term: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: C.night, color: C.white, fontFamily: MONO, fontSize: 38, lineHeight: "58px", padding: "110px 150px", whiteSpace: "pre" }}>{children}</AbsoluteFill>
);

const fmt = (n: number) => n.toLocaleString("en-US");

export const BootSequence = () => {
  useSiteFonts();
  const f = useCurrentFrame();
  const audio = <Audio src={staticFile("audio/boot.wav")} />;

  if (f >= A.endCard) return <AbsoluteFill style={{ background: C.night }}>{audio}<EndCard from={A.endCard} /></AbsoluteFill>;

  if (f >= A.build) {
    const pct = Math.round(interpolate(f, [L.buildStart, L.buildEnd], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
    const cells = 28, filled = Math.round((pct / 100) * cells);
    return (
      <Term>{audio}
        <Typed seg={4} at={A.build} cursorUntil={L.buildStart} />
        <Line at={L.buildStart}><Label>building</Label><span style={{ color: C.blue }}>{"█".repeat(filled)}</span><span style={{ color: C.tblack }}>{"░".repeat(cells - filled)}</span> {String(pct).padStart(3)}%</Line>
        <Line at={L.unpackAt[0]}><Label>unpacking</Label>./guides/*</Line>
        <Line at={L.unpackAt[1]}><Label>unpacking</Label>./support/*</Line>
        <Line at={L.unpackAt[2]}><Label>unpacking</Label>./sponsors/*</Line>
        <Line at={L.unpackAt[3]}><Label>linking</Label>developers → users</Line>
        <Line at={L.tick1}>{"\n"}<span style={{ color: C.green }}>✓</span> upgraded <span style={{ color: C.cyan }}>omarchyapps</span>  1.x → <span style={{ color: C.cyan }}>2.0</span></Line>
        <Line at={L.tick2}><span style={{ color: C.green }}>✓</span> scheduled for <span style={{ color: C.orange }}>next week</span></Line>
        <Line at={L.prompt}>{"\n"}<span style={{ color: C.green }}>~ $</span> {Math.floor(f / 14) % 2 === 0 && <Cursor />}</Line>
      </Term>
    );
  }

  if (f >= A.card3) return <AbsoluteFill style={{ background: C.night }}>{audio}<Card from={A.card3} lines={[{ text: "Next week,", at: 0, color: C.orange }, { text: "the store gets its biggest upgrade yet.", at: 40 }]} size={104} /></AbsoluteFill>;

  if (f >= A.builders) {
    const s = stats as { visitorsLastMonth: number | null; growthPct: number | null; projectionNextMonth: number | null };
    return (
      <Term>{audio}
        <Typed seg={3} at={A.builders} cursorUntil={L.listed} />
        <Line at={L.listed}><Label>listed</Label>the day you ship   <span style={{ color: DIM }}># synced from the official repo</span></Line>
        <Line at={L.noticed}><Label>noticed</Label>readers vote you up the Top {FACTS.top}</Line>
        <Line at={L.foundBy}><Label>found</Label>by people who actually install</Line>
        <Line at={L.paid}><Label>paid</Label>sponsor spots, users who stick around</Line>
        <Line at={L.readers}>{"\n"}<Label>readers</Label><span style={{ color: C.cyan }}>growing fast</span>{s.visitorsLastMonth ? `   ${fmt(s.visitorsLastMonth)} last month` : ""}</Line>
        {s.growthPct ? <Line at={L.stat1}><Label>growth</Label><span style={{ color: C.cyan }}>+{s.growthPct}%</span> month over month</Line> : null}
        {s.projectionNextMonth ? <Line at={L.stat2}><Label>projected</Label>{fmt(s.projectionNextMonth)} next month</Line> : null}
      </Term>
    );
  }

  if (f >= A.card2) return <AbsoluteFill style={{ background: C.night }}>{audio}<Card from={A.card2} lines={[{ text: "Built for builders.", at: 0 }, { text: "Get noticed. Grow. Get paid.", at: 40, color: C.blue }]} /></AbsoluteFill>;

  if (f >= A.resolve) {
    const depColor = (i: number) => (f - (L.dependsStart + i * L.dependsStep) < 6 ? C.turq : C.white);
    return (
      <Term>{audio}
        <Typed seg={2} at={A.resolve} cursorUntil={L.resolving} />
        <Line at={L.resolving}><Label>resolving</Label>omarchyapps.com</Line>
        <Line at={L.found}><Label>found</Label><span style={{ color: C.cyan }}>{FACTS.packages}</span> packages · <span style={{ color: C.cyan }}>{FACTS.categories}</span> categories · one place</Line>
        <Line at={L.synced}><Label>synced</Label>from pkgs.omarchy.org, the official repo</Line>
        <Line at={L.ranked}><Label>ranked by</Label>readers, not ads   <span style={{ color: DIM }}># the Top {FACTS.top}</span></Line>
        <Line at={L.guides}><Label>guides</Label>that get people installing</Line>
        <Line at={L.checklist}><Label>checklist</Label>{FACTS.checklist} checks for packagers</Line>
        <Line at={L.trackers}><Label>trackers</Label>none</Line>
        <Line at={L.install}><Label>install</Label><span style={{ color: C.green }}>omarchy pkg add &lt;name&gt;</span></Line>
        <Line at={L.dependsStart}>{"\n"}<Label>including</Label>
          {DEPS.map((d, i) => (
            <span key={d} style={{ color: depColor(i), opacity: f >= L.dependsStart + i * L.dependsStep ? 1 : 0 }}>
              {i > 0 && i % 3 === 0 ? "\n" + PAD : ""}{d.padEnd(i % 3 === 2 ? 0 : 17)}
            </span>
          ))}
          <span style={{ color: DIM, opacity: f >= L.dependsStart + 12 * L.dependsStep ? 1 : 0 }}>{"\n" + PAD}+{FACTS.packages - 12} more</span>
        </Line>
      </Term>
    );
  }

  if (f >= A.card1) return <AbsoluteFill style={{ background: C.night }}>{audio}<Card from={A.card1} lines={[{ text: "Hoping is not a plan.", at: 0 }, { text: "There is a better way.", at: 45, color: C.blue }]} /></AbsoluteFill>;

  // act 1: the problem
  return (
    <Term>{audio}
      <Typed seg={0} at={0} cursorUntil={L.pushed} />
      <Line at={L.pushed}><Label>→</Label>github.com/you/your-omarchy-app   <span style={{ color: C.green }}>done</span></Line>
      <Typed seg={1} at={L.pushed + 20} cursorUntil={L.stars1} />
      <Line at={L.stars1}><Label>stars</Label>0        <span style={{ color: DIM }}>day 1</span></Line>
      <Line at={L.stars7}><Label>stars</Label>0        <span style={{ color: DIM }}>day 7</span></Line>
      <Line at={L.stars30}><Label>stars</Label>1        <span style={{ color: DIM }}>day 30</span></Line>
      <Line at={L.hoping}>{"\n"}<span style={{ color: DIM }}># hoping someone finds your repo is not a plan</span></Line>
    </Term>
  );
};
