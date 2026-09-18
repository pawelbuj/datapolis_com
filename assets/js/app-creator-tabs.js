(function() {
    'use strict';

    var root = document.querySelector('[data-ac-tabs]');
    if (!root) return;

    var tabs = root.querySelectorAll('[data-ac-tab]');
    var panels = root.querySelectorAll('[data-ac-panel]');
    var subs = root.querySelectorAll('[data-ac-sub]');
    var views = root.querySelectorAll('[data-ac-view]');

    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var timer = null, auto = !reduced, step = 1;

    function show(n) {
        step = n;
        Array.prototype.forEach.call(tabs, function(t) {
            t.setAttribute('aria-selected', String(t.getAttribute('data-ac-tab') === String(n)));
        });
        Array.prototype.forEach.call(panels, function(p) {
            p.classList.toggle('is-on', p.getAttribute('data-ac-panel') === String(n));
        });
    }

    function schedule() {
        window.clearTimeout(timer);
        if (!auto || document.hidden) return;
        timer = window.setTimeout(function() {
            show(step % panels.length + 1);
            schedule();
        }, 6000);
    }

    // Klikniecie zatrzymuje karuzele - dalej oglada juz uzytkownik, nie strona.
    function stop() { auto = false; window.clearTimeout(timer); }

    Array.prototype.forEach.call(tabs, function(t) {
        t.addEventListener('click', function() { stop(); show(Number(t.getAttribute('data-ac-tab'))); });
    });

    Array.prototype.forEach.call(subs, function(b) {
        b.addEventListener('click', function() {
            stop();
            var v = b.getAttribute('data-ac-sub');
            Array.prototype.forEach.call(subs, function(x) { x.setAttribute('aria-selected', String(x === b)); });
            Array.prototype.forEach.call(views, function(x) { x.classList.toggle('is-on', x.getAttribute('data-ac-view') === v); });
        });
    });

    document.addEventListener('visibilitychange', function() {
        if (document.hidden) window.clearTimeout(timer); else schedule();
    });

    if ('IntersectionObserver' in window) {
        var obs = new IntersectionObserver(function(entries) {
            if (entries[0] && entries[0].isIntersecting) schedule();
            else window.clearTimeout(timer);
        }, { threshold: 0.2 });
        obs.observe(root);
    }

    show(1);
    schedule();
})();
