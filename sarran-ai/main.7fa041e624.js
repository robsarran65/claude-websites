/* Sarran AI Solutions — interaction layer.
   Progressive enhancement: nothing is hidden by CSS until JS arms it, so with
   JS disabled the page renders complete and static.
   No cursor-tracked effects anywhere, by design. */

(function () {
  'use strict';

  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Shared by the drawer and the chat panel: both hide an overlay that
  // contains the link the visitor just activated, which drops focus to
  // <body>. If the link was a same-page #anchor, move focus onto the section
  // it points to instead, so the next Tab continues from there rather than
  // the top of the document. Returns true if it found something to focus.
  function focusTarget(href) {
    if (!href || href.charAt(0) !== '#' || href.length < 2) return false;
    var el = document.getElementById(href.slice(1));
    if (!el) return false;
    if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
    el.focus({ preventScroll: true });
    return true;
  }

  /* --- Ask Sarran AI --------------------------------------------------- */
  var chatLauncher = document.querySelector('.chat-launcher');
  var chatPanel = document.getElementById('chat-panel');
  var chatClose = document.querySelector('.chat-panel__close');
  var chatForm = document.querySelector('.chat-form');
  var chatInput = document.getElementById('chat-input');
  var chatMessages = document.querySelector('.chat-panel__messages');
  var chatBook = document.querySelector('[data-chat-book]');
  if (chatLauncher && chatPanel && chatForm && chatInput && chatMessages) {
    var setChatOpen = function (open) { chatPanel.hidden = !open; chatLauncher.setAttribute('aria-expanded', String(open)); if (open) chatInput.focus(); };
    var appendChatMessage = function (text, kind) { var message = document.createElement('p'); message.className = 'chat-message chat-message--' + kind; message.textContent = text; chatMessages.appendChild(message); chatMessages.scrollTop = chatMessages.scrollHeight; };
    var answerChatQuestion = function (question) {
      var normalized = question.toLowerCase();
      if (normalized.includes('assessment') || normalized.includes('250')) return 'The AI Readiness Assessment is a $250 one-time service with a 45-minute working session, 3–7 ranked opportunities, and a written action plan. Use Start $250 assessment below. Payment is only considered verified after Stripe confirms the checkout; a button click alone is not proof of payment.';
      if (normalized.includes('book') || normalized.includes('consult') || normalized.includes('schedule')) return 'Choose Book 30 min with Robert below for a consultation. The form captures the problem first, and Robert replies within one business day.';
      if (normalized.includes('voice') || normalized.includes('call')) return 'Sarran AI builds voice agents that answer approved questions, qualify callers, schedule appointments, and hand off to a person when needed.';
      return 'Sarran AI helps small businesses, clinics, and service providers find repetitive work worth automating. Ask about the assessment, voice agents, workflow automation, or web development.';
    };
    chatLauncher.addEventListener('click', function () { setChatOpen(chatPanel.hidden); });
    if (chatClose) chatClose.addEventListener('click', function () { setChatOpen(false); chatLauncher.focus(); });
    if (chatBook) chatBook.addEventListener('click', function () {
      setChatOpen(false);
      // setChatOpen hides the panel this button lives in, which drops focus
      // to <body> — the close button and Escape both already send focus back
      // to the launcher; this path was the one left doing neither.
      focusTarget(chatBook.getAttribute('href')) || chatLauncher.focus();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !chatPanel.hidden) { setChatOpen(false); chatLauncher.focus(); } });
    Array.prototype.forEach.call(document.querySelectorAll('[data-chat-question]'), function (button) { button.addEventListener('click', function () { var question = button.getAttribute('data-chat-question'); appendChatMessage(question, 'user'); appendChatMessage(answerChatQuestion(question), 'agent'); }); });
    chatForm.addEventListener('submit', function (e) { e.preventDefault(); var question = chatInput.value.trim(); if (!question) return; appendChatMessage(question, 'user'); appendChatMessage(answerChatQuestion(question), 'agent'); chatInput.value = ''; });
  }

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
      var link = e.target.closest('a');
      if (!link) return;
      closeDrawer();
      // Hiding the drawer destroys focus, because the link just activated
      // lives inside it. Hand focus to whatever the link points at, so the
      // next Tab continues from the section the visitor asked for instead of
      // restarting at the top of the document.
      focusTarget(link.getAttribute('href')) || toggle.focus();
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
    '.lede, .assessment-card, .sample-plan, .who-card, .offer, .phase, .rule, .faq__item, .record__row, .about__copy, .guide__inner, .book__inner, .pedigree__inner'
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
    var guideRequests = document.querySelectorAll('[data-guide-request]');
    var assessmentRequests = document.querySelectorAll('a[href="#book"]:not([data-guide-request]), [data-book-toggle]');
    var interestField = form.querySelector('[data-interest-field]');
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
        // and the honeypot, neither of which can take focus. Scope to the
        // visible step too: a field on a hidden step cannot take focus either.
        var first = form.querySelector('.bform__step.is-active .field input, .bform__step.is-active .field textarea') ||
                    form.querySelector('.field input, .field textarea');
        if (first) first.focus({ preventScroll: true });
      }
    };

    var closePanel = function () {
      panel.hidden = true;
      setExpanded(false);
    };

    /* --- Stepped flow ----------------------------------------------------
       One <form>, three visual steps. All fields stay in the DOM the whole
       time, so the POST body is unchanged. The CSS that hides an inactive
       step is scoped to `.bform--stepped`, which is added right here at
       runtime — so with JavaScript off the three fieldsets simply stack and
       the form submits in a single pass exactly as it always did. */
    var steps = form.querySelectorAll('.bform__step');
    var progress = form.querySelector('.bform__progress');
    var progressItems = form.querySelectorAll('.bform__progress-item');
    var stepCount = form.querySelector('.bform__stepcount');
    var backBtn = form.querySelector('[data-step-back]');
    var nextBtn = form.querySelector('[data-step-next]');
    var stepSubmit = form.querySelector('button[type="submit"]');
    var briefField = document.getElementById('bf-brief');
    var stepped = steps.length > 1 && !!backBtn && !!nextBtn;
    var currentStep = 1;
    var guideMode = false;

    var stepLegend = function (n) {
      var step = steps[n - 1];
      return step ? step.querySelector('.bform__step-title') : null;
    };

    // moveFocus: true  -> always land focus on the new step's legend.
    //            'kept'-> only if focus was already inside the form, so that a
    //                     plain "#book" link does not yank focus off the link
    //                     the visitor just clicked.
    //            false -> never.
    var goToStep = function (n, moveFocus) {
      if (!stepped) return;
      if (n < 1) n = 1;
      if (n > steps.length) n = steps.length;

      var hadFocusInside = form.contains(document.activeElement);
      currentStep = n;

      Array.prototype.forEach.call(steps, function (step, i) {
        step.classList.toggle('is-active', (i + 1) === currentStep);
      });

      Array.prototype.forEach.call(progressItems, function (item, i) {
        item.classList.toggle('is-current', (i + 1) === currentStep);
        item.classList.toggle('is-done', (i + 1) < currentStep);
      });

      // the only non-decorative announcement of position (the rail is aria-hidden)
      if (stepCount) stepCount.textContent = 'Step ' + currentStep + ' of ' + steps.length;

      var onLast = currentStep === steps.length;
      // Back stays available on the final step: the visitor must be able to
      // return and fix what they wrote before committing to send it.
      // Guide mode is the exception — it is a single "where do we send it"
      // step, so there is nothing behind it worth walking back into.
      backBtn.hidden = guideMode || currentStep === 1;
      nextBtn.hidden = onLast;
      if (stepSubmit) stepSubmit.hidden = !onLast;

      if (moveFocus === true || (moveFocus === 'kept' && hadFocusInside)) {
        var legend = stepLegend(currentStep);
        // no preventScroll here: the new step should be brought into view
        if (legend) {
          legend.focus();
          // :focus-visible is suppressed on a programmatic focus() that
          // follows a pointer event (clicking Continue/Back with a mouse), so
          // the ring the CSS comment calls "never removed" was in fact
          // removed for every pointer-initiated step change. Force it with a
          // plain class instead of relying on the heuristic, and drop the
          // class on the step's own blur so it does not linger past the step
          // it announced.
          legend.classList.add('is-step-focus');
          legend.addEventListener('blur', function () {
            legend.classList.remove('is-step-focus');
          }, { once: true });
        }
      }
    };

    // Validates only the fields inside one step, reusing the same helpers the
    // submit handler uses so the messages are worded identically.
    var validateStep = function (n) {
      var step = steps[n - 1];
      if (!step) return true;
      var firstBad = null;

      Array.prototype.forEach.call(step.querySelectorAll('input, textarea, select'), function (input) {
        if (input.checkValidity()) { clearError(input); return; }
        showError(input, messageFor(input));
        if (!firstBad) firstBad = input;
      });

      if (firstBad) {
        status.textContent = 'Please fix the highlighted fields.';
        status.setAttribute('data-state', 'error');
        firstBad.focus();
        return false;
      }
      return true;
    };

    var advanceStep = function () {
      if (!validateStep(currentStep)) return;
      status.textContent = '';
      status.setAttribute('data-state', '');
      goToStep(currentStep + 1, true);
    };

    // Reveals the step that owns `input` before anything tries to focus it —
    // focus() on a display:none element silently does nothing, which would
    // leave "please fix the highlighted fields" pointing at nothing visible.
    var revealFieldStep = function (input) {
      if (!stepped || !input || !input.closest) return;
      var owner = input.closest('.bform__step');
      if (!owner) return;
      var n = parseInt(owner.getAttribute('data-step'), 10);
      if (n && n !== currentStep) goToStep(n, false);
    };

    if (stepped) {
      form.classList.add('bform--stepped');
      if (progress) progress.hidden = false;
      if (stepCount) stepCount.hidden = false;
      backBtn.hidden = false;
      nextBtn.hidden = false;

      nextBtn.addEventListener('click', advanceStep);
      backBtn.addEventListener('click', function () { goToStep(currentStep - 1, true); });

      // Enter in a single-line field means "continue", not "submit early".
      // Textareas keep Enter for line breaks; buttons and links keep their own.
      form.addEventListener('keydown', function (e) {
        if (e.key !== 'Enter' || currentStep === steps.length) return;
        var el = e.target;
        if (!el || el.tagName === 'TEXTAREA' || el.tagName === 'BUTTON' || el.tagName === 'A') return;
        e.preventDefault();
        advanceStep();
      });

      goToStep(1, false);
    }

    // Guide mode reuses this form but only needs the contact step, so the
    // brief stops being required and the rail is put away.
    var setGuideMode = function (on) {
      guideMode = !!on;
      if (briefField) {
        if (on) { briefField.removeAttribute('required'); clearError(briefField); }
        else { briefField.setAttribute('required', ''); }
      }
      if (!stepped) return;
      // hide the counter too: "Step 3 of 3" is untrue when there is one step
      if (progress) progress.hidden = on;
      if (stepCount) stepCount.hidden = on;
      goToStep(on ? steps.length : 1, 'kept');
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

    Array.prototype.forEach.call(guideRequests, function (a) {
      a.addEventListener('click', function () {
        if (interestField) interestField.value = 'Free time savings guide';
        openPanel(false);
        var title = form.querySelector('.bform__title');
        var intro = form.querySelector('.bform__intro');
        var submit = form.querySelector('button[type="submit"]');
        if (title) title.textContent = 'Where should we send your guide?';
        if (intro) intro.textContent = 'Enter your details and the guide will be ready immediately.';
        if (submit) submit.textContent = 'Get the Free Guide';
        setGuideMode(true);
      });
    });

    Array.prototype.forEach.call(assessmentRequests, function (a) {
      a.addEventListener('click', function () {
        if (interestField) interestField.value = 'AI Readiness Assessment';
        var title = form.querySelector('.bform__title');
        var intro = form.querySelector('.bform__intro');
        var submit = form.querySelector('button[type="submit"]');
        if (title) title.textContent = 'Tell us where you are losing time';
        if (intro) intro.textContent = 'A few quick questions. Robert replies within one business day.';
        if (submit) submit.textContent = 'Request My Assessment';
        setGuideMode(false);
      });
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
        revealFieldStep(firstBad);
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
            '<a href="mailto:robert@sarranai.com">robert@sarranai.com</a> ' +
            '(including Spam) for the FormSubmit activation email, click its link, then submit again.'
          : 'That did not send. Please email ' +
            '<a href="mailto:robert@sarranai.com">robert@sarranai.com</a> ' +
            'and we will pick it up from there.';
        status.setAttribute('data-state', 'error');
        // The visitor's focus is still on the disabled submit button at this
        // point, several fields above this message — send it to the recovery
        // link so the mailto: is one Tab away rather than a walk back up the
        // whole form.
        var recovery = status.querySelector('a');
        if (recovery) { recovery.setAttribute('tabindex', '-1'); recovery.focus(); }
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
        var requestedGuide = interestField && interestField.value === 'Free time savings guide';
        form.reset();
        submitBtn.disabled = false;
        form.removeAttribute('aria-busy');
        status.innerHTML = requestedGuide
          ? 'Thanks — <a href="small-business-time-savings-guide.html">open your free guide now</a>.'
          : 'Thanks — your request is in. Robert will reply within one business day.';
        status.setAttribute('data-state', 'ok');
      }).catch(failed);
    });
  }

  /* --- Footer year ------------------------------------------------------ */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
