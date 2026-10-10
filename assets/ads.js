(function () {
  "use strict";

  var meta = document.querySelector('meta[name="omarchy-auction"]');
  var base = meta ? meta.content.replace(/\/$/, "") : "";
  if (!base) return;

  function money(n) { return "$" + Number(n).toLocaleString("en-US"); }
  function left(sec) {
    if (sec == null) return "";
    var d = Math.floor(sec / 86400), h = Math.floor(sec % 86400 / 3600), m = Math.floor(sec % 3600 / 60);
    if (d) return d + "d " + h + "h left";
    if (h) return h + "h " + m + "m left";
    return m + "m left";
  }
  function strong(text) { var b = document.createElement("b"); b.textContent = text; return b; }
  function fill(el, parts) {
    el.textContent = "";
    parts.forEach(function (p, i) {
      if (i) el.appendChild(document.createTextNode(" · "));
      el.appendChild(typeof p === "string" ? document.createTextNode(p) : p);
    });
  }

  var slots = {};
  var fetchedAt = 0;

  function render() {
    var elapsed = Math.round((Date.now() - fetchedAt) / 1000);
    Object.keys(slots).forEach(function (id) {
      var s = slots[id];
      var secs = s.seconds_left == null ? null : Math.max(0, s.seconds_left - elapsed);
      var unit = s.per_month ? " per month" : "";

      document.querySelectorAll('.slot[data-slot="' + id + '"] [data-slot-status]').forEach(function (el) {
        var parts = [];
        if (s.status === "closed") parts.push("This round has closed");
        else {
          parts.push(s.high_bid == null ? "No bids yet" : strong("Current high bid " + money(s.high_bid) + unit));
          if (s.units > 1 && s.low_winning_bid != null) parts.push("lowest winning bid " + money(s.low_winning_bid) + unit);
          if (s.status === "live") parts.push(strong(left(secs)) );
          else parts.push("the " + s.auction_days + " day clock starts at the first approved bid");
          if (s.extensions) parts.push("extended " + s.extensions + "x");
        }
        fill(el, parts);
      });
      document.querySelectorAll('[data-bid][data-slot="' + id + '"] [data-bid-amount]').forEach(function (input) {
        if (s.minimum_bid != null) { input.min = s.minimum_bid; input.placeholder = s.minimum_bid; }
      });
      document.querySelectorAll('.ad[data-slot="' + id + '"] [data-ad-sub]').forEach(function (el) {
        var text;
        if (id === "lifetime") {
          text = "One sponsor, forever, always right here. " + (s.high_bid == null ? "Reserve " + money(s.reserve) + " · no bids yet" : "Current high bid " + money(s.high_bid));
          if (s.status === "live") text += " · " + left(secs);
          text += ".";
        } else {
          text = (s.high_bid == null ? "from " + money(s.reserve) + "/mo" : "high bid " + money(s.high_bid) + "/mo") + " · " + s.term_days + " day term";
          text += s.status === "live" ? " · " + left(secs) : " · billed " + money(Math.round(s.reserve * s.term_days / 30));
        }
        el.textContent = text;
      });
    });
  }

  function load() {
    fetch(base + "/api/state", { headers: { Accept: "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error("state"); return r.json(); })
      .then(function (data) { slots = data.slots || {}; fetchedAt = Date.now(); window.omarchyAuctionMode = data.mode; render(); })
      .catch(function () {});
  }

  var notices = {
    verified: "Your bid is confirmed. It shows on the board once it is checked, usually within a day.",
    already: "That bid was already confirmed.",
    invalid: "That confirmation link is not valid any more. Place the bid again if you still want it.",
  };
  var flag = new URLSearchParams(location.search).get("bid");
  var notice = document.querySelector("[data-bid-notice]");
  if (flag && notice && notices[flag]) { notice.textContent = notices[flag]; notice.hidden = false; }

  document.querySelectorAll("form[data-bid]").forEach(function (form) {
    var status = form.querySelector("[data-bid-status]");
    var button = form.querySelector("button");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var f = form.elements;
      var body = {
        slot: form.dataset.slot,
        amount: Number(f.amount.value),
        name: f.name.value,
        url: f.url.value,
        tagline: f.tagline.value,
        email: f.email.value,
        agree: f.agree.checked,
        website: f.website.value,
      };
      button.disabled = true;
      status.textContent = "Sending your bid…";
      fetch(base + "/api/bid", {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(body),
      })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
        .then(function (result) {
          if (!result.ok) throw new Error(result.data.error || "Could not place the bid.");
          form.classList.add("is-done");
          status.textContent = result.data.state === "verify"
            ? "Check your inbox and click the link to confirm your bid. It counts once confirmed and checked."
            : "Bid received. It shows on the board once it is checked, usually within a day. You will hear by email if you win.";
          load();
        })
        .catch(function (error) {
          button.disabled = false;
          status.textContent = error.message || "Could not place the bid. Please try again.";
        });
    });
  });

  load();
  setInterval(render, 60000);
  setInterval(load, 5 * 60000);
})();
