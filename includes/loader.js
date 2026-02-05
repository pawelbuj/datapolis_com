// Loader for header and footer - Datapolis.com
(function() {
    'use strict';

    var loadedComponents = { header: false, footer: false };

    // --- Language detection (used early for loading correct includes) ---
    function normalizeLangFromPath(pathname) {
        var p = (pathname || '').toLowerCase();
        // Handle both with and without trailing slash (for cleanUrls support)
        if (p === '/pl' || p.indexOf('/pl/') === 0) return 'pl';
        if (p === '/de' || p.indexOf('/de/') === 0) return 'de';
        if (p === '/es' || p.indexOf('/es/') === 0) return 'es';
        return 'en';
    }

    function currentPageFromPath(pathname, lang) {
        var p = pathname || '/';
        // If directory root ("/" or "/pl", "/pl/", etc.), return empty string for index
        if (p === '/' || p === '/pl' || p === '/de' || p === '/es' ||
            p === '/pl/' || p === '/de/' || p === '/es/') return '';

        var segments = p.split('/').filter(Boolean);
        if (!segments.length) return '';

        // If the first segment is a language folder, drop it
        if (lang !== 'en' && segments[0].toLowerCase() === lang) segments.shift();

        // If no segments left after removing language, it's the index page
        if (!segments.length) return '';

        var last = segments[segments.length - 1] || '';
        // Remove .html extension if present (for clean URLs)
        if (last.endsWith('.html')) {
            last = last.slice(0, -5);
        }
        return last;
    }

    // Load HTML content
    function loadHTML(elementId, filePath, componentName) {
        var element = document.getElementById(elementId);
        if (!element) return;

        fetch(filePath)
            .then(function(response) {
                if (!response.ok) throw new Error('HTTP ' + response.status);
                return response.text();
            })
            .then(function(html) {
                element.innerHTML = html;
                loadedComponents[componentName] = true;

                if (componentName === 'header') {
                    // Small delay to ensure DOM is ready
                    requestAnimationFrame(function() {
                        requestAnimationFrame(initNavigation);
                    });
                }

                if (loadedComponents.header && loadedComponents.footer) {
                    document.dispatchEvent(new CustomEvent('includesLoaded'));
                }
            })
            .catch(function(err) {
                console.error('Load error:', filePath, err);
            });
    }

    // =========================================
    // NAVIGATION INITIALIZATION
    // =========================================
    function initNavigation() {
        var header = document.querySelector('.dp-header');
        if (!header || header.dataset.init) return;
        header.dataset.init = 'true';

        var body = document.body;
        var hoverTimeout = null;

        function setActiveLang(lang) {
            var current = header.querySelector('.dp-lang__current');
            if (current) current.textContent = (lang || 'en').toUpperCase();

            // Desktop dropdown
            header.querySelectorAll('.dp-lang__option').forEach(function(a) {
                var aLang = (a.getAttribute('data-lang') || a.textContent || '').toLowerCase();
                a.classList.toggle('dp-lang__option--active', aLang === lang);
            });
            // Mobile footer
            header.querySelectorAll('.dp-mobile-menu__lang-opt').forEach(function(a) {
                var aLang = (a.getAttribute('data-lang') || a.textContent || '').toLowerCase();
                a.classList.toggle('dp-mobile-menu__lang-opt--active', aLang === lang);
            });
        }

        function updateLangLinks() {
            var lang = normalizeLangFromPath(window.location.pathname);
            var page = currentPageFromPath(window.location.pathname, lang);

            // Generate clean URLs: "/" for index, "/page" for others
            var targets = {
                en: page ? '/' + page : '/',
                pl: '/pl/' + page,
                de: '/de/' + page,
                es: '/es/' + page
            };

            header.querySelectorAll('.dp-lang__option, .dp-mobile-menu__lang-opt').forEach(function(a) {
                var aLang = (a.getAttribute('data-lang') || a.textContent || '').toLowerCase();
                if (targets[aLang]) a.setAttribute('href', targets[aLang]);
            });

            setActiveLang(lang);
        }

        // --- Scroll effect ---
        function onScroll() {
            header.classList.toggle('is-scrolled', window.scrollY > 40);
        }
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();

        // --- Desktop dropdowns ---
        var dropdownItems = header.querySelectorAll('.dp-nav__item--has-dropdown');

        dropdownItems.forEach(function(item) {
            var trigger = item.querySelector('.dp-nav__link');
            var dropdown = item.querySelector('.dp-dropdown');
            if (!trigger || !dropdown) return;

            var menuItems = dropdown.querySelectorAll('.dp-dropdown__item');

            function open() {
                // Close others
                dropdownItems.forEach(function(other) {
                    if (other !== item && other.classList.contains('is-open')) {
                        other.classList.remove('is-open');
                        var otherTrigger = other.querySelector('.dp-nav__link');
                        if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
                    }
                });
                item.classList.add('is-open');
                trigger.setAttribute('aria-expanded', 'true');
            }

            function close() {
                item.classList.remove('is-open');
                trigger.setAttribute('aria-expanded', 'false');
            }

            // Hover
            item.addEventListener('mouseenter', function() {
                clearTimeout(hoverTimeout);
                open();
            });

            item.addEventListener('mouseleave', function() {
                hoverTimeout = setTimeout(close, 120);
            });

            // Click toggle
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                item.classList.contains('is-open') ? close() : open();
            });

            // Keep open when hovering dropdown
            dropdown.addEventListener('mouseenter', function() {
                clearTimeout(hoverTimeout);
            });
            dropdown.addEventListener('mouseleave', function() {
                hoverTimeout = setTimeout(close, 120);
            });

            // Keyboard: Enter/Space on trigger
            trigger.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    item.classList.contains('is-open') ? close() : open();
                }
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    if (!item.classList.contains('is-open')) open();
                    if (menuItems && menuItems.length) menuItems[0].focus();
                }
            });

            // Keyboard: Arrow navigation inside dropdown
            menuItems.forEach(function(link, index) {
                link.addEventListener('keydown', function(e) {
                    if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        var next = menuItems[index + 1] || menuItems[0];
                        next.focus();
                    } else if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        var prev = menuItems[index - 1] || menuItems[menuItems.length - 1];
                        prev.focus();
                    } else if (e.key === 'Escape') {
                        e.preventDefault();
                        close();
                        trigger.focus();
                    }
                });
            });
        });

        // --- Language dropdown ---
        var langDropdown = header.querySelector('.dp-lang');
        if (langDropdown) {
            var langTrigger = langDropdown.querySelector('.dp-lang__trigger');

            function openLang() {
                langDropdown.classList.add('is-open');
                if (langTrigger) langTrigger.setAttribute('aria-expanded', 'true');
            }
            function closeLang() {
                langDropdown.classList.remove('is-open');
                if (langTrigger) langTrigger.setAttribute('aria-expanded', 'false');
            }

            langDropdown.addEventListener('mouseenter', openLang);
            langDropdown.addEventListener('mouseleave', closeLang);

            if (langTrigger) {
                langTrigger.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    langDropdown.classList.contains('is-open') ? closeLang() : openLang();
                });
            }
        }

        // Update language links after header is injected
        updateLangLinks();

        // --- Mobile menu ---
        var hamburger = header.querySelector('.dp-hamburger');
        var mobileMenu = header.querySelector('.dp-mobile-menu');

        function openMobile() {
            if (!hamburger || !mobileMenu) return;
            hamburger.classList.add('is-active');
            hamburger.setAttribute('aria-expanded', 'true');
            (function() {
                var lang = normalizeLangFromPath(window.location.pathname);
                var labels = {
                    en: 'Close menu',
                    pl: 'Zamknij menu',
                    de: 'Menü schließen',
                    es: 'Cerrar menú'
                };
                hamburger.setAttribute('aria-label', labels[lang] || labels.en);
            })();
            mobileMenu.classList.add('is-open');
            mobileMenu.setAttribute('aria-hidden', 'false');
            // Inline display override ensures visibility even if cached CSS still hides it.
            mobileMenu.style.display = 'block';
            body.style.overflow = 'hidden';
        }

        function closeMobile() {
            if (!hamburger || !mobileMenu) return;
            hamburger.classList.remove('is-active');
            hamburger.setAttribute('aria-expanded', 'false');
            (function() {
                var lang = normalizeLangFromPath(window.location.pathname);
                var labels = {
                    en: 'Open menu',
                    pl: 'Otwórz menu',
                    de: 'Menü öffnen',
                    es: 'Abrir menú'
                };
                hamburger.setAttribute('aria-label', labels[lang] || labels.en);
            })();
            mobileMenu.classList.remove('is-open');
            mobileMenu.setAttribute('aria-hidden', 'true');
            mobileMenu.style.display = '';
            body.style.overflow = '';
        }

        if (hamburger) {
            hamburger.addEventListener('click', function(e) {
                e.stopPropagation();
                mobileMenu && mobileMenu.classList.contains('is-open') ? closeMobile() : openMobile();
            });
        }

        // Mobile accordion
        var mobileTriggers = header.querySelectorAll('.dp-mobile-nav__trigger');
        mobileTriggers.forEach(function(trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                var item = trigger.closest('.dp-mobile-nav__item');
                if (!item) return;

                var isOpen = item.classList.contains('is-open');

                // Close others
                header.querySelectorAll('.dp-mobile-nav__item.is-open').forEach(function(openItem) {
                    if (openItem !== item) {
                        openItem.classList.remove('is-open');
                        var t = openItem.querySelector('.dp-mobile-nav__trigger');
                        if (t) t.setAttribute('aria-expanded', 'false');
                    }
                });

                item.classList.toggle('is-open');
                trigger.setAttribute('aria-expanded', isOpen ? 'false' : 'true');
            });
        });

        // Close mobile on link click
        if (mobileMenu) {
            mobileMenu.querySelectorAll('a').forEach(function(link) {
                link.addEventListener('click', function() {
                    setTimeout(closeMobile, 80);
                });
            });
        }

        // --- Global: ESC key ---
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                // Close desktop dropdowns
                dropdownItems.forEach(function(item) {
                    item.classList.remove('is-open');
                    var t = item.querySelector('.dp-nav__link');
                    if (t) t.setAttribute('aria-expanded', 'false');
                });
                // Close lang
                if (langDropdown) {
                    langDropdown.classList.remove('is-open');
                    var lt = langDropdown.querySelector('.dp-lang__trigger');
                    if (lt) lt.setAttribute('aria-expanded', 'false');
                }
                // Close mobile
                closeMobile();
            }
        });

        // --- Global: Click outside ---
        document.addEventListener('click', function(e) {
            // Desktop dropdowns
            if (!e.target.closest('.dp-nav__item--has-dropdown')) {
                dropdownItems.forEach(function(item) {
                    item.classList.remove('is-open');
                    var t = item.querySelector('.dp-nav__link');
                    if (t) t.setAttribute('aria-expanded', 'false');
                });
            }
            // Lang dropdown
            if (langDropdown && !e.target.closest('.dp-lang')) {
                langDropdown.classList.remove('is-open');
                var lt = langDropdown.querySelector('.dp-lang__trigger');
                if (lt) lt.setAttribute('aria-expanded', 'false');
            }
        });

        // --- Resize: close mobile if large ---
        window.addEventListener('resize', function() {
            if (window.innerWidth > 1100) {
                closeMobile();
            }
        });
    }

    // =========================================
    // INIT
    // =========================================
    function init() {
        // Detect current language to load correct header/footer
        var lang = normalizeLangFromPath(window.location.pathname);
        
        // Use absolute paths to ensure correct loading regardless of URL structure
        var basePath = (lang === 'en') ? '/includes/' : '/' + lang + '/includes/';
        
        loadHTML('header-placeholder', basePath + 'header.html', 'header');
        loadHTML('footer-placeholder', basePath + 'footer.html', 'footer');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
