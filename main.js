/* Portfolio — subtle reveal-on-scroll. Progressive enhancement.
   Content is fully visible without JS; this only adds an entrance animation.
   Honors prefers-reduced-motion. */
(function () {
  "use strict";

  var docEl = document.documentElement;
  var revealables = document.querySelectorAll(".reveal");
  if (!revealables.length) return;

  var reduce =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // No observer support, or reduced motion: leave everything visible, no animation.
  if (reduce || !("IntersectionObserver" in window)) {
    return; // .reveal stays visible because .js-reveal is never added
  }

  // Opt into the hidden-then-revealed treatment only now that we can observe.
  docEl.classList.add("js-reveal");

  var io = new IntersectionObserver(
    function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
  );

  revealables.forEach(function (el) {
    io.observe(el);
  });

  // Safety net: if anything is still hidden a moment after load
  // (e.g. observer never fired in an odd embedding), reveal it.
  window.addEventListener("load", function () {
    setTimeout(function () {
      revealables.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && !el.classList.contains("is-in")) {
          el.classList.add("is-in");
          io.unobserve(el);
        }
      });
    }, 200);
  });
})();
