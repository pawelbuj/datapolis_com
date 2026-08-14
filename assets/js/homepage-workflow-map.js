(function() {
    'use strict';

    var map = document.querySelector('[data-home-workflow-map]');
    if (!map) return;

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

    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var step = reducedMotion ? 1 : 0;
    var timer = null;
    var isVisible = true;

    function setText(selector, value) {
        var element = map.querySelector(selector);
        if (element) element.textContent = value;
    }

    function applyStep(nextStep) {
        step = Math.max(0, Math.min(nextStep, states.length - 1));
        var current = states[step];

        map.setAttribute('data-step', String(step));
        map.setAttribute('data-role', current.role);

        setText('[data-home-current-state]', current.name.toUpperCase());
        setText('[data-home-current-role]', current.roleLabel);
        setText('[data-home-current-task]', current.task);

        Array.prototype.forEach.call(map.querySelectorAll('[data-home-state-index]'), function(node) {
            var index = Number(node.getAttribute('data-home-state-index'));
            node.classList.toggle('is-done', index < step);
            node.classList.toggle('is-active', index === step);
            node.classList.toggle('is-future', index > step);
        });

        Array.prototype.forEach.call(map.querySelectorAll('[data-home-edge-index]'), function(edge) {
            var index = Number(edge.getAttribute('data-home-edge-index'));
            edge.classList.toggle('is-done', index < step - 1);
            edge.classList.toggle('is-active', step > 0 && index === step - 1);
        });
    }

    function clearTimer() {
        if (!timer) return;
        window.clearTimeout(timer);
        timer = null;
    }

    function schedule(delay) {
        clearTimer();
        if (reducedMotion || document.hidden || !isVisible) return;

        timer = window.setTimeout(function() {
            applyStep((step + 1) % states.length);
            schedule(step === states.length - 1 ? 2450 : 1750);
        }, delay);
    }

    applyStep(step);
    schedule(1050);

    document.addEventListener('visibilitychange', function() {
        if (document.hidden) clearTimer();
        else schedule(700);
    });

    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function(entries) {
            isVisible = entries[0] ? entries[0].isIntersecting : true;
            if (isVisible) schedule(700);
            else clearTimer();
        }, { threshold: 0.15 });

        observer.observe(map);
    }
})();
