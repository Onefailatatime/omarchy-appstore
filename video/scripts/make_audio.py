#!/usr/bin/env python3
"""Synthesises both soundtracks from src/timeline.json so every hit lands on the
frame the video expects. Writes public/audio/boot.wav, public/audio/signal.wav
and src/typing.json (keystroke frames shared with BootSequence)."""
import json, wave, numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = json.load(open(ROOT / "src/timeline.json"))
FPS, SR = T["fps"], 44100
rng = np.random.RandomState(42)

def sec(frame): return frame / FPS
def t_axis(n): return np.arange(n) / SR
def write(path, y):
    y = y / max(1e-9, np.abs(y).max()) * 0.89   # normalise to -1 dBFS, no clipping
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def place(buf, start_s, sig):
    i = int(start_s * SR); j = min(len(buf), i + len(sig))
    if j > i: buf[i:j] += sig[: j - i]

def ramp(n, points):
    t = t_axis(n); xs, ys = zip(*points); return np.interp(t, xs, ys)

def pad_voice(freq, n, bright):
    t = t_axis(n); out = np.zeros(n)
    for det in (-0.4, 0.0, 0.4):
        f = freq * (2 ** (det / 1200)); vib = 1 + 0.003 * np.sin(2 * np.pi * 0.17 * t + det)
        for h in range(1, 9):
            gain = (1.0 / h) * np.clip(bright * 8 - (h - 1), 0, 1)
            out += gain * np.sin(2 * np.pi * f * h * vib * t + rng.rand() * 6.28)
    return out / 6

def reverb(y, taps=((0.031, 0.42), (0.067, 0.33), (0.113, 0.27), (0.197, 0.2)), wet=0.35):
    out = y.copy()
    for d, g in taps:
        k = int(d * SR); r = np.zeros_like(y); r[k:] = y[:-k] * g
        for _ in range(3):
            r2 = np.zeros_like(y); r2[k:] = r[:-k] * g; r += r2
        out += wet * r
    return out

def noise_burst(dur):
    n = int(dur * SR); x = np.diff(rng.randn(n), prepend=0)
    return x * np.exp(-t_axis(n) * (1 / (dur * 0.25)))

def thump(gain=1.0, f0=70, f1=42, dec=9):
    n = int(0.45 * SR); t = t_axis(n)
    ph = 2 * np.pi * np.cumsum(np.interp(t, [0, 0.06, 0.45], [f0, f1, f1])) / SR
    return np.sin(ph) * np.exp(-t * dec) * gain

def hit(gain=1.0):
    n = int(2.4 * SR); t = t_axis(n)
    ph = 2 * np.pi * np.cumsum(np.interp(t, [0, 0.12, 2.4], [95, 48, 46])) / SR
    out = np.sin(ph) * np.exp(-t * 1.8) * gain
    out[: int(0.03 * SR)] += noise_burst(0.03) * 0.5 * gain
    return out

def riser(dur, gain=0.2):
    n = int(dur * SR); x = rng.randn(n)
    x = np.convolve(x, np.ones(6) / 6, mode="same")
    return x * ramp(n, [(0, 0), (dur, gain)]) * np.linspace(0.3, 1, n)

def chord_bed(buf, chords, bright, master, gain=1.6):
    for (a, z), notes in chords:
        ln = int((z - a) * SR); i0 = int(a * SR)
        v = sum(pad_voice(fq, ln, bright[i0:i0 + ln]) for fq in notes) / len(notes) * gain
        att, rel = int(min(1.0, (z - a) / 3) * SR), int(min(1.0, (z - a) / 3) * SR)
        env = np.ones(ln); env[:att] = np.linspace(0, 1, att); env[-rel:] *= np.linspace(1, 0, rel)
        place(buf, a, v * env)
    buf *= master

def pulse(buf, start_s, end_s, bpm, gain_pts):
    beat = 60 / bpm; k = 0; t = start_s
    while t < end_s:
        g = np.interp(t, *zip(*gain_pts)); place(buf, t, thump(g, dec=11 if k % 2 else 9)); t += beat; k += 1

# ------------------------------------------------------------------ typing map
b = T["boot"]; segs = []
for sgm in b["typing"]:
    cmd, span = sgm["cmd"], sgm["end"] - sgm["start"]
    gaps = rng.uniform(0.6, 1.4, len(cmd)); gaps[[i for i, ch in enumerate(cmd) if ch in " -"]] += 0.9; gaps[0] = 0.3
    frames = sgm["start"] + np.cumsum(gaps) / gaps.sum() * span
    segs.append({"cmd": cmd, "frames": [round(float(x), 2) for x in frames]})
json.dump(segs, open(ROOT / "src/typing.json", "w"))

# ------------------------------------------------------------------ boot.wav
A, L = b["acts"], b["lines"]
n = int(sec(b["frames"]) * SR); boot = np.zeros(n)
for s in segs:
    for fr in s["frames"]:
        place(boot, sec(fr), noise_burst(0.018) * 0.3)
        m = int(0.014 * SR); place(boot, sec(fr), np.sin(2 * np.pi * rng.uniform(1700, 2500) * t_axis(m)) * np.linspace(0.12, 0, m))
        place(boot, sec(fr) + 0.055, noise_burst(0.012) * 0.22)
blip_frames = [L[k] for k in ("pushed", "stars1", "stars7", "stars30", "resolving", "found", "synced", "ranked", "guides", "checklist", "trackers", "install",
                              "listed", "noticed", "foundBy", "paid", "readers", "buildStart", "tick1")] + L["unpackAt"] + [L["dependsStart"] + i * L["dependsStep"] for i in range(12)]
for fr in blip_frames:
    m = int(0.03 * SR); place(boot, sec(fr), np.sin(2 * np.pi * 1320 * t_axis(m)) * np.exp(-t_axis(m) * 90) * 0.07)

end = sec(b["frames"]); hitS = sec(b["bassHit"])
# a low drone sits under the problem act, then chords take over from card 1
boot_bed = np.zeros(n)
chords = [((sec(A["card1"]) - 0.5, sec(A["resolve"]) + 0.5), (110.0, 164.81, 220.0)),                       # A minor, bare
          ((sec(A["resolve"]), sec(A["card2"]) + 0.3), (110.0, 164.81, 220.0, 261.63, 329.63)),                # Am full
          ((sec(A["card2"]), sec(A["builders"]) + 0.3), (87.31, 130.81, 174.61, 261.63)),                     # F
          ((sec(A["builders"]), sec(A["card3"]) + 0.3), (130.81, 196.0, 261.63, 329.63)),                     # C
          ((sec(A["card3"]), sec(A["build"]) + 0.3), (98.0, 146.83, 196.0, 293.66)),                          # G, tension
          ((sec(A["build"]), hitS), (110.0, 164.81, 220.0, 261.63, 329.63, 440.0))]                           # Am, peak
bright = ramp(n, [(0, 0.08), (sec(A["card1"]), 0.2), (sec(A["card2"]), 0.4), (sec(A["card3"]), 0.55), (hitS, 0.8)])
master = ramp(n, [(0, 0), (sec(A["card1"]), 0.3), (sec(A["card2"]), 0.4), (sec(A["card3"]), 0.42), (sec(A["build"]), 0.5), (hitS - 0.006, 0.52), (hitS, 0)])
chord_bed(boot_bed, chords, bright, master)
drone = np.sin(2 * np.pi * 55 * t_axis(n)) * ramp(n, [(0, 0), (2, 0.14), (sec(A["card1"]), 0.14), (sec(A["card1"]) + 0.2, 0)])
boot_bed += drone
pulse(boot_bed, sec(A["resolve"]), hitS - 0.1, 112, [(sec(A["resolve"]), 0.25), (sec(A["card2"]), 0.4), (sec(A["card3"]), 0.5), (hitS, 0.6)])
for card in ("card1", "card2", "card3"):                         # a riser into each statement card, a thump on the cut
    place(boot_bed, sec(A[card]) - 1.2, riser(1.2, 0.16)); place(boot_bed, sec(A[card]), hit(0.45)[: int(0.8 * SR)])
place(boot_bed, sec(A["build"]), hit(0.4)[: int(0.8 * SR)])
place(boot_bed, hitS, hit(0.75))
boot += reverb(boot_bed, wet=0.25)
write(ROOT / "public/audio/boot.wav", boot)

# ------------------------------------------------------------------ signal.wav
s = T["signal"]; n = int(sec(s["frames"]) * SR); sig = np.zeros(n); t = t_axis(n)
lock, burst, ign, hop = sec(s["lockAt"]), sec(s["burstStart"]), sec(s["ignite"]), sec(s["hoping"])
dim, nxt, hitS, end = sec(s["dim"]), sec(s["nextWeek"]), sec(s["bassHit"]), sec(s["frames"])
sub = np.sin(2 * np.pi * 36.71 * t) * ramp(n, [(0, 0), (3, 0.2), (hop, 0.22), (ign, 0.34), (lock, 0.36), (burst + 1.5, 0.22), (dim, 0.22), (dim + 1.5, 0.3), (hitS, 0.3), (hitS + 2, 0.18), (end - 2, 0.16), (end, 0)])
sig += sub
chords = [((0, hop + 0.3), (146.83, 220.0, 293.66)),                                   # Dm, thin and lonely
          ((hop, ign + 0.3), (116.54, 174.61, 233.08, 349.23)),                         # Bb
          ((ign, lock + 0.3), (174.61, 261.63, 349.23, 440.0, 523.25)),                  # F, climbing
          ((lock, burst + 0.3), (146.83, 220.0, 293.66, 349.23, 440.0)),                 # Dm, wide
          ((burst, sec(s["builders"]) + 0.3), (116.54, 174.61, 233.08, 293.66, 349.23)), # Bb
          ((sec(s["builders"]), dim + 0.3), (130.81, 196.0, 261.63, 329.63, 392.0)),     # C, bright
          ((dim, nxt + 0.3), (98.0, 146.83, 196.0)),                                      # G, hollow, tension
          ((nxt, hitS), (110.0, 164.81, 220.0, 261.63)),                                  # A, the question
          ((hitS, end), (146.83, 220.0, 293.66, 329.63, 440.0, 587.33))]                  # Dm add9, resolve
bright = ramp(n, [(0, 0.05), (hop, 0.12), (ign, 0.3), (lock, 0.8), (burst + 2, 0.5), (dim, 0.55), (dim + 1, 0.2), (nxt, 0.25), (hitS, 0.8), (end, 0.3)])
master = ramp(n, [(0, 0), (2, 0.12), (hop, 0.16), (ign, 0.24), (lock - 0.05, 0.52), (lock + 0.4, 0.48), (burst + 2, 0.4), (dim - 0.5, 0.42), (dim + 1, 0.14), (nxt, 0.16), (hitS - 0.01, 0.2), (hitS, 0.52), (end - 2, 0.4), (end, 0)])
chord_bed(sig, chords, bright, master)
pulse(sig, ign, dim - 0.2, 112, [(ign, 0.2), (lock, 0.45), (burst, 0.5), (dim, 0.55)])
place(sig, hop, hit(0.5)[: int(1.0 * SR)])
place(sig, lock - 1.6, riser(1.6, 0.2))
cn = int(3.2 * SR); tc = t_axis(cn); chime = np.zeros(cn)
for ratio, g, dec in ((1, 1, 1.4), (2.76, 0.5, 2.2), (5.4, 0.25, 3.5), (8.93, 0.12, 5)):
    chime += g * np.sin(2 * np.pi * 880 * ratio * tc) * np.exp(-tc * dec)
place(sig, lock, reverb(chime * 0.22, wet=0.5))
wn = int(1.1 * SR); whoosh = np.convolve(rng.randn(wn), np.ones(12) / 12, mode="same") * ramp(wn, [(0, 0), (0.35, 0.18), (1.1, 0)])
place(sig, burst - 0.15, whoosh)
for fr in s["different"] + s["builderLines"] + [s["grow"], s["stats"]]:
    place(sig, sec(fr), hit(0.3)[: int(0.5 * SR)])
place(sig, dim, riser(2.0, 0.22)); place(sig, nxt, hit(0.4)[: int(1.2 * SR)])
place(sig, hitS - 1.4, riser(1.4, 0.26)); place(sig, hitS, hit(0.85))
sig = reverb(sig, wet=0.22)
write(ROOT / "public/audio/signal.wav", sig)
print("wrote boot.wav", round(len(boot) / SR, 1), "s; signal.wav", round(len(sig) / SR, 1), "s")

# ================================================================== arcade.wav
def square(freq, n, duty=0.5, gain=1.0):
    t = t_axis(n); ph = (freq * t) % 1.0
    return np.where(ph < duty, 1.0, -1.0) * gain

def tri(freq, n, gain=1.0):
    t = t_axis(n); return (2 * np.abs(2 * ((freq * t) % 1.0) - 1) - 1) * gain

def env_ad(n, a=0.004, dec=6.0):
    t = t_axis(n); e = np.minimum(1, t / a) * np.exp(-np.maximum(0, t - a) * dec); return e

def nz(dur, dec):
    n = int(dur * SR); return rng.randn(n) * np.exp(-t_axis(n) * dec)

r = T["arcade"]; n = int(sec(r["frames"]) * SR); arc = np.zeros(n)
BPM = 128; beat = 60 / BPM; eighth = beat / 2; sixteenth = beat / 4
NOTE = lambda name: {"A2": 110.0, "C3": 130.81, "E3": 164.81, "F2": 87.31, "F3": 174.61, "G2": 98.0, "G3": 196.0, "A3": 220.0, "C4": 261.63, "E4": 329.63, "F4": 349.23, "G4": 392.0, "A4": 440.0, "B4": 493.88, "C5": 523.25, "D5": 587.33, "E5": 659.25}[name]
PROG = [("A2", ["A3", "C4", "E4", "A4"]), ("F2", ["F3", "A3", "C4", "F4"]), ("C3", ["C4", "E4", "G4", "C5"]), ("G2", ["G3", "B4", "D5", "G4"])]

def chip_section(buf, start_s, end_s, lead=True, drums=True, gain=1.0):
    """Two bars per chord, bass on eighths, arpeggio on sixteenths, kick/snare/hat."""
    t = start_s; bar = 0
    while t < end_s:
        root, arp = PROG[(bar // 2) % 4]
        for k in range(8):                                         # bass, eighths
            s0 = t + k * eighth; ln = int(eighth * 0.9 * SR)
            place(buf, s0, square(NOTE(root) * (2 if k % 4 == 3 else 1), ln, 0.5, 0.11 * gain) * env_ad(ln, 0.003, 4))
        if lead:
            for k in range(16):                                    # arpeggio, sixteenths
                s0 = t + k * sixteenth; ln = int(sixteenth * 0.8 * SR)
                note = arp[[0, 1, 2, 3, 2, 1][k % 6]]
                place(buf, s0, square(NOTE(note) * 2, ln, 0.25, 0.05 * gain) * env_ad(ln, 0.002, 10))
        if drums:
            for k in range(4):
                place(buf, t + k * beat, thump(0.5 * gain, 110, 50, 16)[: int(0.25 * SR)])
                if k % 2 == 1: place(buf, t + k * beat, nz(0.14, 28) * 0.22 * gain)
            for k in range(8): place(buf, t + k * eighth + sixteenth, nz(0.03, 120) * 0.08 * gain)
        t += 4 * beat; bar += 1

def coin(buf, at):
    for i, fq in enumerate((987.77, 1318.51)):
        ln = int((0.08 if i == 0 else 0.4) * SR); place(buf, at + i * 0.08, square(fq, ln, 0.5, 0.25) * env_ad(ln, 0.002, 4 if i else 20))

def waka(buf, at, up=True):
    ln = int(0.07 * SR); t = t_axis(ln); f0, f1 = (300, 620) if up else (620, 300)
    ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, ln)) / SR
    place(buf, at, np.sign(np.sin(ph)) * 0.12 * env_ad(ln, 0.002, 30))

def arp_up(buf, at, notes, step=0.07, gain=0.22):
    for i, nm in enumerate(notes):
        ln = int(0.25 * SR); place(buf, at + i * step, square(NOTE(nm), ln, 0.5, gain) * env_ad(ln, 0.002, 9))

def descend(buf, at):
    for i, fq in enumerate((392.0, 349.23, 311.13, 261.63, 207.65)):
        ln = int(0.22 * SR); place(buf, at + i * 0.2, square(fq, ln, 0.5, 0.2) * env_ad(ln, 0.002, 8))

s1, lanes, lvl, st2, sc, dark, hitS, end = (sec(r[k]) for k in ("stage1", "lanes", "levelUp", "stage2", "scores", "dark", "bassHit", "frames"))
# act 1: a lonely two-note bass pulse, no drums
chip_section(arc, sec(r["lone"]), sec(r["gameOver"]), lead=False, drums=False, gain=0.6)
descend(arc, sec(r["gameOver"]))
coin(arc, sec(r["coin"]))
arp_up(arc, s1, ["A3", "C4", "E4", "A4", "C5", "E5"], 0.06)
chip_section(arc, s1 + 0.5, lanes, lead=False, drums=True, gain=0.8)
chip_section(arc, lanes, lvl, lead=True, drums=True, gain=1.0)
for i in range(3):                                                 # chomping through the lanes
    a = lanes + i * sec(r["laneLen"])
    for k in range(18): waka(arc, a + k * sec(r["laneLen"]) / 18, up=k % 2 == 0)
arp_up(arc, lvl, ["C4", "E4", "G4", "C5", "E5", "G4", "C5", "E5"], 0.05, 0.26)
chip_section(arc, st2, sc, lead=True, drums=True, gain=1.0)
for at in r["pellets"]: arp_up(arc, sec(at), ["E4", "A4", "C5"], 0.05, 0.2)
chip_section(arc, sc, dark, lead=False, drums=True, gain=0.9)
place(arc, dark, riser(1.0, 0.2)); descend(arc, dark + 0.2)
chip_section(arc, sec(r["nextWeek"]) + 0.2, hitS, lead=False, drums=False, gain=0.7)  # bare bass under the tease
for i in range(6): place(arc, sec(r["player2"]) + i * 0.33, square(1046.5 if i % 2 else 880, int(0.06 * SR), 0.5, 0.12) * env_ad(int(0.06 * SR), 0.002, 30))
place(arc, hitS - 1.2, riser(1.2, 0.25)); place(arc, hitS, hit(0.9))
chip_section(arc, hitS + 0.1, sec(r["endCard"]), lead=True, drums=True, gain=1.0)
write(ROOT / "public/audio/arcade.wav", reverb(arc, wet=0.12))

# ================================================================== catalogue.wav
c = T["catalogue"]; n = int(sec(c["frames"]) * SR); cat = np.zeros(n); t = t_axis(n)
asm, srch, lead_, bld, sts, dim_, nxt, hitS, end = (sec(c[k]) for k in ("assemble", "search", "leaderboard", "builders", "stats", "dim", "nextWeek", "bassHit", "frames"))
BPM = 120; beat = 60 / BPM
def four_floor(buf, a, z, gain_pts, hats=True, bass_root=None):
    tt = a; k = 0
    while tt < z:
        g = np.interp(tt, *zip(*gain_pts))
        place(buf, tt, thump(0.6 * g, 90, 46, 12)[: int(0.3 * SR)])
        if hats: place(buf, tt + beat / 2, nz(0.03, 150) * 0.1 * g)
        if bass_root is not None:
            ln = int(beat / 2 * 0.85 * SR); fq = bass_root(tt)
            for j in range(2):
                v = sum(np.sin(2 * np.pi * fq * (j + 1) * h * t_axis(ln)) / h for h in range(1, 6)) / 3
                place(buf, tt + j * beat / 2, v * env_ad(ln, 0.004, 5) * 0.16 * g)
        tt += beat; k += 1
chords = [((sec(c["hoped"][0]), asm + 0.3), (146.83, 220.0, 293.66)),                      # Dm, lonely
          ((asm, srch + 0.3), (174.61, 261.63, 349.23, 440.0)),                             # F
          ((srch, lead_ + 0.3), (130.81, 196.0, 261.63, 329.63, 392.0)),                     # C
          ((lead_, bld + 0.3), (116.54, 174.61, 233.08, 349.23)),                            # Bb
          ((bld, sts + 0.3), (174.61, 261.63, 349.23, 440.0, 523.25)),                       # F bright
          ((sts, dim_ + 0.3), (130.81, 196.0, 261.63, 392.0)),                               # C
          ((dim_, hitS), (110.0, 164.81, 220.0)),                                            # Am, hollow
          ((hitS, end), (146.83, 220.0, 293.66, 329.63, 440.0, 587.33))]                     # Dm add9
bright = ramp(n, [(0, 0.08), (asm, 0.3), (srch, 0.5), (bld, 0.65), (dim_, 0.5), (dim_ + 1, 0.15), (hitS, 0.8), (end, 0.3)])
master = ramp(n, [(0, 0), (1, 0.14), (sec(c["hoping"]), 0.2), (asm, 0.34), (srch, 0.38), (bld, 0.42), (dim_ - 0.3, 0.42), (dim_ + 1, 0.12), (hitS - 0.01, 0.14), (hitS, 0.5), (end - 2, 0.4), (end, 0)])
chord_bed(cat, chords, bright, master)
roots = [(asm, 87.31), (srch, 65.41), (lead_, 58.27), (bld, 87.31), (sts, 65.41)]
def root_at(tt): return [fq for a, fq in roots if tt >= a][-1] if tt >= asm else 73.42
four_floor(cat, asm, dim_ - 0.2, [(asm, 0.5), (srch, 0.8), (bld, 1.0), (dim_, 1.0)], bass_root=root_at)
place(cat, sec(c["hoping"]), hit(0.5)[: int(1.0 * SR)])
for k in c["searchKeys"] + c["cmdKeys"]:                              # keystrokes in search and the install command
    place(cat, sec(k), noise_burst(0.018) * 0.3); m = int(0.014 * SR); place(cat, sec(k), np.sin(2 * np.pi * rng.uniform(1700, 2500) * t_axis(m)) * np.linspace(0.12, 0, m))
for k in ("assemble", "chrome", "filtered", "zoom", "copied", "leaderboard", "climb", "builders", "sponsor", "grow", "stats"):
    place(cat, sec(c[k]), hit(0.3)[: int(0.5 * SR)])
for i in range(3): place(cat, sec(c["panels"][i]), hit(0.28)[: int(0.4 * SR)])
ln = int(0.12 * SR); place(cat, sec(c["copied"]), np.sin(2 * np.pi * 1760 * t_axis(ln)) * env_ad(ln, 0.002, 25) * 0.15)
place(cat, dim_ - 1.0, riser(1.0, 0.2)); place(cat, nxt, hit(0.4)[: int(1.2 * SR)])
place(cat, hitS - 1.4, riser(1.4, 0.26)); place(cat, hitS, hit(0.85))
write(ROOT / "public/audio/catalogue.wav", reverb(cat, wet=0.2))
print("wrote arcade.wav", round(len(arc) / SR, 1), "s; catalogue.wav", round(len(cat) / SR, 1), "s")
