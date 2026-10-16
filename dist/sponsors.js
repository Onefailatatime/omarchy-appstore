/* Fair sequential rotation for sponsor units (omarchyapps.com).
 *
 * Each [data-rotate] container holds every ACTIVE sponsor for one slot
 * (server-rendered by sponsors.py) and shows `visible` units at a time. The
 * window advances one position every INTERVAL_MS and wraps around, so
 * every sponsor gets exactly equal screen time — no randomness, no
 * bidding for position.
 *
 * Fairness details:
 * - The starting offset is (days since epoch) % n, so every visitor sees
 *   the same order on a given day, and nobody is permanently first or last.
 * - Without JS all units stay visible (nothing is hidden by default).
 * - prefers-reduced-motion users see a static set (the day's first `visible`).
 */
(function () {
  "use strict";
  var INTERVAL_MS = 10000;

  function unitsOf(box) {
    var out = [];
    for (var c = box.firstElementChild; c; c = c.nextElementSibling) {
      if (c.classList && c.classList.contains("ad")) out.push(c);
    }
    return out;
  }

  function paint(units, start, per) {
    for (var i = 0; i < units.length; i++) {
      var on = false;
      for (var k = 0; k < per; k++) {
        if ((start + k) % units.length === i) { on = true; break; }
      }
      units[i].style.display = on ? "" : "none";
    }
  }

  var reduceMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var boxes = document.querySelectorAll("[data-rotate]");
  for (var b = 0; b < boxes.length; b++) {
    (function (box) {
      var units = unitsOf(box);
      var per = parseInt(box.getAttribute("data-rotate"), 10) || 3;
      if (units.length <= per) return; // nothing to rotate
      var n = units.length;
      var idx = Math.floor(Date.now() / 86400000) % n; // daily seed
      paint(units, idx, per);
      if (reduceMotion) return;
      setInterval(function () {
        idx = (idx + 1) % n;
        paint(units, idx, per);
      }, INTERVAL_MS);
    })(boxes[b]);
  }
})();
