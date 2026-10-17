/* RiTa homepage — progressive enhancement only.
   The page is fully usable without this file: anchors, <details> and
   smooth-scrolling are all native. This handles the mobile nav toggle. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (!toggle || !nav) return;

  var setOpen = function (open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  };

  toggle.addEventListener("click", function () {
    setOpen(!nav.classList.contains("is-open"));
  });

  // close the menu after choosing a destination
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setOpen(false);
  });

  // reset state if the viewport grows past the mobile breakpoint
  window.addEventListener("resize", function () {
    if (window.innerWidth > 640) setOpen(false);
  });

  // a link (or deep link) to a collapsed <details> should reveal its content
  var reveal = function () {
    var id = decodeURIComponent((location.hash || "").slice(1));
    if (!id) return;
    var target = document.getElementById(id);
    var details = target && target.closest
      ? (target.matches("details") ? target : target.querySelector("details"))
      : null;
    if (details) details.open = true;
  };

  document.addEventListener("click", function (e) {
    var link = e.target.closest && e.target.closest('a[href^="#"]');
    if (link) reveal();
  });

  window.addEventListener("hashchange", reveal);

  // RiScript is a grammar extension, so group it under RiGrammar rather than
  // giving it its own column. docgen emits the classes in RiTa/RiGrammar/
  // RiMarkov/RiScript order, so this is a simple append.
  var api = document.querySelector(".api");
  if (api) {
    var sections = [].slice.call(api.children);
    var grammar = sections.filter(function (s) {
      var b = s.querySelector("b");
      return b && b.textContent.trim() === "RiGrammar";
    })[0];
    var script = sections.filter(function (s) {
      var b = s.querySelector("b");
      return b && b.textContent.trim() === "RiScript";
    })[0];
    if (grammar && script && grammar !== script) grammar.appendChild(script);
  }

  reveal();
  setOpen(false);
})();
