import { C, MONO } from "./theme";
import { CAT } from "./catcolors";
import cat from "./catalogue.json";

export type Pkg = { n: string; d: string; c: string; s?: string };
export const ALL = cat as Pkg[];
export const DIM = "rgba(122,162,247,0.62)";

/* A catalogue card in the site's own styling: storm fill, 1px border, category dot, install size. */
export const Card: React.FC<{ p: Pkg; w?: number; hi?: boolean; isNew?: boolean; big?: boolean; style?: React.CSSProperties }> =
  ({ p, w, hi = false, isNew = false, big = false, style }) => (
  <div style={{ width: w, background: C.storm, border: `1px solid ${hi ? CAT[p.c] : "rgba(65,72,104,0.8)"}`, borderTop: isNew ? `2px solid ${C.orange}` : undefined, borderRadius: 7,
    padding: big ? "22px 26px" : "14px 16px", fontFamily: MONO, fontSize: big ? 26 : 17, color: C.blue, display: "flex", flexDirection: "column", gap: big ? 12 : 7, boxSizing: "border-box", ...style }}>
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 10 }}>
      <b style={{ color: hi ? C.turq : C.white, fontSize: big ? 34 : 18, overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis" }}>{p.n}</b>
      {isNew ? <span style={{ color: C.orange, fontSize: big ? 20 : 13, whiteSpace: "nowrap" }}>new</span> : <span style={{ color: DIM, fontSize: big ? 20 : 13, whiteSpace: "nowrap" }}>{p.s ?? ""}</span>}
    </div>
    <div style={{ color: "rgba(122,162,247,0.85)", lineHeight: 1.4, overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" }}>{p.d}</div>
    <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: big ? 20 : 13, color: DIM }}>
      <span style={{ width: big ? 12 : 8, height: big ? 12 : 8, borderRadius: 6, background: CAT[p.c] ?? C.tblack }} />{p.c}
    </div>
  </div>
);

/* The site's top bar, without the ad links. */
export const SiteBar: React.FC<{ size?: number }> = ({ size = 18 }) => (
  <div style={{ height: size * 3.4, borderBottom: "1px solid rgba(65,72,104,0.8)", display: "flex", alignItems: "center", padding: `0 ${size * 1.6}px`, gap: size * 1.6, fontFamily: MONO, fontSize: size, color: C.blue }}>
    <b style={{ color: C.white, fontSize: size * 1.15 }}>Omarchy Apps</b>
    {["Apps", "Top apps", "Guides", "Develop"].map((n) => <span key={n}>{n}</span>)}
  </div>
);

export const LeaderRow: React.FC<{ p: Pkg; rank: number; hi?: boolean; pulse?: boolean; size?: number }> = ({ p, rank, hi = false, pulse = false, size = 22 }) => (
  <div style={{ display: "flex", alignItems: "center", gap: size * 0.8, padding: `${size * 0.4}px ${size * 0.7}px`, border: `1px solid ${hi ? CAT[p.c] : "rgba(65,72,104,0.5)"}`, borderRadius: 7, background: hi ? "rgba(65,72,104,0.28)" : "transparent", fontFamily: MONO, fontSize: size }}>
    <span style={{ color: DIM, width: size * 1.6 }}>{String(rank).padStart(2, "0")}</span>
    <span style={{ width: size * 0.45, height: size * 0.45, borderRadius: size, background: CAT[p.c] }} />
    <b style={{ color: hi ? C.turq : C.white, flex: 1, overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis" }}>{p.n}</b>
    <span style={{ color: pulse ? C.turq : C.blue, border: "1px solid rgba(65,72,104,0.8)", borderRadius: 6, padding: `${size * 0.15}px ${size * 0.5}px` }}>▲</span>
  </div>
);
