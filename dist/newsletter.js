(function () {
  "use strict";

  var messages = {
    subscribed: "Sent! Check your inbox for the checklist.",
    existing: "You're already on the list. Check your inbox for the checklist.",
  };

  document.querySelectorAll("[data-newsletter]").forEach(function (form) {
    var status = form.querySelector("[data-newsletter-status]");
    var button = form.querySelector("button");

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var email = form.elements.email.value.trim();
      if (!email) return;
      button.disabled = true;
      status.textContent = "Sending…";
      fetch(form.action, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, website: form.elements.website.value }),
      })
        .then(function (response) { return response.json().then(function (data) { return { ok: response.ok, data: data }; }); })
        .then(function (result) {
          if (!result.ok) throw new Error(result.data.error || "Signup failed");
          form.classList.add("is-done");
          status.textContent = messages[result.data.status] || messages.subscribed;
        })
        .catch(function (error) {
          button.disabled = false;
          status.textContent = error.message || "Could not sign you up. Please try again.";
        });
    });
  });
})();
