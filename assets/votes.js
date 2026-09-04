(function () {
  "use strict";

  var state = { counts: {}, voted: new Set(), ready: false };

  function buttonsFor(app) {
    return Array.prototype.filter.call(document.querySelectorAll("[data-vote-app]"), function (button) {
      return button.dataset.voteApp === app;
    });
  }

  function render(button) {
    var app = button.dataset.voteApp;
    if (!app) return;
    var count = state.counts[app] || 0;
    var countEl = button.querySelector("[data-vote-count]");
    if (countEl) countEl.textContent = count;
    var didVote = state.voted.has(app);
    button.classList.toggle("is-voted", didVote);
    button.setAttribute("aria-pressed", didVote ? "true" : "false");
    button.setAttribute("aria-label", didVote ? "You upvoted " + app : "Upvote " + app);
    button.title = didVote ? "Your upvote is saved on the site" : "Upvote this app";
  }

  function renderAll() {
    document.querySelectorAll("[data-vote-app]").forEach(render);
  }

  function loadVotes() {
    return fetch("/api/votes", { credentials: "same-origin", headers: { "Accept": "application/json" } })
      .then(function (response) { if (!response.ok) throw new Error("votes unavailable"); return response.json(); })
      .then(function (data) {
        state.counts = data.counts || {};
        state.voted = new Set(data.voted || []);
        state.ready = true;
        renderAll();
      })
      .catch(function () {
        document.querySelectorAll("[data-vote-app]").forEach(function (button) {
          button.classList.add("vote-unavailable");
          button.title = "Upvotes are temporarily unavailable";
        });
      });
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-vote-app]");
    if (!button) return;
    event.preventDefault();
    event.stopPropagation();
    var app = button.dataset.voteApp;
    if (!app || !state.ready || state.voted.has(app) || button.getAttribute("aria-busy") === "true") return;
    buttonsFor(app).forEach(function (item) { item.setAttribute("aria-busy", "true"); });
    fetch("/api/votes", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({ app: app }),
    })
      .then(function (response) { if (!response.ok) throw new Error("vote not saved"); return response.json(); })
      .then(function (data) {
        state.counts[app] = data.count;
        state.voted.add(app);
        buttonsFor(app).forEach(function (item) { item.removeAttribute("aria-busy"); render(item); });
      })
      .catch(function () {
        buttonsFor(app).forEach(function (item) {
          item.removeAttribute("aria-busy");
          item.classList.add("vote-error");
          item.title = "Could not save this upvote. Please try again.";
        });
      });
  }, true);

  window.omarchyVotes = { refresh: render, reload: loadVotes };
  loadVotes();
})();
