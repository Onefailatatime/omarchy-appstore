(function () {
  "use strict";

  var podium = document.getElementById("leader-podium");
  var list = document.getElementById("leader-list");
  var status = document.getElementById("leader-status");
  if (!podium || !list) return;

  var rows = Array.prototype.slice.call(list.querySelectorAll("[data-leader-app]"));

  function render(counts) {
    rows.sort(function (a, b) {
      var countA = counts[a.dataset.leaderApp] || 0;
      var countB = counts[b.dataset.leaderApp] || 0;
      return countB - countA || a.dataset.leaderApp.localeCompare(b.dataset.leaderApp);
    });

    var podiumFragment = document.createDocumentFragment();
    var listFragment = document.createDocumentFragment();
    rows.forEach(function (row, index) {
      var rank = index + 1;
      row.querySelector("[data-leader-rank]").textContent = "#" + rank;
      row.classList.toggle("leader-winner", rank <= 3);
      row.classList.toggle("leader-champion", rank === 1);
      row.hidden = rank > 25;
      if (rank <= 3) podiumFragment.appendChild(row);
      else listFragment.appendChild(row);
    });
    podium.replaceChildren(podiumFragment);
    list.replaceChildren(listFragment);
    podium.hidden = false;
    status.textContent = "Live community rankings · ties are sorted A–Z";
  }

  window.addEventListener("omarchy:votes", function (event) {
    render(event.detail.counts || {});
  });
  window.addEventListener("omarchy:votes-error", function () {
    render({});
    status.textContent = "Live vote totals are temporarily unavailable · showing apps A–Z";
  });
})();
