#!/usr/bin/env node
// Resize one screenshot to 1200px and 600px WebP/AVIF at quality 75.
// Usage: node optimize.mjs --input in.png --out-dir dir --stem abc123 --quality 75 --widths 1200,600
import { mkdir, writeFile } from "node:fs/promises";
import { parseArgs } from "node:util";
import { join } from "node:path";
import sharp from "sharp";

const { values } = parseArgs({
  options: {
    input: { type: "string" },
    "out-dir": { type: "string" },
    stem: { type: "string" },
    quality: { type: "string", default: "75" },
    widths: { type: "string", default: "1200,600" },
  },
});

if (!values.input || !values["out-dir"] || !values.stem) {
  console.error("optimize.mjs: --input, --out-dir and --stem are required");
  process.exit(2);
}

const quality = Number(values.quality);
const widths = values.widths.split(",").map((w) => Number(w)).filter((w) => w > 0);
const outDir = values["out-dir"];
await mkdir(outDir, { recursive: true });

const sharpOpts = { animated: true, failOn: "none", limitInputPixels: 268402689 };
const base = sharp(values.input, sharpOpts).rotate();
const meta = await base.metadata();
const srcWidth = meta.width || 0;
const srcHeight = meta.pageHeight || meta.height || 0;
const animated = (meta.pages || 1) > 1;
const files = [];

for (const width of widths) {
  const target = Math.min(width, srcWidth || width);
  if (width !== widths[0] && srcWidth && srcWidth <= widths[widths.length - 1] && width !== srcWidth) {
    // Still emit the smaller variant when the source is at least that wide.
  }
  if (srcWidth && target < 1) continue;
  if (width !== widths[0] && srcWidth && srcWidth < width) {
    // Do not invent a larger named width than the source; skip this step.
    // The largest requested width that fits is still written above when it matches min(width, srcWidth).
    continue;
  }

  const suffix = `${target}`;
  const webpPath = join(outDir, `${values.stem}-${suffix}.webp`);
  const avifPath = join(outDir, `${values.stem}-${suffix}.avif`);

  const resized = () =>
    sharp(values.input, sharpOpts)
      .rotate()
      .resize({ width: target, withoutEnlargement: true });

  await resized().webp({ quality, effort: 4 }).toFile(webpPath);
  const entry = { width: target, webp: webpPath };
  if (!animated) {
    await resized().avif({ quality, effort: 4 }).toFile(avifPath);
    entry.avif = avifPath;
  }
  files.push(entry);
}

// Intrinsic size of the largest written variant (for width/height attributes).
const largest = files[0];
let displayWidth = largest?.width || srcWidth;
let displayHeight = srcHeight;
if (srcWidth && displayWidth && srcHeight) {
  displayHeight = Math.max(1, Math.round(srcHeight * (displayWidth / srcWidth)));
}

const result = {
  sourceWidth: srcWidth,
  sourceHeight: srcHeight,
  width: displayWidth,
  height: displayHeight,
  format: meta.format,
  animated,
  files: files.map((f) => ({
    width: f.width,
    webp: f.webp,
    avif: f.avif || null,
  })),
};
await writeFile(join(outDir, `${values.stem}.json`), JSON.stringify(result), "utf8");
process.stdout.write(JSON.stringify(result) + "\n");
