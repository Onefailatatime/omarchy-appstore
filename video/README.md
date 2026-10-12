# Omarchyapps teaser videos

Four Remotion cuts of the "next week" teaser, all 1920x1080, all ending on the same card.

| Composition | Output | Style |
|---|---|---|
| BootSequence | out/boot-sequence.mp4 | One terminal, package-manager narrative |
| SignalField | out/signal-from-the-field.mp4 | Homepage star field, cinematic typography |
| Arcade | out/insert-coin.mp4 | CRT attract mode, Pac-Man lanes, chiptune |
| Catalogue | out/live-catalogue.mp4 | The site's own catalogue UI in motion |

- `src/timeline.json` holds every beat as a frame number. The soundtracks are synthesised from the same file by `scripts/make_audio.py`, so moving a beat and re-running the script keeps picture and sound in step.
- `src/stats.json` holds the traffic figures. Null fields are skipped in every cut.
- `src/facts.ts` holds the counts the site publishes (packages, categories, checklist length, Top 25).
- `src/catalogue.json` and `src/packages.json` are copies of the real catalogue; refresh them from `../data/packages-brief.json` after a package sync.

```bash
python3 scripts/make_audio.py
npm run render:all
```
