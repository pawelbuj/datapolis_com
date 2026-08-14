(function() {
    'use strict';

    var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-concept]'));
    var panels = Array.prototype.slice.call(document.querySelectorAll('[data-concept-panel]'));
    var notes = Array.prototype.slice.call(document.querySelectorAll('[data-concept-note]'));
    var replay = document.querySelector('.hac-replay');
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var activeConcept = 'live-case';
    var activeTimer = null;
    var startDelay = null;

    var liveCaseSteps = [
        {
            owner: 'HUMAN TASK',
            action: 'Request submitted',
            meta: 'FORM · 8 FIELDS',
            time: '00:00'
        },
        {
            owner: 'DIGITAL WORKER',
            action: 'Reading & validating documents',
            meta: 'AI · 8 DOCUMENTS',
            time: '00:09'
        },
        {
            owner: 'HUMAN DECISION',
            action: 'Review policy exception',
            meta: 'RISK · 1 EXCEPTION',
            time: '00:18'
        },
        {
            owner: 'DIGITAL WORKER',
            action: 'Creating vendor in ERP',
            meta: 'ERP · CONNECTED',
            time: '00:31'
        },
        {
            owner: 'PROCESS OUTCOME',
            action: 'Vendor activated',
            meta: 'COMPLETE · AUDITED',
            time: '00:43'
        }
    ];

    function clearAnimationTimers() {
        if (activeTimer) {
            window.clearInterval(activeTimer);
            activeTimer = null;
        }
        if (startDelay) {
            window.clearTimeout(startDelay);
            startDelay = null;
        }
    }

    function setLiveCaseStep(step) {
        var canvas = document.querySelector('.c1-canvas');
        if (!canvas) return;

        var safeStep = Math.max(0, Math.min(step, liveCaseSteps.length - 1));
        var data = liveCaseSteps[safeStep];
        canvas.setAttribute('data-c1-step', String(safeStep));

        var owner = canvas.querySelector('[data-c1-owner]');
        var action = canvas.querySelector('[data-c1-action]');
        var meta = canvas.querySelector('[data-c1-meta]');
        var time = canvas.querySelector('[data-c1-time]');

        if (owner) owner.textContent = data.owner;
        if (action) action.textContent = data.action;
        if (meta) meta.textContent = data.meta;
        if (time) time.textContent = data.time;

        Array.prototype.forEach.call(canvas.querySelectorAll('.c1-workflow li'), function(node, index) {
            node.classList.toggle('is-done', index < safeStep);
            node.classList.toggle('is-active', index === safeStep);
        });
    }

    function setSwimlaneStep(step) {
        var canvas = document.querySelector('.c3-canvas');
        if (!canvas) return;

        var events = Array.prototype.slice.call(canvas.querySelectorAll('.c3-events li'));
        var safeStep = Math.max(0, Math.min(step, events.length - 1));
        canvas.setAttribute('data-c3-step', String(safeStep));

        events.forEach(function(event, index) {
            event.classList.toggle('is-done', index < safeStep);
            event.classList.toggle('is-active', index === safeStep);
        });
    }

    function restartCssAnimations(panel) {
        if (!panel) return;

        panel.classList.add('is-reset');
        void panel.offsetWidth;
        panel.classList.remove('is-reset');

        Array.prototype.forEach.call(panel.querySelectorAll('svg'), function(svg) {
            if (typeof svg.setCurrentTime === 'function') {
                try { svg.setCurrentTime(0); } catch (error) { /* SVG may not expose a timeline. */ }
            }
        });
    }

    function startActiveAnimation() {
        clearAnimationTimers();

        var activePanel = document.querySelector('[data-concept-panel="' + activeConcept + '"]');
        restartCssAnimations(activePanel);

        if (activeConcept === 'live-case') {
            var liveStep = reducedMotion ? 3 : 0;
            setLiveCaseStep(liveStep);
            if (!reducedMotion) {
                startDelay = window.setTimeout(function() {
                    activeTimer = window.setInterval(function() {
                        liveStep = (liveStep + 1) % liveCaseSteps.length;
                        setLiveCaseStep(liveStep);
                    }, 1850);
                }, 850);
            }
        }

        if (activeConcept === 'swimlane') {
            var swimStep = reducedMotion ? 5 : 0;
            setSwimlaneStep(swimStep);
            if (!reducedMotion) {
                startDelay = window.setTimeout(function() {
                    activeTimer = window.setInterval(function() {
                        swimStep = (swimStep + 1) % 6;
                        setSwimlaneStep(swimStep);
                    }, 1350);
                }, 750);
            }
        }
    }

    function selectConcept(name, moveFocus) {
        var exists = panels.some(function(panel) {
            return panel.getAttribute('data-concept-panel') === name;
        });
        if (!exists) return;

        activeConcept = name;

        tabs.forEach(function(tab) {
            var selected = tab.getAttribute('data-concept') === name;
            tab.classList.toggle('is-active', selected);
            tab.setAttribute('aria-selected', selected ? 'true' : 'false');
            tab.setAttribute('tabindex', selected ? '0' : '-1');
            if (selected && moveFocus) tab.focus();
        });

        panels.forEach(function(panel) {
            var selected = panel.getAttribute('data-concept-panel') === name;
            panel.hidden = !selected;
            panel.classList.toggle('is-active', selected);
        });

        notes.forEach(function(note) {
            note.classList.toggle('is-active', note.getAttribute('data-concept-note') === name);
        });

        if (window.history && window.history.replaceState) {
            window.history.replaceState(null, '', '#' + name);
        }

        startActiveAnimation();
    }

    tabs.forEach(function(tab, index) {
        tab.addEventListener('click', function() {
            selectConcept(tab.getAttribute('data-concept'), false);
        });

        tab.addEventListener('keydown', function(event) {
            var targetIndex = index;
            if (event.key === 'ArrowRight' || event.key === 'ArrowDown') targetIndex = (index + 1) % tabs.length;
            if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') targetIndex = (index - 1 + tabs.length) % tabs.length;
            if (event.key === 'Home') targetIndex = 0;
            if (event.key === 'End') targetIndex = tabs.length - 1;
            if (targetIndex !== index) {
                event.preventDefault();
                selectConcept(tabs[targetIndex].getAttribute('data-concept'), true);
            }
        });
    });

    if (replay) {
        replay.addEventListener('click', function() {
            startActiveAnimation();
        });
    }

    document.addEventListener('visibilitychange', function() {
        if (document.hidden) clearAnimationTimers();
        else startActiveAnimation();
    });

    var requestedConcept = window.location.hash ? window.location.hash.slice(1) : '';
    selectConcept(requestedConcept || activeConcept, false);
})();
