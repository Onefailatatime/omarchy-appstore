(function () {
  "use strict";
  var q = document.getElementById("q");
  var cards = Array.prototype.slice.call(document.querySelectorAll("#catalogue .card"));
  var groups = Array.prototype.slice.call(document.querySelectorAll("#catalogue .group"));
  var shown = document.getElementById("shown");
  var empty = document.getElementById("empty");
  var emptyQ = document.getElementById("empty-q");
  var catalogue = document.getElementById("catalogue");
  var dlg = document.getElementById("detail");
  var activeCat = "";
  var catalogPromise = null;
  var catalogLoaded = false;
  var dmRecipient = document.body.getAttribute("data-x-dm-recipient") || "";

  function hayFor(c) { return (c.dataset.name + " " + c.dataset.desc).toLowerCase(); }
  cards.forEach(function (c) { c._hay = hayFor(c); });

  // Rankings, arrivals and guides sit between the search box and the catalogue.
  // Hide them while a query or category is active so results land right under
  // the box instead of 2,000px further down, where typing looked like a no-op.
  var browseOnly = Array.prototype.slice.call(document.querySelectorAll("[data-browse-only]"));
  var categoryBrowser = document.querySelector(".category-browser");
  // Guides are searchable too, so an app we cover but the repo lacks (or a
  // topic like "notion alternative") still answers the query.
  var guideResults = document.getElementById("guide-results");
  var guideLinks = Array.prototype.slice.call(guideResults.querySelectorAll("a"));
  guideLinks.forEach(function (a) { a._hay = (a.dataset.hay || "").toLowerCase(); });

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderCard(p) {
    var name = esc(p.name);
    var cls = "card cat-" + esc(p.cat);
    if (p.indieNote) cls += " indie-app";
    var sticker = p.indieNote
      ? '  <span class="indie-sticker card-sticker" title="' + esc(p.indieNote) + '">Indie app</span>\n'
      : "";
    var byline = (p.authorName && p.authorUrl)
      ? '<p class="byline">by <a href="' + esc(p.authorUrl) + '" target="_blank" rel="author noopener">' + esc(p.authorName) + "</a></p>"
      : "";
    var desc = p.desc ? esc(p.desc) : "<em>No description provided.</em>";
    var detail = esc(p.detailUrl);
    var shareUrl = "https://omarchyapps.com/" + (p.detailUrl || "");
    var share = '<a class="app-share" href="' + esc(shareUrl) + '" data-share-app="' + name
      + '" data-share-title="' + name + ' for Omarchy" data-share-url="' + esc(shareUrl)
      + '" aria-label="Share ' + name + '">share</a>';
    var vote = '<button class="app-vote" type="button" data-vote-app="' + name
      + '" aria-pressed="false" aria-label="Upvote ' + name
      + '"><span aria-hidden="true">▲</span> <span data-vote-count>0</span></button>';
    var html = '<article class="' + cls + '" data-detail-url="' + detail + '"\n'
      + '  data-name="' + name + '" data-dir="' + esc(p.dir) + '" data-version="' + esc(p.version) + '" data-desc="' + esc(p.desc) + '"\n'
      + '  data-url="' + esc(p.url) + '" data-github="' + esc(p.github) + '" data-license="' + esc(p.license) + '" data-csize="' + esc(p.csize) + '" data-isize="' + esc(p.isize) + '"\n'
      + '  data-built="' + esc(p.built) + '" data-built-ts="' + esc(p.builtTs) + '" data-added="' + esc(p.added) + '" data-added-ts="' + esc(p.addedTs) + '"\n'
      + '  data-category="' + esc(p.category) + '" data-cat="' + esc(p.cat) + '" data-pricing="' + esc(p.pricing) + '"\n'
      + '  data-yt="' + esc(p.youtubeId) + '" data-yt-title="' + esc(p.youtubeTitle) + '">\n'
      + '  <header><h3><a href="' + detail + '">' + name + '</a></h3><span class="ver">' + esc(p.version) + "</span></header>\n"
      + sticker + "  " + byline + "\n"
      + '  <p class="card-description">' + desc + "</p>\n"
      + '  <footer><span class="card-facts"><span class="cat-dot" aria-hidden="true"></span><span class="size">'
      + esc(p.csize) + '</span></span><span class="card-actions">' + share + vote + "</span></footer>\n"
      + "</article>";
    var wrap = document.createElement("div");
    wrap.innerHTML = html.trim();
    return wrap.firstElementChild;
  }

  function wireCard(c) {
    c._hay = hayFor(c);
  }

  function loadCatalog() {
    if (!catalogPromise) {
      catalogPromise = fetch("/home-catalog.json")
        .then(function (r) { return r.ok ? r.json() : { groups: {} }; })
        .then(function (data) {
          var rest = (data && data.groups) || {};
          groups.forEach(function (g) {
            var list = rest[g.dataset.cat];
            if (!list || !list.length) return;
            var grid = g.querySelector(".grid");
            var frag = document.createDocumentFragment();
            list.forEach(function (p) {
              var card = renderCard(p);
              wireCard(card);
              frag.appendChild(card);
            });
            grid.appendChild(frag);
          });
          cards = Array.prototype.slice.call(document.querySelectorAll("#catalogue .card"));
          catalogLoaded = true;
          if (window.omarchyVotes && typeof window.omarchyVotes.refresh === "function") {
            window.omarchyVotes.refresh();
          }
          apply();
          return data;
        })
        .catch(function () {
          catalogPromise = null;
          return { groups: {} };
        });
    }
    return catalogPromise;
  }

  function apply() {
    var terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    var n = 0;
    var browsing = terms.length === 0 && !activeCat;
    browseOnly.forEach(function (el) { el.hidden = !browsing; });
    // The category chips stay while a category filter is active (they show the
    // state) but get out of the way of a typed query.
    categoryBrowser.hidden = terms.length > 0;
    groups.forEach(function (g) {
      g.classList.toggle("collapsed", browsing && g.dataset.preview && !g.dataset.opened);
      var catOk = !activeCat || g.dataset.cat === activeCat;
      var visibleInGroup = 0;
      if (catOk) {
        Array.prototype.forEach.call(g.querySelectorAll(".card"), function (c) {
          var hit = terms.every(function (t) { return c._hay.indexOf(t) !== -1; });
          c.hidden = !hit;
          if (hit) { visibleInGroup++; n++; }
        });
      }
      g.hidden = !catOk || visibleInGroup === 0;
    });
    shown.textContent = n;
    var hasQuery = terms.length > 0;
    var guideHits = 0;
    guideLinks.forEach(function (a) {
      var hit = hasQuery && terms.every(function (t) { return a._hay.indexOf(t) !== -1; });
      a.hidden = !hit;
      if (hit) guideHits++;
    });
    guideResults.hidden = guideHits === 0;
    empty.classList.toggle("on", n === 0 && guideHits === 0);
    catalogue.hidden = n === 0;
    if (n === 0) {
      emptyQ.textContent = hasQuery ? '"' + q.value.trim() + '"' : "that category";
    }
    if (!catalogLoaded && (hasQuery || activeCat)) loadCatalog();
  }
  q.addEventListener("input", apply);

  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== q && !dlg.open) { e.preventDefault(); q.focus(); }
    if (e.key === "Escape" && document.activeElement === q) { q.value = ""; apply(); q.blur(); }
  });

  document.querySelectorAll("[data-group-more]").forEach(function (button) {
    button.addEventListener("click", function () {
      var g = button.closest(".group");
      function openGroup() {
        g.dataset.opened = "1";
        g.classList.remove("collapsed");
        button.setAttribute("aria-expanded", "true");
      }
      if (catalogLoaded) openGroup();
      else loadCatalog().then(openGroup);
    });
  });

  /* ---------- sort (within each visible group) ---------- */
  var sortChips = document.querySelectorAll(".chip.sort");
  sortChips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      sortChips.forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      var mode = chip.dataset.sort;
      var finish = function () {
        groups.forEach(function (g) {
          var list = Array.prototype.slice.call(g.querySelectorAll(".card"));
          list.sort(function (a, b) {
            if (mode === "new") { return (+b.dataset.builtTs) - (+a.dataset.builtTs); }
            return a.dataset.name.localeCompare(b.dataset.name);
          });
          var grid = g.querySelector(".grid");
          list.forEach(function (c) { grid.appendChild(c); });
        });
      };
      if (catalogLoaded) finish();
      else loadCatalog().then(finish);
    });
  });

  /* ---------- category chips ---------- */
  var catChips = document.querySelectorAll(".chip[data-cat]");
  var filterActive = document.getElementById("filter-active");
  var filterName = document.getElementById("filter-name");
  var filterClear = document.getElementById("filter-clear");

  function setCategory(cat, chip) {
    activeCat = cat;
    catChips.forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
    if (cat) {
      filterActive.classList.add("on");
      filterActive.style.setProperty("--cat", getComputedStyle(chip).getPropertyValue("--cat"));
      filterName.textContent = chip.textContent.replace(/\s*\d+\s*$/, "").trim();
    } else {
      filterActive.classList.remove("on");
    }
    apply();
  }
  catChips.forEach(function (chip) {
    chip.addEventListener("click", function () { setCategory(chip.dataset.cat, chip); });
  });
  filterClear.addEventListener("click", function () { setCategory("", catChips[0]); });

  /* ---------- detail dialog ---------- */
  var PRICING_LABEL = {
    "free": "Free", "free-libre": "Free & open source", "freemium": "Freemium",
    "paid": "Paid", "subscription": "Subscription",
  };
  function text(id, v) { document.getElementById(id).textContent = v; }
  // Drawer-only fields (full description, deps, gallery...) live in one JSON
  // file fetched on the first click, so the catalogue HTML stays light.
  var detailsPromise = null;
  function loadDetails() {
    if (!detailsPromise) {
      detailsPromise = fetch("/package-details.json")
        .then(function (r) { return r.ok ? r.json() : {}; })
        .catch(function () { return {}; });
    }
    return detailsPromise;
  }
  function fillDetails(d, x) {
    var taglineEl = document.getElementById("d-tagline");
    taglineEl.hidden = !x.tagline;
    if (x.tagline) text("d-tagline", x.tagline);

    var galleryWrap = document.getElementById("d-gallery-wrap");
    var gallery = document.getElementById("d-gallery");
    var gallerySource = document.getElementById("d-gallery-source");
    var images = (x.gallery || []);
    gallery.textContent = "";
    images.forEach(function (image) {
      var link = document.createElement("a");
      link.className = "shot-wrap";
      link.href = image.url;
      link.target = "_blank";
      link.rel = "noopener";
      link.setAttribute("aria-label", "Open full-size " + (image.alt || d.name + " screenshot"));
      var shot = document.createElement("img");
      shot.src = image.url;
      shot.alt = image.alt || (d.name + " screenshot");
      shot.loading = "lazy";
      shot.decoding = "async";
      shot.referrerPolicy = "no-referrer";
      link.appendChild(shot);
      gallery.appendChild(link);
    });
    gallerySource.textContent = "";
    var sourceImage = images.find(function (image) { return image.source_url; });
    if (sourceImage) {
      gallerySource.appendChild(document.createTextNode("Loaded from the upstream project · "));
      var sourceLink = document.createElement("a");
      sourceLink.href = sourceImage.source_url;
      sourceLink.target = "_blank";
      sourceLink.rel = "noopener";
      sourceLink.textContent = "View upstream source ↗";
      gallerySource.appendChild(sourceLink);
    }
    galleryWrap.hidden = images.length === 0;

    text("d-desc", x.full_desc || d.desc || "No description provided.");

    var pricingEl = document.getElementById("d-pricing");
    if (d.pricing && PRICING_LABEL[d.pricing]) {
      pricingEl.textContent = PRICING_LABEL[d.pricing] + (x.pricing_note ? " · " + x.pricing_note : "");
      pricingEl.className = "badge pricing p-" + d.pricing;
      pricingEl.hidden = false;
    } else {
      pricingEl.hidden = true;
    }
    var indieEl = document.getElementById("d-indie");
    indieEl.hidden = !x.indie_note;
    indieEl.title = x.indie_note || "";
    var reqs = (x.reqs || []);
    var reqsWrap = document.getElementById("d-reqs-wrap");
    var reqsList = document.getElementById("d-reqs");
    reqsList.textContent = "";
    reqs.forEach(function (r) { var li = document.createElement("li"); li.textContent = r; reqsList.appendChild(li); });
    reqsWrap.hidden = reqs.length === 0;

    var deps = (x.deps || []);
    var wrap = document.getElementById("d-deps-wrap");
    var list = document.getElementById("d-deps");
    list.textContent = "";
    deps.forEach(function (name) { var s = document.createElement("span"); s.textContent = name; list.appendChild(s); });
    wrap.hidden = deps.length === 0;
  }
  function open(c) {
    var d = c.dataset;
    text("d-name", d.name);
    text("d-ver", d.version);
    text("d-cat-name", d.category);
    document.getElementById("d-cat").style.setProperty("--cat", getComputedStyle(c).getPropertyValue("--cat"));

    var appVote = document.getElementById("d-vote");
    appVote.dataset.voteApp = d.name;
    if (window.omarchyVotes) window.omarchyVotes.refresh(appVote);

    fillDetails(d, {});
    loadDetails().then(function (all) { if (document.getElementById("d-name").textContent === d.name) fillDetails(d, all[d.name] || {}); });

    text("d-cmd", "omarchy pkg add " + d.name);
    text("d-csize", d.csize);
    text("d-isize", d.isize);
    text("d-license", d.license);
    text("d-built", d.built);
    var addedWrap = document.getElementById("d-added-wrap");
    if (d.added) { text("d-added", d.added); addedWrap.hidden = false; } else { addedWrap.hidden = true; }
    /* Click-to-play: nothing is fetched from YouTube until this button is
       pressed, so opening a dialog never makes a third-party request. */
    var videoWrap = document.getElementById("d-video-wrap");
    var videoSlot = document.getElementById("d-video-slot");
    videoSlot.textContent = "";
    if (d.yt) {
      var playBtn = document.createElement("button");
      playBtn.type = "button";
      playBtn.className = "video-ph";
      playBtn.setAttribute("aria-label", "Play demo video");
      var icon = document.createElement("span");
      icon.className = "play-icon";
      icon.setAttribute("aria-hidden", "true");
      icon.textContent = "▶";
      var label = document.createElement("span");
      label.textContent = d.ytTitle ? "Watch: " + d.ytTitle : "Watch demo";
      playBtn.appendChild(icon);
      playBtn.appendChild(label);
      playBtn.addEventListener("click", function () {
        var iframe = document.createElement("iframe");
        iframe.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(d.yt) + "?autoplay=1";
        iframe.title = d.ytTitle || (d.name + " demo video");
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.referrerPolicy = "strict-origin-when-cross-origin";
        iframe.style.cssText = "width:100%;aspect-ratio:16/9;border:0;border-radius:var(--radius);display:block";
        videoSlot.textContent = "";
        videoSlot.appendChild(iframe);
      });
      videoSlot.appendChild(playBtn);
      videoWrap.hidden = false;
    } else {
      videoWrap.hidden = true;
    }

    var url = document.getElementById("d-url");
    url.href = d.url || "#";
    url.hidden = !d.url;
    var gh = document.getElementById("d-github");
    gh.href = d.github || "#";
    gh.hidden = !d.github;
    document.getElementById("d-src").href = "https://github.com/omacom/omarchy-pkgs/tree/master/pkgbuilds/" + encodeURIComponent(d.dir || d.name);
    var share = document.getElementById("d-share");
    share.href = new URL(c.dataset.detailUrl, window.location.href).href;
    share.dataset.shareUrl = share.href;
    share.dataset.shareApp = d.name;
    share.dataset.shareTitle = d.name + " for Omarchy";
    var claimText =
      "Hi! I'd like to claim the " + d.name + " listing on the Unofficial Omarchy App Store.\n\n" +
      "I can provide:\n- a correction or edit\n- screenshots of the app\n- a demo video\n\n" +
      "Project URL: \nMy role with the app: ";
    document.getElementById("d-claim").href =
      "https://x.com/messages/compose?recipient_id=" + encodeURIComponent(dmRecipient) + "&text=" + encodeURIComponent(claimText);
    dlg.showModal();
  }
  document.addEventListener("click", function (e) {
    var c = e.target.closest(".card");
    if (!c || !catalogue.contains(c) && !c.closest("[data-browse-only]")) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button === 1) return;
    if (e.target.closest(".byline a, .app-share, .app-vote")) return;
    e.preventDefault();
    open(c);
  });
  dlg.querySelector("[data-close]").addEventListener("click", function () { dlg.close(); });
  dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  // Covers every close path (button, backdrop click, native Esc) in one place:
  // destroy any playing embed so it doesn't keep playing behind a closed dialog.
  dlg.addEventListener("close", function () { document.getElementById("d-video-slot").textContent = ""; });

  /* ---------- copy ---------- */
  var copy = document.getElementById("d-copy");
  copy.addEventListener("click", function () {
    var cmd = document.getElementById("d-cmd").textContent;
    var done = function () {
      copy.textContent = "Copied";
      setTimeout(function () { copy.textContent = "Copy"; }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(cmd).then(done, function () { copy.textContent = "Select it"; });
    } else {
      copy.textContent = "Select it";
    }
  });

  // Fetch the rest of the catalogue after first paint so search, sort and
  // "Show all" have every package without shipping them in the HTML.
  if (window.requestIdleCallback) requestIdleCallback(function () { loadCatalog(); }, { timeout: 2000 });
  else window.addEventListener("load", function () { loadCatalog(); });
})();
