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

  /* ---------- 4 · before / after blocks --------------------
     Used twice: the lifecycle track and the team row.
     One class flips the whole thing; everything animated is
     width, flex-grow, opacity or transform.
     -------------------------------------------------------- */
  function wireBeforeAfter(el) {
    var id       = el.id;
    var buttons  = document.querySelectorAll('.ba-btn[data-target="' + id + '"]');
    var captions = document.querySelectorAll('.ba-caption[data-for="' + id + '"]');
    var readout  = document.querySelector('.ba-readout[data-for="' + id + '"]');
    var counters = readout ? readout.querySelectorAll('[data-count]') : [];
    var played   = false;

    function setState(state) {
      var after = state === 'after';
      el.classList.toggle('is-after', after);
      if (readout) readout.classList.toggle('is-after', after);

      Array.prototype.forEach.call(buttons, function (b) {
        b.setAttribute('aria-pressed', String(b.dataset.state === state));
      });
      Array.prototype.forEach.call(captions, function (c) {
        c.hidden = (c.dataset.cap !== state);
      });
      Array.prototype.forEach.call(counters, function (c) {
        countTo(c, Number(after ? c.dataset.after : c.dataset.before), c.dataset.suffix || '', 700);
      });
    }

    Array.prototype.forEach.call(buttons, function (b) {
      b.addEventListener('click', function () { setState(b.dataset.state); });
    });

    if (el.hasAttribute('data-autoplay') && hasIO) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting || played) return;
          played = true;
          setTimeout(function () { setState('after'); }, reduced ? 0 : 600);
          io.disconnect();
        });
      }, { threshold: 0.4 });
      io.observe(el);
    }
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-ba]'), wireBeforeAfter);
  window.yarnCountTo = countTo;   /* the steppers below reuse it */

  /* ---------- 5 · sub-nav current section ------------------ */
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
   LIFECYCLE — four steps on a timer
   Advances itself; the buttons jump the reader to a step and the
   cycle carries on from there.
   ============================================================ */
(function () {
  var cycle = document.getElementById('cycle');
  if (!cycle) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var CAPS = [
    "A normal project. <b>Build is where the calendar goes</b> \u2014 everything else waits on it.",
    "Agents draft in discover and design. <b>The front of the project tightens</b> before a line of code is written.",
    "Agents draft the build too. <b>The bottleneck collapses</b> \u2014 520 down to 130.",
    "Test, ship and learn tighten as well. <b>Six weeks come back</b>, and a person still signs off every merge."
  ];

  var buttons = cycle.querySelectorAll('.lc__step');
  var cap     = document.getElementById('cycleCap');
  var readout = cycle.querySelector('.lc__readout');
  var metrics = readout ? readout.querySelectorAll('[data-steps]') : [];
  var count   = window.yarnCountTo;

  /* the words used to hard-cut while the bars were still gliding.
     Fade out, swap, fade back in, so text and diagram change together. */
  var capTimer = null;
  function setCap(html) {
    if (!cap) return;
    clearTimeout(capTimer);
    if (reduced) { cap.innerHTML = html; return; }
    cap.classList.add('is-swapping');
    capTimer = setTimeout(function () {
      cap.innerHTML = html;
      cap.classList.remove('is-swapping');
    }, 150);
  }

  /* dur: how long the bars are taking, so the counters land with them
     rather than finishing early and sitting dead */
  function go(n, dur) {
    cycle.dataset.step = String(n);
    Array.prototype.forEach.call(buttons, function (b) {
      b.setAttribute('aria-current', String(Number(b.dataset.go) === n));
    });
    setCap(CAPS[n - 1]);
    if (readout) readout.classList.toggle('is-after', n > 1);
    Array.prototype.forEach.call(metrics, function (m) {
      var to = Number(m.dataset.steps.split(',')[n - 1]);
      if (count) count(m, to, m.dataset.suffix || '', reduced ? 0 : (dur || 900));
      else m.textContent = to + (m.dataset.suffix || '');
    });
  }

  if (reduced) {
    /* no cycling: land on the end state, which is the point of the section */
    go(4);
    Array.prototype.forEach.call(buttons, function (b) {
      b.addEventListener('click', function () { go(Number(b.dataset.go), 0); });
    });
    return;
  }

  function ms(name) {
    var v = getComputedStyle(cycle).getPropertyValue(name).trim();
    return v.slice(-2) === 'ms' ? parseFloat(v) : parseFloat(v) * 1000;
  }

  var step        = 1;
  var timer       = null;
  var rewindTimer = null;
  var startedAt   = 0;
  var remaining   = 0;
  var visible     = false;
  var hovered     = false;
  var focused     = false;

  function dwell() { return step === 4 ? ms('--dwell-last') : ms('--dwell'); }
  function shouldRun() { return visible && !hovered && !focused; }

  function arm(wait) {
    startedAt = Date.now();
    remaining = wait;
    timer = setTimeout(advance, wait);
  }

  function advance() {
    timer = null;
    var wrapping = step === 4;
    show(wrapping ? 1 : step + 1, wrapping);
    sync();
  }

  /* one place moves the diagram, whether a timer or a click asked for it */
  function show(n, wrapping) {
    step = n;
    /* going back to a normal project is a rewind — one slower, unstaggered
       move, so it does not read as a fifth step */
    clearTimeout(rewindTimer);
    cycle.classList.toggle('is-rewind', !!wrapping);
    if (wrapping) {
      rewindTimer = setTimeout(function () { cycle.classList.remove('is-rewind'); }, 1250);
    }
    go(step, wrapping ? 1150 : 900);
    remaining = 0;
  }

  /* one place decides whether the timer is running, so the reasons it
     can stop (off screen, hovered, focused) cannot fight */
  function sync() {
    if (shouldRun()) {
      if (!timer) {
        cycle.classList.remove('is-paused');
        arm(remaining > 0 ? remaining : dwell());
      }
    } else {
      if (timer) {
        clearTimeout(timer);
        timer = null;
        remaining = Math.max(400, remaining - (Date.now() - startedAt));
      }
      cycle.classList.add('is-paused');
    }
  }

  /* Two observers.

     `ready` gates the timer on the WHOLE block being on screen. Gating on a
     bare 35% fired while the diagram was still clipping the bottom edge — only
     143px of 302 showing — so by the time the reader had it comfortably in
     view it was already a step or two in, which reads as "it didn't start on
     scroll, it was already running".

     `seen` tracks whether it has fully left, so coming back to it later
     replays from step 1 rather than resuming mid-sequence. A small scroll that
     only dips it below the ready line does not reset it. */
  var needsReset = false;

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        /* a block taller than the viewport can never be wholly visible */
        var cannotFit = e.rootBounds && e.boundingClientRect.height > e.rootBounds.height * 0.9;
        var ready = e.intersectionRatio >= 0.99 || (cannotFit && e.isIntersecting);
        if (ready && needsReset) {
          needsReset = false;
          show(1, false);
        }
        visible = ready;
        sync();
      });
    }, { threshold: [0, 0.99] }).observe(cycle);

    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (!e.isIntersecting) needsReset = true; });
    }, { threshold: 0 }).observe(cycle);
  } else {
    visible = true; sync();
  }

  /* let someone read a step without it moving under them */
  cycle.addEventListener('pointerenter', function () { hovered = true;  sync(); });
  cycle.addEventListener('pointerleave', function () { hovered = false; sync(); });
  /* Only keyboard focus pauses. A mouse click leaves the button focused, and
     pausing on that would freeze the cycle for good once the pointer left. */
  cycle.addEventListener('focusin', function (e) {
    var t = e.target;
    focused = !!(t && t.matches && t.matches(':focus-visible'));
    sync();
  });
  cycle.addEventListener('focusout', function () { focused = false; sync(); });

  /* a click jumps to that step and the cycle carries on from there,
     with a full dwell so the reader gets to look at what they picked */
  Array.prototype.forEach.call(buttons, function (b) {
    b.addEventListener('click', function () {
      var n = Number(b.dataset.go);
      if (timer) { clearTimeout(timer); timer = null; }
      show(n, false);
      sync();
    });
  });
})();
