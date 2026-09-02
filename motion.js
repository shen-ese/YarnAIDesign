/* ============================================================
   YarnAI — motion
   Three behaviours, all of which Webflow Interactions can do
   natively. This file stands in for IX2 in the prototype.
   The only exception is the number counter — see WEBFLOW.md.
   ============================================================ */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO   = 'IntersectionObserver' in window;

  /* ---------- 1 · reveal on scroll ------------------------- */
  var reveals = document.querySelectorAll('.reveal');
  if (!hasIO || reduced) {
    Array.prototype.forEach.call(reveals, function (el) { el.classList.add('is-in'); });
  } else {
    var revealIO = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        obs.unobserve(e.target);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    Array.prototype.forEach.call(reveals, function (el) { revealIO.observe(el); });
  }

  /* ---------- 2 · maturity meters -------------------------- */
  var levels = document.getElementById('levels');
  if (levels) {
    if (!hasIO || reduced) levels.classList.add('is-in');
    else {
      var lio = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          obs.unobserve(e.target);
        });
      }, { threshold: 0.3 });
      lio.observe(levels);
    }
  }

  /* ---------- 3 · counters that run once on arrival -------- */
  function countTo(el, target, suffix, duration) {
    var start = parseFloat(el.textContent) || 0;
    if (reduced || !duration) { el.textContent = target + suffix; return; }
    var t0 = null;
    if (el._raf) cancelAnimationFrame(el._raf);
    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min((ts - t0) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(start + (target - start) * eased) + suffix;
      if (p < 1) el._raf = requestAnimationFrame(step);
    }
    el._raf = requestAnimationFrame(step);
  }

  var countIns = document.querySelectorAll('[data-count-in]');
  if (countIns.length) {
    if (!hasIO || reduced) {
      Array.prototype.forEach.call(countIns, function (el) { el.textContent = el.dataset.to; });
    } else {
      var cio = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          countTo(e.target, Number(e.target.dataset.to), '', 900);
          obs.unobserve(e.target);
        });
      }, { threshold: 0.6 });
      Array.prototype.forEach.call(countIns, function (el) { cio.observe(el); });
    }
  }

  /* ---------- 4 · sub-nav current section ------------------ */
  var links = document.querySelectorAll('.subnav__link');
  if (links.length && hasIO) {
    var map = {};
    Array.prototype.forEach.call(links, function (l) {
      var t = document.querySelector(l.getAttribute('href'));
      if (t) map[t.id] = l;
    });
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var link = map[e.target.id];
        if (!link) return;
        if (e.isIntersecting) {
          Array.prototype.forEach.call(links, function (l) { l.classList.remove('is-current'); });
          link.classList.add('is-current');
        }
      });
    }, { threshold: 0.25, rootMargin: '-80px 0px -55% 0px' });
    Object.keys(map).forEach(function (k) { sio.observe(document.getElementById(k)); });
  }
})();

/* ============================================================
   VSCROLL — before/after scrubbed by scroll, used twice
   Sets two custom properties on the section:
     --p   raw progress 0..1 through the sticky travel
     --pm  the same, ramped 0..1 across the middle third
   CSS does the rest, so nothing here touches layout directly.
   ============================================================ */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function wire(root, copy) {
    if (!root) return;
    var track = root.querySelector('.vscroll__track');
    var label = root.querySelector('.vscroll__label');
    var note  = root.querySelector('.vscroll__note');
    if (!track) return;

    /* reduced motion: land on the state that makes the argument, no scrubbing */
    if (reduced) {
      root.style.setProperty('--p', 1);
      root.style.setProperty('--pm', 1);
      root.dataset.state = 'after';
      if (label) label.textContent = copy.after[0];
      if (note)  note.innerHTML    = copy.after[1];
      return;
    }

    var state = null;
    function setState(key) {
      if (state === key) return;
      state = key;
      root.dataset.state = key;
      if (label) label.textContent = copy[key][0];
      if (note)  note.innerHTML    = copy[key][1];
    }
    setState('before');

    function update() {
      var r = root.getBoundingClientRect();
      /* the sticky child holds for (root height - viewport) of scrolling */
      var travel = r.height - window.innerHeight;
      if (travel <= 0) return;
      var p = Math.min(Math.max(-r.top / travel, 0), 1);

      /* ease the raw progress so the middle of the scroll does most of the
         work — a linear map makes the first and last pixels feel dead */
      var eased = p * p * (3 - 2 * p);
      root.style.setProperty('--p', eased.toFixed(4));

      /* the words swap across the middle third, not at a hard midpoint */
      var pm = Math.min(Math.max((p - 0.34) / 0.32, 0), 1);
      root.style.setProperty('--pm', pm.toFixed(4));
      setState(pm > 0.5 ? 'after' : 'before');
    }

    var queued = false;
    function onScroll() {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () { queued = false; update(); });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }

  wire(document.getElementById('cycle'), {
    before: ['Without AI \u00b7 12 weeks',
             'Build is where the calendar goes \u2014 every other stage waits on it.'],
    after:  ['An AI-enhanced process \u00b7 6 weeks',
             '<em>Agents draft</em> a share of every stage. <b>The bottleneck collapses and six weeks come back</b>, and a person still signs off every merge.']
  });

  wire(document.getElementById('tscroll'), {
    before: ['A cross-functional team \u00b7 7 people',
             'Seven people, each holding one part of the work.'],
    after:  ['An AI-enhanced team \u00b7 2 people, plus agents',
             'Two senior makers own the outcome. Agents draft, and specialist craft comes in when it is needed.']
  });
})();

/* ============================================================
   BUILT BY LOOMERY — the stage follows what you are reading
   A thin band across the middle of the viewport decides which
   product is active; whichever step is crossing it wins.
   ============================================================ */
(function () {
  var scroll = document.getElementById('pscroll');
  if (!scroll) return;

  var steps = scroll.querySelectorAll('.pstep');
  var panes = scroll.querySelectorAll('.ppane');
  if (!steps.length) return;

  function activate(key) {
    if (scroll.dataset.product === key) return;
    scroll.dataset.product = key;
    Array.prototype.forEach.call(panes, function (p) {
      if (p.dataset.product === key) p.setAttribute('data-on', '');
      else p.removeAttribute('data-on');
    });
  }

  if (!('IntersectionObserver' in window)) {
    scroll.setAttribute('data-static', '');
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) activate(e.target.dataset.product);
    });
  }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 });

  Array.prototype.forEach.call(steps, function (s) { io.observe(s); });
})();
