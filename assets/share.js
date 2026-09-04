(function () {
  "use strict";

  function copyText(value) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(value);
    }
    return new Promise(function (resolve, reject) {
      var input = document.createElement("textarea");
      input.value = value;
      input.setAttribute("readonly", "");
      input.style.position = "fixed";
      input.style.opacity = "0";
      document.body.appendChild(input);
      input.select();
      try {
        if (!document.execCommand("copy")) throw new Error("copy failed");
        resolve();
      } catch (error) {
        reject(error);
      } finally {
        input.remove();
      }
    });
  }

  function feedback(trigger, label) {
    var original = trigger.dataset.shareLabel || trigger.textContent;
    trigger.dataset.shareLabel = original;
    trigger.textContent = label;
    window.setTimeout(function () { trigger.textContent = original; }, 1800);
  }

  document.addEventListener("click", function (event) {
    var trigger = event.target.closest("[data-share-app]");
    if (!trigger) return;
    event.preventDefault();
    event.stopPropagation();

    var url = new URL(trigger.dataset.shareUrl || trigger.href || window.location.href, document.baseURI).href;
    var app = trigger.dataset.shareApp;
    var title = trigger.dataset.shareTitle || app + " for Omarchy";
    var payload = {
      title: title,
      text: "Check out " + app + " on the Unofficial Omarchy App Store.",
      url: url,
    };

    var nativeShare = navigator.share ? navigator.share(payload) : Promise.reject(new Error("share unavailable"));
    nativeShare.catch(function (error) {
      if (error && error.name === "AbortError") return;
      copyText(url).then(function () {
        feedback(trigger, "Copied!");
      }).catch(function () {
        window.prompt("Copy this app link:", url);
      });
    });
  }, true);
})();
