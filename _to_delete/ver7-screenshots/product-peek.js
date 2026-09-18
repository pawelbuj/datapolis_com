/* product-peek.js — podglady zrzutow z produktu (ver7)
 * Miniatura otwiera lightbox z pelnym kadrem. Bez bibliotek.
 * Dialog powstaje raz i jest wspoldzielony przez wszystkie podglady.
 */
(function () {
    'use strict';

    var dlg = null, imgEl = null, barEl = null, capEl = null;

    function build() {
        if (dlg) { return; }
        dlg = document.createElement('dialog');
        dlg.className = 'v7-lightbox';
        dlg.innerHTML =
            '<div class="v7-lightbox__inner">' +
              '<div class="v7-lightbox__bar"><i aria-hidden="true"></i>' +
                '<span data-lb-bar></span>' +
                '<button type="button" class="v7-lightbox__close" data-lb-close aria-label="Close">&#10005;</button>' +
              '</div>' +
              '<img class="v7-lightbox__img" alt="" data-lb-img>' +
              '<p class="v7-lightbox__cap" data-lb-cap></p>' +
            '</div>';
        document.body.appendChild(dlg);
        imgEl = dlg.querySelector('[data-lb-img]');
        barEl = dlg.querySelector('[data-lb-bar]');
        capEl = dlg.querySelector('[data-lb-cap]');

        dlg.querySelector('[data-lb-close]').addEventListener('click', close);
        // klikniecie w tlo zamyka
        dlg.addEventListener('click', function (e) {
            if (e.target === dlg) { close(); }
        });
    }

    function close() {
        if (dlg && dlg.open) { dlg.close(); }
    }

    function open(btn) {
        build();
        imgEl.src = btn.getAttribute('data-peek-src');
        imgEl.alt = btn.getAttribute('data-peek-alt') || '';
        barEl.textContent = btn.getAttribute('data-peek-bar') || '';
        capEl.innerHTML = btn.getAttribute('data-peek-cap') || '';
        if (typeof dlg.showModal === 'function') {
            dlg.showModal();
        } else {
            // starsza przegladarka: po prostu otwieramy obraz
            window.open(imgEl.src, '_blank', 'noopener');
        }
    }

    function boot() {
        var btns = document.querySelectorAll('[data-peek-src]');
        for (var i = 0; i < btns.length; i++) {
            (function (b) {
                b.addEventListener('click', function () { open(b); });
            })(btns[i]);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
