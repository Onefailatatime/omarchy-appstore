/* Animated hero backdrop. One canvas per .hero-pixels element; the variant
   comes from data-mode: "drift" (seeded dither that breathes and slides),
   "matrix" (falling columns) or "pacman" (dot lanes with a chomping sprite).
   Draws nothing while off-screen, in a hidden tab, or when the visitor asks
   for reduced motion (then it paints one static frame). Tokyo Night palette. */
(function () {
  var NIGHT = [26, 27, 38], BLACK = [65, 72, 104], BLUE = [122, 162, 247], CYAN = [125, 207, 255],
      GREEN = [158, 206, 106], ORANGE = [255, 158, 100], WHITE = [192, 202, 245], TURQ = [180, 249, 248],
      PINK = [247, 118, 142], MAGENTA = [187, 154, 247], PURPLE = [157, 124, 216];
  function rgba(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function makeRng(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }

  /* ---------- drift: the dither field as a star field. Cells stay put; each has
     its own slow eased fade so some are always blinking in while others blink
     out, in Tokyo Night blues with pinks, reds and purples mixed in. The layout
     is different for every visit. ---------- */
  var STAR_TONES = [
    [BLACK, 0.55, 0.40], [BLACK, 0.55, 0.12], [BLUE, 0.38, 0.16], [CYAN, 0.45, 0.08],
    [MAGENTA, 0.40, 0.09], [PURPLE, 0.42, 0.07], [PINK, 0.38, 0.06], [TURQ, 0.35, 0.02]
  ];
  function pickTone(r) {
    var acc = 0;
    for (var i = 0; i < STAR_TONES.length; i++) { acc += STAR_TONES[i][2]; if (r <= acc) return STAR_TONES[i]; }
    return STAR_TONES[0];
  }
  // Per-cell noise salted with a per-visit seed, so every visitor (and every
  // reload) gets their own sky. Stable within one page view, so nothing jumps.
  var VISIT = (Math.random() * 2147483647) | 0;
  function hash(x, y, k) {
    var n = (x * 374761393 + y * 668265263 + k * 1274126177 + VISIT) | 0;
    n = (n ^ (n >>> 13)) * 1274126177 | 0;
    return ((n ^ (n >>> 16)) >>> 0) / 4294967296;
  }
  function ease(v) { return v * v * (3 - 2 * v); } // smoothstep
  function drift(ctx, w, h, t) {
    var cell = 12, gap = 2;
    var cols = Math.ceil(w / cell) + 2, rows = Math.ceil(h / cell);
    var cx = cols / 2, cy = rows * 0.42;
    var first = 0, frac = 0;                      // fixed field: cells twinkle in place
    for (var y = 0; y < rows; y++) {
      for (var x = 0; x < cols; x++) {
        var wx = x + first;                       // world column for the noise
        var dx = (x - cx) / cols * 2, dy = (y - cy) / rows * 2.2;
        var d = Math.sqrt(dx * dx + dy * dy);
        var p = Math.max(0, 0.55 - d * 0.5) * (0.65 + hash(wx, y, 1) * 0.7);
        if (hash(wx, y, 2) > p) continue;
        var tone = pickTone(hash(wx, y, 3));
        var phase = hash(wx, y, 4) * 6.283, period = 3000 + hash(wx, y, 5) * 7000;
        // 0..1 sine, eased at both ends so cells breathe in and out with no hard edge
        var v = 0.5 + 0.5 * Math.sin(t * (6.283 / period) + phase);
        var a = tone[1] * ease(ease(v));
        if (a < 0.004) continue;
        ctx.fillStyle = rgba(tone[0], a);
        ctx.fillRect(x * cell - frac, y * cell, cell - gap, cell - gap);
      }
    }
  }

  /* ---------- matrix: columns of half-width katakana and digits, bright head, fading tail ---------- */
  var KATA = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789";
  function matrixFactory() {
    var cols = null, cell = 16;
    return function (ctx, w, h, t, dt) {
      var n = Math.ceil(w / cell), rows = Math.ceil(h / cell) + 1;
      if (!cols || cols.length !== n) {
        var rnd = makeRng(4242);
        cols = [];
        for (var i = 0; i < n; i++) {
          var glyphs = [];
          for (var g = 0; g < rows + 24; g++) glyphs.push(KATA[Math.floor(rnd() * KATA.length)]);
          cols.push({ y: rnd() * rows * -1.5, v: 5 + rnd() * 10, len: 8 + Math.floor(rnd() * 18), seed: rnd() * 1000, glyphs: glyphs });
        }
      }
      ctx.font = "700 " + (cell - 2) + "px 'JetBrains Mono', ui-monospace, monospace";
      ctx.textBaseline = "top";
      for (var i = 0; i < n; i++) {
        var c = cols[i];
        c.y += c.v * dt / 1000;
        if (c.y - c.len > rows) { c.y = -Math.random() * rows * 0.8; c.v = 5 + Math.random() * 10; c.len = 8 + Math.floor(Math.random() * 18); }
        // mutate a glyph now and then so the columns shimmer
        if (Math.random() < 0.08) c.glyphs[Math.floor(Math.random() * c.glyphs.length)] = KATA[Math.floor(Math.random() * KATA.length)];
        var head = Math.floor(c.y);
        for (var k = 0; k < c.len; k++) {
          var y = head - k;
          if (y < 0 || y >= rows) continue;
          var f = 1 - k / c.len;
          var flick = 0.75 + 0.25 * Math.sin(t * 0.01 + c.seed + k);
          ctx.fillStyle = k === 0 ? rgba(TURQ, 0.95) : rgba(GREEN, 0.62 * f * flick);
          ctx.fillText(c.glyphs[(y + c.glyphs.length) % c.glyphs.length], i * cell + 1, y * cell);
        }
      }
    };
  }

  /* ---------- pacman: two dot lanes. The top lane is a plain chase. The bottom
     lane runs the full bit: Pac-Man eats dots, grabs a piece of fruit, grows,
     turns around at speed and gobbles the ghost, whose eyes float off; then the
     whole thing resets. Ghost eyes go wonky every now and then in both lanes. ---------- */
  function pacmanFactory() {
    var lanes = null, px = 5;
    var PAC_OPEN = ["..XXXXX..", ".XXXXXXX.", "XXXXXXXXX", "XXXXXX...", "XXXX.....", "XXXXXX...", "XXXXXXXXX", ".XXXXXXX.", "..XXXXX.."];
    var PAC_SHUT = ["..XXXXX..", ".XXXXXXX.", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", ".XXXXXXX.", "..XXXXX.."];
    var GHOST = ["..XXXXX..", ".XXXXXXX.", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXXXX", "X.XX.XX.X"];
    var FRUITS = [
      { name: "cherry", art: ["....GG...", "...G.G...", "..G..G...", ".RR..RR..", "RRRRRRRR.", "RRRRRRRR.", "RWRRRWRR.", ".RR..RR..", "........."] },
      { name: "strawberry", art: ["...GGG...", "..GGGGG..", ".RRRRRRR.", "RRWRRRWRR", "RRRRWRRRR", "RRWRRRWRR", ".RRRRRRR.", "..RRRRR..", "...RRR..."] },
      { name: "orange", art: ["....G....", "...GG....", ".OOOOOOO.", "OOOOOOOOO", "OOOOOOOOO", "OOOOOOOOO", "OOOOOOOOO", ".OOOOOOO.", "..OOOOO.."] }
    ];
    var INK = { R: PINK, G: GREEN, O: ORANGE, W: WHITE };
    function sprite(ctx, art, x, y, color, scale, flip) {
      var s = px * (scale || 1), n = art.length;
      for (var r = 0; r < n; r++) for (var c = 0; c < art[r].length; c++) {
        var ch = art[r][c];
        if (ch === ".") continue;
        ctx.fillStyle = color || rgba(INK[ch] || WHITE, 0.95);
        var cx = flip ? (art[r].length - 1 - c) : c;
        ctx.fillRect(x + cx * s, y + r * s, s, s);
      }
    }
    function ghostEyes(ctx, gx, gy, t, mood, scale) {
      var s = px * (scale || 1);
      var wonky = mood === "wonky", scared = mood === "scared";
      ctx.fillStyle = rgba(WHITE, 0.95);
      var lx = gx + 2 * s, rx = gx + 6 * s, ey = gy + 3 * s;
      if (wonky) { // eyes drift apart and bob out of sync
        lx += Math.round(Math.sin(t * 0.02) * 1.5) * s; rx += Math.round(Math.cos(t * 0.017) * 1.5) * s;
        ey += Math.round(Math.sin(t * 0.03)) * s;
        ctx.fillRect(lx, ey, s, s); ctx.fillRect(rx, ey - s, s, s);
        ctx.fillStyle = rgba(NIGHT, 1); ctx.fillRect(lx, ey, s * 0.6, s * 0.6); ctx.fillRect(rx + s * 0.4, ey - s + s * 0.4, s * 0.6, s * 0.6);
      } else if (scared) { // crossed, flickering
        var blink = Math.floor(t / 120) % 2 === 0;
        ctx.fillStyle = blink ? rgba(WHITE, 0.95) : rgba(PINK, 0.95);
        ctx.fillRect(lx + s, ey, s, s); ctx.fillRect(rx - s, ey, s, s);
        ctx.fillRect(lx, ey + 3 * s, s, s); ctx.fillRect(lx + 2 * s, ey + 3 * s, s, s); ctx.fillRect(rx, ey + 3 * s, s, s);
      } else {
        ctx.fillRect(lx, ey, s, s); ctx.fillRect(rx, ey, s, s);
        ctx.fillStyle = rgba(NIGHT, 1); ctx.fillRect(lx + s * 0.5, ey + s * 0.5, s * 0.5, s * 0.5); ctx.fillRect(rx + s * 0.5, ey + s * 0.5, s * 0.5, s * 0.5);
      }
    }
    function makeLane(y, ghost, story) {
      return { y: y, x: -120, v: 90, dots: [], ghostColor: ghost, story: story, phase: "chase", dir: 1, scale: 1,
               fruit: null, fruitIdx: 0, ghostX: -230, ghostMood: "normal", wonkyUntil: 0, nextWonky: 2000 + Math.random() * 4000, eyesY: 0 };
    }
    function reset(L, w) {
      L.x = -120; L.v = 90; L.dir = 1; L.scale = 1; L.phase = "chase"; L.ghostX = L.x - 110; L.ghostMood = "normal";
      for (var i = 0; i < L.dots.length; i++) L.dots[i] = true;
      if (L.story) { L.fruit = { x: w * (0.74 + Math.random() * 0.16), kind: FRUITS[L.fruitIdx % FRUITS.length] }; L.fruitIdx++; }
    }
    return function (ctx, w, h, t, dt) {
      var dotGap = 28, n = Math.ceil(w / dotGap) + 1, sec = dt / 1000;
      if (!lanes) { lanes = [makeLane(h * 0.14, CYAN, false), makeLane(h * 0.86, GREEN, true)]; }
      lanes.forEach(function (L) {
        if (L.dots.length !== n) { L.dots = []; for (var i = 0; i < n; i++) L.dots.push(true); reset(L, w); }

        // ghost mood: wonky now and then, scared while Pac-Man is powered up
        if (L.phase === "power") L.ghostMood = "scared";
        else if (L.phase === "eaten") L.ghostMood = "eyes";
        else { if (t > L.nextWonky) { L.wonkyUntil = t + 900; L.nextWonky = t + 2500 + Math.random() * 5000; } L.ghostMood = t < L.wonkyUntil ? "wonky" : "normal"; }

        // movement per phase
        if (L.phase === "chase") {
          L.x += L.v * sec; L.ghostX = L.x - 110 + Math.sin(t * 0.004) * 6;
          if (L.story && L.fruit && L.x + 45 >= L.fruit.x) { L.fruit = null; L.phase = "power"; L.scale = 1.6; L.dir = -1; L.v = 170; L.powerAt = t; }
          else if (L.x > w + 160) reset(L, w);
        } else if (L.phase === "power") {
          L.x -= L.v * sec; L.ghostX -= 70 * sec; // ghost flees left, slower than Pac-Man
          if (L.x <= L.ghostX + 20) { L.phase = "eaten"; L.eyesY = 0; }
        } else if (L.phase === "eaten") {
          L.x -= L.v * sec; L.eyesY -= 60 * sec; L.ghostX -= 140 * sec;
          if (L.x < -200) reset(L, w);
        }

        // dots (eaten from the left on the way out; the way back doesn't matter, they're gone)
        for (var i = 0; i < n; i++) {
          var dx = i * dotGap;
          if (L.phase === "chase" && dx < L.x + 20) L.dots[i] = false;
          if (L.dots[i]) { ctx.fillStyle = rgba(BLACK, 0.9); ctx.fillRect(dx, L.y - 3, 6, 6); }
        }
        if (L.fruit) sprite(ctx, L.fruit.kind.art, L.fruit.x, L.y - 22, null, 1, false);

        // ghost
        if (L.phase === "eaten") {
          ghostEyes(ctx, L.ghostX, L.y - 22 + L.eyesY, t, "normal", 1);
        } else {
          var gcol = L.ghostMood === "scared" ? (Math.floor(t / 160) % 2 ? rgba(BLUE, 0.85) : rgba(WHITE, 0.7)) : rgba(L.ghostColor, 0.8);
          sprite(ctx, GHOST, L.ghostX, L.y - 22, gcol, 1, false);
          ghostEyes(ctx, L.ghostX, L.y - 22, t, L.ghostMood, 1);
        }

        // Pac-Man (bigger and facing left while powered)
        var open = Math.floor(t / (L.phase === "chase" ? 140 : 90)) % 2 === 0;
        var size = 9 * px * L.scale;
        sprite(ctx, open ? PAC_OPEN : PAC_SHUT, L.x, L.y - size / 2, rgba(ORANGE, 0.95), L.scale, L.dir < 0);
      });

      var rnd = makeRng(77), cell = 12;
      var cols = Math.ceil(w / cell), rows = Math.ceil(h / cell);
      for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) {
        if (rnd() > 0.06) continue;
        ctx.fillStyle = rgba(BLACK, 0.3);
        ctx.fillRect(x * cell, y * cell, cell - 2, cell - 2);
      }
    };
  }

  function mount(cv) {
    if (!cv.getContext) return;
    var ctx = cv.getContext("2d");
    var mode = cv.dataset.mode;
    if (!mode || mode === "random") { var MODES = ["drift", "matrix", "pacman"]; mode = MODES[Math.floor(Math.random() * MODES.length)]; }
    cv.parentElement.setAttribute("data-mode", mode);
    var render = mode === "matrix" ? matrixFactory() : mode === "pacman" ? pacmanFactory() : drift;
    var w = 0, h = 0, dpr = 1, last = 0, running = false, visible = true, raf = 0;
    function size() {
      var host = cv.parentElement;
      w = host.clientWidth; h = host.clientHeight;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = w * dpr; cv.height = h * dpr; cv.style.width = w + "px"; cv.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function frame(now) {
      raf = 0;
      var dt = last ? Math.min(now - last, 50) : 16;
      last = now;
      ctx.clearRect(0, 0, w, h);
      render(ctx, w, h, now, dt);
      if (running && visible && !document.hidden) raf = requestAnimationFrame(frame);
    }
    function start() { if (reduce) { ctx.clearRect(0, 0, w, h); render(ctx, w, h, 0, 16); return; } running = true; if (!raf) raf = requestAnimationFrame(frame); }
    function stop() { running = false; }
    size(); start();
    var t; window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(function () { size(); if (reduce) start(); }, 120); });
    document.addEventListener("visibilitychange", function () { if (!document.hidden) start(); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); else stop(); }, { threshold: 0.05 }).observe(cv);
    }
  }
  document.querySelectorAll(".hero-pixels").forEach(mount);
})();
