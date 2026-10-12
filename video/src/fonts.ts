import { continueRender, delayRender, staticFile } from "remotion";

/* Load the site's own woff2 files once per render process. */
let loaded: Promise<void> | null = null;
export function useSiteFonts() {
  if (typeof document === "undefined") return;
  if (!loaded) {
    const handle = delayRender("site fonts");
    const faces = [
      new FontFace("Geist", `url(${staticFile("fonts/geist-latin-wght-normal.woff2")}) format("woff2-variations")`, { weight: "100 900" }),
      new FontFace("JetBrains Mono", `url(${staticFile("fonts/jetbrains-mono-latin-400.woff2")}) format("woff2")`, { weight: "400" }),
      new FontFace("JetBrains Mono", `url(${staticFile("fonts/jetbrains-mono-latin-700.woff2")}) format("woff2")`, { weight: "700" }),
    ];
    loaded = Promise.all(faces.map((f) => f.load().then((l) => document.fonts.add(l))))
      .then(() => continueRender(handle))
      .catch((e) => { console.error(e); continueRender(handle); });
  }
}
