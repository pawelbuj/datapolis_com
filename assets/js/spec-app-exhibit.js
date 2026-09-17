/* spec-app-exhibit.js — eksponat "specyfikacja <-> aplikacja" (ver7)
 *
 * Zasady:
 *  - brak autoplaya i brak petli: pierwsza klatka pokazuje gotowa aplikacje,
 *  - powiazanie dziala w obie strony (zdanie <-> element aplikacji),
 *  - jeden przelacznik pokazuje drugi kierunek synchronizacji,
 *  - dziala z klawiatury i respektuje prefers-reduced-motion.
 */
(function () {
    'use strict';

    var LIT = 'is-lit';

    function init(root) {
        var links = root.querySelectorAll('[data-link]');
        if (!links.length) { return; }

        function paint(key, on) {
            for (var i = 0; i < links.length; i++) {
                if (links[i].getAttribute('data-link') === key) {
                    links[i].classList.toggle(LIT, on);
                }
            }
        }

        function bind(el) {
            var key = el.getAttribute('data-link');
            el.addEventListener('mouseenter', function () { paint(key, true); });
            el.addEventListener('mouseleave', function () { paint(key, false); });
            el.addEventListener('focus', function () { paint(key, true); });
            el.addEventListener('blur', function () { paint(key, false); });
        }

        for (var i = 0; i < links.length; i++) {
            bind(links[i]);
        }

        var toggle = root.querySelector('[data-exhibit-toggle]');
        if (!toggle) { return; }

        var labelEl = toggle.querySelector('[data-toggle-label]');
        var hint = root.querySelector('[data-exhibit-hint]');
        var copy = {
            idle: toggle.getAttribute('data-label-idle') || '',
            drifted: toggle.getAttribute('data-label-drifted') || '',
            synced: toggle.getAttribute('data-label-synced') || ''
        };
        var hints = {
            idle: hint ? hint.getAttribute('data-hint-idle') || '' : '',
            drifted: hint ? hint.getAttribute('data-hint-drifted') || '' : '',
            synced: hint ? hint.getAttribute('data-hint-synced') || '' : ''
        };
        var syncText = root.querySelector('[data-sync-text]');
        var syncCopy = {
            idle: syncText ? syncText.getAttribute('data-sync-idle') || '' : '',
            drifted: syncText ? syncText.getAttribute('data-sync-drifted') || '' : ''
        };

        // idle -> drifted (power user dopisal krok) -> synced (dokumentacja nadrobila)
        var state = 'idle';

        function render() {
            root.classList.toggle('is-drifted', state === 'drifted');
            root.classList.toggle('is-synced', state === 'synced');
            if (labelEl) { labelEl.textContent = copy[state]; }
            if (hint) { hint.textContent = hints[state]; }
            if (syncText) {
                syncText.textContent = state === 'drifted' ? syncCopy.drifted : syncCopy.idle;
            }
        }

        toggle.addEventListener('click', function () {
            state = state === 'idle' ? 'drifted' : (state === 'drifted' ? 'synced' : 'idle');
            render();
        });

        render();
    }

    function boot() {
        var roots = document.querySelectorAll('[data-spec-app-exhibit]');
        for (var i = 0; i < roots.length; i++) {
            init(roots[i]);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
