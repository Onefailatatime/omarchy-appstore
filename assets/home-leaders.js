(function () {
  "use strict";

  var podium = document.getElementById("home-leaders");
  var status = document.getElementById("home-leader-status");
  if (!podium || !status) return;

  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));

  function leaderCard(source, rank, count) {
    var article = document.createElement("article");
    article.className = "home-leader cat-" + source.dataset.cat;
    if (rank === 1) article.classList.add("home-leader-champion");

    var appLink = document.createElement("a");
    appLink.className = "home-leader-line";
    appLink.href = source.dataset.detailUrl;
    appLink.setAttribute("aria-label", "Rank " + rank + ": " + source.dataset.name + " with " + count + " upvotes");

    var rankEl = document.createElement("span");
    rankEl.className = "home-leader-rank";
    rankEl.textContent = "#" + rank;

    var name = document.createElement("strong");
    name.className = "home-leader-name";
    name.textContent = source.dataset.name;

    var score = document.createElement("span");
    score.className = "home-leader-score";
    score.textContent = "▲ " + count;
    score.setAttribute("aria-hidden", "true");

    appLink.appendChild(rankEl);
    appLink.appendChild(name);
    appLink.appendChild(score);
    article.appendChild(appLink);
    return article;
  }

  function render(counts) {
    var ranked = cards.slice().sort(function (a, b) {
      var countA = counts[a.dataset.name] || 0;
      var countB = counts[b.dataset.name] || 0;
      return countB - countA || a.dataset.name.localeCompare(b.dataset.name);
    }).slice(0, 3);
    var fragment = document.createDocumentFragment();
    ranked.forEach(function (card, index) {
      fragment.appendChild(leaderCard(card, index + 1, counts[card.dataset.name] || 0));
    });
    podium.replaceChildren(fragment);
    podium.hidden = false;
    status.textContent = "Live community rankings · updates with every vote";
  }

  window.addEventListener("omarchy:votes", function (event) {
    render(event.detail.counts || {});
  });
  window.addEventListener("omarchy:votes-error", function () {
    render({});
    status.textContent = "Live totals are temporarily unavailable · showing apps A–Z";
  });
  if (window.omarchyVotes) {
    var current = window.omarchyVotes.snapshot();
    if (current.ready) render(current.counts);
  }
})();
