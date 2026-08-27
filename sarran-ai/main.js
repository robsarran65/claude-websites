/* Sarran AI Solutions — interaction layer.
   Progressive enhancement: nothing is hidden by CSS until JS arms it, so with
   JS disabled the page renders complete and static.
   No cursor-tracked effects anywhere, by design. */

(function () {
  'use strict';

  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Mobile drawer ---------------------------------------------------- */
  var toggle = document.querySelector('.masthead__toggle');
  var drawer = document.getElementById('drawer');

  function closeDrawer() {
    if (!toggle || !drawer) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    drawer.hidden = true;
  }

  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      if (open) { closeDrawer(); return; }
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
      drawer.hidden = false;
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeDrawer();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !drawer.hidden) { closeDrawer(); toggle.focus(); }
    });
  }

  /* --- Masthead tucks away on scroll down, returns on scroll up --------- */
  var masthead = document.querySelector('.masthead');
  var lastY = window.scrollY;
  var ticking = false;

  if (masthead) {
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        var y = window.scrollY;
        var tuck = y > lastY && y > 240 && (!drawer || drawer.hidden);
        masthead.setAttribute('data-tucked', String(tuck));
        lastY = y;
        ticking = false;
      });
    }, { passive: true });
  }

  /* --- Signature: the call log plays itself out on first view ----------- */
  var log = document.querySelector('[data-log]');

  if (log && !calm) {
    var lines = Array.prototype.slice.call(log.querySelectorAll('[data-line]'));
    lines.forEach(function (line) { line.setAttribute('data-armed', ''); });

    var play = function () {
      lines.forEach(function (line, i) {
        // the last line is the booking confirmation — let it land on its own beat
        var gap = i === lines.length - 1 ? 620 : 480;
        var delay = i * 480 + (i === lines.length - 1 ? gap - 480 : 0);
        window.setTimeout(function () { line.classList.add('is-typed'); }, 420 + delay);
      });
    };

    if ('IntersectionObserver' in window) {
      var logWatch = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          logWatch.unobserve(entry.target);
          play();
        });
      }, { threshold: 0.35 });
      logWatch.observe(log);
    } else {
      play();
    }
  }

  /* --- Typewriter on the closing headline ------------------------------- */
  var tw = document.querySelector('[data-typewriter]');

  if (tw && !calm) {
    var real = tw.querySelector('.tw__real');
    var out = tw.querySelector('.tw__type');
    var text = real.textContent.trim();

    tw.setAttribute('data-armed', '');

    var caret = document.createElement('span');
    caret.className = 'tw__caret';

    var typeOut = function () {
      var i = 0;
      (function step() {
        out.textContent = text.slice(0, i);
        out.appendChild(caret);
        if (i > text.length) { tw.classList.add('is-done'); return; }
        // hold a beat on the sentence's punctuation, run on normally otherwise
        var ch = text.charAt(i - 1);
        i += 1;
        window.setTimeout(step, ch === ',' ? 220 : 38);
      })();
    };

    if ('IntersectionObserver' in window) {
      var twWatch = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          twWatch.unobserve(entry.target);
          window.setTimeout(typeOut, 220);
        });
      }, { threshold: 0.6 });
      twWatch.observe(tw);
    } else {
      typeOut();
    }
  }

  /* --- Scroll reveal ---------------------------------------------------- */
  var targets = document.querySelectorAll(
    '.lede, .offer, .phase, .rule, .faq__item, .record__row, .about__copy, .book__inner, .pedigree__inner'
  );

  if (targets.length && !calm && 'IntersectionObserver' in window) {
    var revealWatch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        revealWatch.unobserve(entry.target);
        entry.target.classList.add('is-in');
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    Array.prototype.forEach.call(targets, function (el, i) {
      el.setAttribute('data-reveal', '');
      // stagger siblings slightly so a grid resolves in sequence, not all at once
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      revealWatch.observe(el);
    });
  }

  /* --- Booking form ----------------------------------------------------- */
  var panel = document.getElementById('book-form');
  var form = panel && panel.querySelector('.bform');

  if (panel && form) {
    var status = form.querySelector('.bform__status');
    var toggles = document.querySelectorAll('[data-book-toggle]');
    // every "Book" link elsewhere on the page also opens the panel
    var openers = document.querySelectorAll('a[href="#book"]');

    // Collapse only now that JS is running — without JS the form stays visible.
    panel.hidden = true;
    panel.classList.add('is-collapsible');

    var setExpanded = function (open) {
      Array.prototype.forEach.call(toggles, function (t) {
        t.setAttribute('aria-expanded', String(open));
      });
    };

    var openPanel = function (moveFocus) {
      panel.hidden = false;
      setExpanded(true);
      if (moveFocus) {
        // scope to .field — the form's first `input` is a hidden control
        // and the honeypot, neither of which can take focus
        var first = form.querySelector('.field input, .field textarea');
        if (first) first.focus({ preventScroll: true });
      }
    };

    var closePanel = function () {
      panel.hidden = true;
      setExpanded(false);
    };

    Array.prototype.forEach.call(toggles, function (t) {
      t.addEventListener('click', function () {
        if (panel.hidden) { openPanel(true); } else { closePanel(); }
      });
    });

    Array.prototype.forEach.call(openers, function (a) {
      // let the anchor scroll to #book as normal, then reveal the form
      a.addEventListener('click', function () { openPanel(false); });
    });

    /* Validation. Native constraints do the checking; we render the messages
       so they are visible, associated, and announced (WCAG 3.3.1). */
    var showError = function (input, message) {
      var err = document.getElementById(input.id + '-err');
      input.setAttribute('aria-invalid', 'true');
      if (err) { err.textContent = message; err.hidden = false; }
    };

    var clearError = function (input) {
      var err = document.getElementById(input.id + '-err');
      input.removeAttribute('aria-invalid');
      if (err) { err.textContent = ''; err.hidden = true; }
    };

    var messageFor = function (input) {
      if (input.validity.valueMissing) {
        return input.tagName === 'TEXTAREA'
          ? 'Tell us briefly what you are looking for.'
          : 'Enter your ' + input.labels[0].textContent.replace(/required/i, '').trim().toLowerCase() + '.';
      }
      if (input.validity.typeMismatch && input.type === 'email') return 'Enter a valid email address, like name@company.com.';
      if (input.validity.typeMismatch && input.type === 'url') return 'Enter a full address, starting with https://';
      return 'Check this field.';
    };

    form.addEventListener('input', function (e) {
      if (e.target.getAttribute('aria-invalid') === 'true' && e.target.checkValidity()) clearError(e.target);
    });

    form.addEventListener('submit', function (e) {
      var fields = form.querySelectorAll('input, textarea');
      var firstBad = null;

      Array.prototype.forEach.call(fields, function (input) {
        if (input.checkValidity()) { clearError(input); return; }
        showError(input, messageFor(input));
        if (!firstBad) firstBad = input;
      });

      if (firstBad) {
        e.preventDefault();
        status.textContent = 'Please fix the highlighted fields.';
        status.setAttribute('data-state', 'error');
        firstBad.focus();
        return;
      }

      var endpoint = form.getAttribute('data-endpoint');

      // No fetch (or no endpoint configured)? Let the browser post the form
      // natively to `action` — the visitor still gets through.
      if (!endpoint || !window.fetch) {
        status.textContent = 'Sending…';
        return;
      }

      e.preventDefault();

      var submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      form.setAttribute('aria-busy', 'true');
      status.textContent = 'Sending…';
      status.setAttribute('data-state', '');

      var failed = function (reason) {
        submitBtn.disabled = false;
        form.removeAttribute('aria-busy');
        var detail = reason && reason.message ? reason.message : String(reason || '');
        var needsActivation = /activation|activate/i.test(detail);

        status.innerHTML = needsActivation
          ? 'This form still needs to be activated for this website. Check ' +
            '<a href="mailto:robertgangasarran@gmail.com">robertgangasarran@gmail.com</a> ' +
            '(including Spam) for the FormSubmit activation email, click its link, then submit again.'
          : 'That did not send. Please email ' +
            '<a href="mailto:robertgangasarran@gmail.com">robertgangasarran@gmail.com</a> ' +
            'and we will pick it up from there.';
        status.setAttribute('data-state', 'error');
        // surface the relay's own reason in the console for diagnosis —
        // it returns HTTP 200 even when it rejects a submission
        if (reason && window.console) window.console.error('[booking form]', reason);
      };

      var payload = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.type !== 'submit') payload[el.name] = el.value;
      });

      // FormSubmit recommends an explicit form URL because strict referrer
      // policies can otherwise prevent it from identifying the form's site.
      payload._url = window.location.href.split('#')[0];

      window.fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      }).then(function (data) {
        // The relay answers HTTP 200 even on rejection — the real verdict is
        // `success` in the body, and it arrives as the string "true"/"false".
        var delivered = data && (data.success === true || data.success === 'true');
        if (!delivered) throw new Error((data && data.message) || 'Submission rejected');
        form.reset();
        submitBtn.disabled = false;
        form.removeAttribute('aria-busy');
        status.textContent = 'Thanks — your request is in. We reply within one business day.';
        status.setAttribute('data-state', 'ok');
      }).catch(failed);
    });
  }

  /* --- Footer year ------------------------------------------------------ */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
