(function() {
    'use strict';

    var states = [
        {
            name: 'New',
            role: 'human',
            roleLabel: 'HUMAN · SERVICE COORDINATOR',
            task: 'Review and assign the request'
        },
        {
            name: 'AI triage',
            role: 'digital',
            roleLabel: 'DIGITAL WORKER · TRIAGE WORKER',
            task: 'Classify, enrich and set priority'
        },
        {
            name: 'In progress',
            role: 'human',
            roleLabel: 'HUMAN · SERVICE ENGINEER',
            task: 'Investigate and resolve the issue'
        },
        {
            name: 'Waiting',
            role: 'digital',
            roleLabel: 'DIGITAL WORKER · FOLLOW-UP WORKER',
            task: 'Request missing customer information'
        },
        {
            name: 'Resolved',
            role: 'human',
            roleLabel: 'HUMAN · SERVICE MANAGER',
            task: 'Confirm the resolution'
        },
        {
            name: 'Closed',
            role: 'digital',
            roleLabel: 'DIGITAL WORKER · CLOSURE WORKER',
            task: 'Update systems and archive the case'
        }
    ];

    var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-concept]'));
    var panels = Array.prototype.slice.call(document.querySelectorAll('[data-concept-panel]'));
    var notes = Array.prototype.slice.call(document.querySelectorAll('[data-concept-note]'));
    var replay = document.querySelector('.hac-replay');
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var activeConcept = 'journey';
    var activeTimer = null;
    var activeStep = 0;

    function clearAnimationTimer() {
        if (activeTimer) {
            window.clearTimeout(activeTimer);
            activeTimer = null;
        }
    }

    function setText(panel, selector, text) {
        Array.prototype.forEach.call(panel.querySelectorAll(selector), function(element) {
            element.textContent = text;
        });
    }

    function applyStep(panel, step) {
        if (!panel) return;

        var visual = panel.querySelector('[data-process-animation]');
        if (!visual) return;

        var safeStep = Math.max(0, Math.min(step, states.length - 1));
        var current = states[safeStep];
        var progress = (safeStep / (states.length - 1)) * 100;

        visual.setAttribute('data-step', String(safeStep));
        visual.setAttribute('data-role', current.role);
        visual.style.setProperty('--process-progress', progress + '%');

        setText(panel, '[data-current-state]', current.name.toUpperCase());
        setText(panel, '[data-current-role]', current.roleLabel);
        setText(panel, '[data-current-task]', current.task);
        setText(panel, '[data-state-counter]', String(safeStep + 1).padStart(2, '0') + ' / 06');

        Array.prototype.forEach.call(panel.querySelectorAll('[data-progress-fill]'), function(fill) {
            fill.style.width = progress + '%';
        });

        Array.prototype.forEach.call(panel.querySelectorAll('[data-state-index]'), function(node) {
            var index = Number(node.getAttribute('data-state-index'));
            node.classList.toggle('is-done', index < safeStep);
            node.classList.toggle('is-active', index === safeStep);
            node.classList.toggle('is-future', index > safeStep);
        });

        Array.prototype.forEach.call(panel.querySelectorAll('[data-edge-index]'), function(edge) {
            var index = Number(edge.getAttribute('data-edge-index'));
            edge.classList.toggle('is-done', index < safeStep - 1);
            edge.classList.toggle('is-active', safeStep > 0 && index === safeStep - 1);
        });
    }

    function restartCssAnimations(panel) {
        if (!panel) return;
        panel.classList.add('is-reset');
        void panel.offsetWidth;
        panel.classList.remove('is-reset');
    }

    function scheduleNextStep() {
        if (reducedMotion || document.hidden) return;

        var delay = activeStep === states.length - 1 ? 2450 : 1750;
        activeTimer = window.setTimeout(function() {
            activeStep = (activeStep + 1) % states.length;
            var activePanel = document.querySelector('[data-concept-panel="' + activeConcept + '"]');
            applyStep(activePanel, activeStep);
            scheduleNextStep();
        }, delay);
    }

    function startActiveAnimation() {
        clearAnimationTimer();

        var panel = document.querySelector('[data-concept-panel="' + activeConcept + '"]');
        activeStep = reducedMotion ? 2 : 0;
        restartCssAnimations(panel);
        applyStep(panel, activeStep);

        if (!reducedMotion) {
            activeTimer = window.setTimeout(function() {
                activeStep = 1;
                applyStep(panel, activeStep);
                scheduleNextStep();
            }, 950);
        }
    }

    function selectConcept(name, focusTab) {
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
            if (selected && focusTab) tab.focus();
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
        if (document.hidden) clearAnimationTimer();
        else startActiveAnimation();
    });

    var requestedConcept = window.location.hash ? window.location.hash.slice(1) : '';
    selectConcept(requestedConcept || activeConcept, false);
})();
