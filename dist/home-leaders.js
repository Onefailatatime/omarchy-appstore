(function () {
  "use strict";

  var podium = document.getElementById("home-leaders");
  var status = document.getElementById("home-leader-status");
  if (!podium || !status) return;

  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));

  function leaderCard(source, rank, count) {
    var article = document.createElement("article");
    article.className = "leader-row leader-winner cat-" + source.dataset.cat;
    if (rank === 1) article.classList.add("leader-champion");

    var rankEl = document.createElement("span");
    rankEl.className = "leader-rank";
    rankEl.textContent = "#" + rank;
    rankEl.setAttribute("aria-label", "Rank " + rank);

    var copy = document.createElement("div");
    copy.className = "leader-copy";
    var heading = document.createElement("h3");
    var appLink = document.createElement("a");
    appLink.href = source.dataset.detailUrl;
    appLink.textContent = source.dataset.name;
    heading.appendChild(appLink);
    var description = document.createElement("p");
    description.textContent = source.querySelector(".card-description").textContent.trim();

    var meta = document.createElement("div");
    meta.className = "leader-meta";
    var category = document.createElement("span");
    category.className = "leader-category";
    var dot = document.createElement("span");
    dot.className = "dot";
    dot.setAttribute("aria-hidden", "true");
    category.appendChild(dot);
    category.appendChild(document.createTextNode(source.dataset.category));
    meta.appendChild(category);

    var authorLink = source.querySelector(".byline a");
    if (authorLink) {
      var author = document.createElement("span");
      author.className = "leader-author";
      author.appendChild(document.createTextNode("by "));
      author.appendChild(authorLink.cloneNode(true));
      meta.appendChild(author);
    }
    var indie = source.querySelector(".indie-sticker");
    if (indie) meta.appendChild(indie.cloneNode(true));

    copy.appendChild(heading);
    copy.appendChild(description);
    copy.appendChild(meta);

    var score = document.createElement("span");
    score.className = "home-leader-score";
    score.innerHTML = '<span aria-hidden="true">▲</span> <b>' + count + '</b> <span class="score-label">upvotes</span>';

    article.appendChild(rankEl);
    article.appendChild(copy);
    article.appendChild(score);
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
