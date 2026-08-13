/* 2to2 hero animation — living model loop (spec → build → app → sync → app change → doc update → sync) */
(function () {
  'use strict';

  function init() {
    var stage = document.getElementById('v4aStage');
    if (!stage) return;

    var $ = function (id) { return document.getElementById(id); };
    var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var cursor = $('v4aCursor'), core = $('v4aCore');
    var docPanel = $('v4aDocPanel'), appPanel = $('v4aAppPanel');
    var buildBtn = $('v4aBuildBtn'), updateBtn = $('v4aUpdateBtn'), syncBadge = $('v4aSync');
    var linkL = $('v4aLinkL'), linkR = $('v4aLinkR');

    var docParts = [
      ['v4aDocTitle', 'v4aCaretT', 'Vendor onboarding', 34],
      ['v4aDocL1', 'v4aCaret1', 'Roles|:  Buyer, Compliance Manager', 17],
      ['v4aDocL2', 'v4aCaret2', 'Data|:  vendor name, risk category', 17],
      ['v4aDocL3', 'v4aCaret3', 'Process|:  Draft → Review → Active', 17],
      ['v4aDocL4', 'v4aCaret4', '“High-risk vendors require approval.”', 21]
    ];

    async function typeInto(spanId, caretId, text, speed) {
      var span = $(spanId), caret = $(caretId);
      caret.classList.add('on');
      var keyIdx = text.indexOf('|');
      var clean = text.replace('|', '');
      for (var i = 0; i < clean.length; i++) {
        span.innerHTML = (keyIdx > 0 && i >= keyIdx - 1)
          ? '<span class="v4a-k">' + clean.slice(0, keyIdx) + '</span>' + clean.slice(keyIdx, i + 1)
          : clean.slice(0, i + 1);
        await sleep(speed);
      }
      caret.classList.remove('on');
    }

    function moveCursorTo(el, dx, dy) {
      var s = stage.getBoundingClientRect(), r = el.getBoundingClientRect();
      cursor.style.transform = 'translate(' + (r.left - s.left + r.width / 2 + (dx || 0)) + 'px,' + (r.top - s.top + r.height / 2 + (dy || 0)) + 'px)';
    }

    async function clickWith(btn) {
      cursor.classList.add('visible');
      moveCursorTo(btn, 12, 7);
      await sleep(900);
      cursor.classList.add('clicking');
      btn.classList.add('pressed');
      await sleep(180);
      btn.classList.remove('pressed');
      await sleep(380);
      cursor.classList.remove('clicking');
    }

    function hideCursor() { cursor.classList.remove('visible'); }

    async function syncSignal() {
      core.classList.remove('spin', 'spin-rev');
      linkL.className = 'v4a-link v4a-link-l'; linkR.className = 'v4a-link v4a-link-r';
      docPanel.classList.add('flash'); appPanel.classList.add('flash');
      syncBadge.classList.add('show', 'pulse');
      await sleep(1900);
      docPanel.classList.remove('flash'); appPanel.classList.remove('flash');
      docPanel.classList.add('live'); appPanel.classList.add('live');
      syncBadge.classList.remove('pulse');
    }

    function resetAll() {
      docParts.forEach(function (p) { $(p[0]).innerHTML = ''; $(p[1]).classList.remove('on'); });
      $('v4aDocComplete').classList.remove('show');
      $('v4aDocNew').classList.remove('show', 'settled');
      $('v4aAppEmpty').classList.remove('hide');
      ['v4aBlockFlow', 'v4aBlockData', 'v4aBlockPage'].forEach(function (id) { $(id).classList.remove('show'); });
      $('v4aNewChip').classList.remove('show', 'settled');
      $('v4aNewSep').classList.remove('show');
      buildBtn.classList.remove('show'); updateBtn.classList.remove('show');
      syncBadge.classList.remove('show', 'pulse');
      docPanel.classList.remove('flash', 'live'); appPanel.classList.remove('flash', 'live');
      core.classList.remove('spin', 'spin-rev');
      linkL.className = 'v4a-link v4a-link-l'; linkR.className = 'v4a-link v4a-link-r';
      hideCursor();
    }

    function finalState() {
      $('v4aDocTitle').textContent = 'Vendor onboarding';
      $('v4aDocL1').innerHTML = '<span class="v4a-k">Roles:</span>  Buyer, Compliance Manager';
      $('v4aDocL2').innerHTML = '<span class="v4a-k">Data:</span>  vendor name, risk category';
      $('v4aDocL3').innerHTML = '<span class="v4a-k">Process:</span>  Draft → Review → Active';
      $('v4aDocL4').textContent = '“High-risk vendors require approval.”';
      $('v4aDocComplete').classList.add('show');
      $('v4aDocNew').classList.add('show', 'settled');
      $('v4aAppEmpty').classList.add('hide');
      ['v4aBlockFlow', 'v4aBlockData', 'v4aBlockPage'].forEach(function (id) { $(id).classList.add('show'); });
      $('v4aNewChip').classList.add('show', 'settled'); $('v4aNewSep').classList.add('show');
      syncBadge.classList.add('show');
      docPanel.classList.add('live'); appPanel.classList.add('live');
    }

    async function run() {
      if (reduced) { finalState(); return; }
      for (;;) {
        resetAll();
        await sleep(1100);

        /* the specification writes itself */
        for (var i = 0; i < docParts.length; i++) {
          await typeInto(docParts[i][0], docParts[i][1], docParts[i][2], docParts[i][3]);
          await sleep(240);
        }
        $('v4aDocComplete').classList.add('show');
        await sleep(700);

        /* click: Build application */
        buildBtn.classList.add('show');
        await clickWith(buildBtn);
        buildBtn.classList.remove('show');
        hideCursor();

        /* build: core spins, app assembles */
        core.classList.add('spin');
        linkL.classList.add('flow', 'ltr'); linkR.classList.add('flow', 'ltr');
        await sleep(650);
        $('v4aAppEmpty').classList.add('hide');
        await sleep(350);
        $('v4aBlockFlow').classList.add('show'); await sleep(640);
        $('v4aBlockData').classList.add('show'); await sleep(640);
        $('v4aBlockPage').classList.add('show'); await sleep(760);

        /* in sync */
        await syncSignal();
        await sleep(1500);

        /* a change in the app: new workflow state */
        syncBadge.classList.remove('show');
        docPanel.classList.remove('live');
        $('v4aNewSep').classList.add('show');
        $('v4aNewChip').classList.add('show');
        await sleep(1250);

        /* click: Update documentation */
        updateBtn.classList.add('show');
        await clickWith(updateBtn);
        updateBtn.classList.remove('show');
        hideCursor();

        /* the spec catches up */
        core.classList.add('spin-rev');
        linkL.classList.add('flow', 'rtl'); linkR.classList.add('flow', 'rtl');
        await sleep(750);
        $('v4aDocNew').classList.add('show');
        await sleep(1050);
        $('v4aDocNew').classList.add('settled');
        $('v4aNewChip').classList.add('settled');
        await syncSignal();
        await sleep(2600);
      }
    }

    run();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
