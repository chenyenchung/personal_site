(function () {
  document.documentElement.classList.add("has-js");

  const breakpoint = window.matchMedia("(max-width: 820px)");
  const button = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-site-menu]");

  if (!button || !menu) {
    return;
  }

  function setExpanded(expanded) {
    button.setAttribute("aria-expanded", String(expanded));
    if (breakpoint.matches) {
      menu.hidden = !expanded;
    } else {
      menu.hidden = false;
    }
  }

  function syncForViewport() {
    setExpanded(!breakpoint.matches);
  }

  button.addEventListener("click", function () {
    const expanded = button.getAttribute("aria-expanded") === "true";
    setExpanded(!expanded);
  });

  menu.addEventListener("click", function (event) {
    if (breakpoint.matches && event.target.closest(".site-nav a")) {
      setExpanded(false);
    }
  });

  document.addEventListener("keydown", function (event) {
    const expanded = button.getAttribute("aria-expanded") === "true";
    if (event.key === "Escape" && breakpoint.matches && expanded) {
      setExpanded(false);
      button.focus();
    }
  });

  if (typeof breakpoint.addEventListener === "function") {
    breakpoint.addEventListener("change", syncForViewport);
  } else if (typeof breakpoint.addListener === "function") {
    breakpoint.addListener(syncForViewport);
  }

  syncForViewport();
})();
