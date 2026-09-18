(function() {
    'use strict';

    var map = document.querySelector('[data-home-workflow-map]');
    if (!map) return;

    // Teksty stanow przychodza z HTML (data-role-label / data-task na stanie),
    // dzieki czemu kazda wersja jezykowa niesie wlasne. Ponizsza tablica jest
    // tylko zabezpieczeniem, gdyby ktoregos atrybutu zabraklo.
    var states = [
        { name: 'New',         role: 'human',   roleLabel: 'HUMAN · SERVICE COORDINATOR',        task: 'Review and assign the request' },
        { name: 'AI triage',   role: 'digital', roleLabel: 'DIGITAL WORKER · TRIAGE WORKER',     task: 'Classify, enrich and set priority' },
        { name: 'In progress', role: 'human',   roleLabel: 'HUMAN · SERVICE ENGINEER',           task: 'Investigate and resolve the issue' },
        { name: 'Waiting',     role: 'digital', roleLabel: 'DIGITAL WORKER · FOLLOW-UP WORKER',  task: 'Request missing customer information' },
        { name: 'Resolved',    role: 'human',   roleLabel: 'HUMAN · SERVICE MANAGER',            task: 'Confirm the resolution' },
        { name: 'Closed',      role: 'digital', roleLabel: 'DIGITAL WORKER · CLOSURE WORKER',    task: 'Update systems and archive the case' }
    ];

    var nodes = map.querySelectorAll('[data-home-state-index]');
    if (nodes.length) {
        var fromDom = [];
        for (var n = 0; n < nodes.length; n++) {
            var node = nodes[n];
            var roleLabel = node.getAttribute('data-role-label');
            var task = node.getAttribute('data-task');
            if (!roleLabel || !task) { fromDom = []; break; }
            var nameEl = node.querySelector('strong');
            fromDom.push({
                name: nameEl ? nameEl.textContent.trim() : '',
                role: node.querySelector('.dp-workflow-role--digital') ? 'digital' : 'human',
                roleLabel: roleLabel,
                task: task
            });
        }
        if (fromDom.length) { states = fromDom; }
    }

    // ---------------------------------------------------------------
    // Graf stanow czytany z HTML: data-home-edge="skad-dokad".
    // Dodanie krawedzi w SVG wystarczy - tutaj nie ma nic do zmiany.
    // ---------------------------------------------------------------
    var edges = {};   // "a-b" -> <path>
    var next = {};    // a -> [b, ...]

    Array.prototype.forEach.call(map.querySelectorAll('[data-home-edge]'), function(el) {
        var key = el.getAttribute('data-home-edge');
        var parts = key.split('-');
        var from = Number(parts[0]);
        var to = Number(parts[1]);
        if (isNaN(from) || isNaN(to)) return;
        edges[key] = el;
        (next[from] = next[from] || []).push(to);
    });

    var current = 0;
    var visited = {};    // stany juz odwiedzone w tym przebiegu
    var back = {};       // stany, z ktorych proces sie cofnal
    var edgeUsed = {};   // "a-b" -> 'done' | 'back'
    var lastEdge = null;
    var backTaken = false;

    function options(from) {
        return next[from] || [];
    }

    // Przy rozgalezieniu losujemy. Cofniecie moze sie zdarzyc najwyzej raz
    // na przebieg - inaczej petla potrafilaby krecic sie w kolko.
    function pick(from) {
        var all = options(from);
        if (!all.length) return null;
        var pool = [];
        for (var i = 0; i < all.length; i++) {
            if (all[i] < from && backTaken) continue;
            pool.push(all[i]);
        }
        if (!pool.length) pool = all;
        return pool[Math.floor(Math.random() * pool.length)];
    }

    function go(to) {
        var from = current;
        var key = from + '-' + to;
        visited[from] = true;
        if (to < from) {
            back[from] = true;          // bylismy tu, ale proces sie cofnal
            edgeUsed[key] = 'back';
            backTaken = true;
        } else {
            delete back[from];
            edgeUsed[key] = 'done';
        }
        delete back[to];                // wchodzimy tu ponownie - slad powrotu znika
        lastEdge = key;
        current = to;
        render();
    }

    function reset() {
        current = 0;
        visited = {};
        back = {};
        edgeUsed = {};
        lastEdge = null;
        backTaken = false;
        render();
    }

    function setText(selector, value) {
        var element = map.querySelector(selector);
        if (element) element.textContent = value;
    }

    function render() {
        var state = states[current] || states[0];

        map.setAttribute('data-step', String(current));
        map.setAttribute('data-role', state.role);

        setText('[data-home-current-state]', (state.name || '').toUpperCase());
        setText('[data-home-current-role]', state.roleLabel);
        setText('[data-home-current-task]', state.task);

        Array.prototype.forEach.call(map.querySelectorAll('[data-home-state-index]'), function(node) {
            var i = Number(node.getAttribute('data-home-state-index'));
            var active = i === current;
            node.classList.toggle('is-active', active);
            node.classList.toggle('is-back', !active && !!back[i]);
            node.classList.toggle('is-done', !active && !back[i] && !!visited[i]);
            node.classList.toggle('is-future', !active && !back[i] && !visited[i]);
        });

        for (var key in edges) {
            if (!Object.prototype.hasOwnProperty.call(edges, key)) continue;
            var used = edgeUsed[key];
            edges[key].classList.toggle('is-done', used === 'done');
            edges[key].classList.toggle('is-back', used === 'back');
            edges[key].classList.toggle('is-active', key === lastEdge);
        }
    }

    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var timer = null;
    var isVisible = true;

    function clearTimer() {
        if (!timer) return;
        window.clearTimeout(timer);
        timer = null;
    }

    function schedule(delay) {
        clearTimer();
        if (reducedMotion || document.hidden || !isVisible) return;

        timer = window.setTimeout(function() {
            if (!options(current).length) {   // stan koncowy - przebieg od nowa
                reset();
                schedule(1400);
                return;
            }
            go(pick(current));
            // Postoj w stanie jest dlugi celowo: w tym czasie ikona roli
            // pokazuje, ze ktos tu pracuje (iskry Digital Workera / babelki
            // czlowieka). Na stanie koncowym jeszcze dluzej - cala sciezka
            // jest juz narysowana i to jest pointa animacji.
            schedule(options(current).length ? 3500 : 4500);
        }, delay);
    }

    if (reducedMotion) {
        // Bez animacji pokazujemy jedna, gotowa sciezke - historia zostaje,
        // tylko nie rysuje sie na oczach.
        for (var guard = 0; guard < 4; guard++) {
            var forward = null;
            var all = options(current);
            for (var k = 0; k < all.length; k++) {
                if (all[k] > current && (forward === null || all[k] < forward)) forward = all[k];
            }
            if (forward === null) break;
            go(forward);
        }
    } else {
        render();
        schedule(1050);
    }

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
