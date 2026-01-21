// Loader for header and footer - Datapolis.com
(function() {
    'use strict';

    var loadedComponents = { header: false, footer: false };

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
            });
        });

        // --- Language dropdown ---
        var langDropdown = header.querySelector('.dp-lang');
        if (langDropdown) {
            var langTrigger = langDropdown.querySelector('.dp-lang__trigger');
            var langMenu = langDropdown.querySelector('.dp-lang__dropdown');

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

        // --- Mobile menu ---
        var hamburger = header.querySelector('.dp-hamburger');
        var mobileMenu = header.querySelector('.dp-mobile-menu');

        function openMobile() {
            if (!hamburger || !mobileMenu) return;
            hamburger.classList.add('is-active');
            hamburger.setAttribute('aria-expanded', 'true');
            hamburger.setAttribute('aria-label', 'Close menu');
            mobileMenu.classList.add('is-open');
            mobileMenu.setAttribute('aria-hidden', 'false');
            body.style.overflow = 'hidden';
        }

        function closeMobile() {
            if (!hamburger || !mobileMenu) return;
            hamburger.classList.remove('is-active');
            hamburger.setAttribute('aria-expanded', 'false');
            hamburger.setAttribute('aria-label', 'Open menu');
            mobileMenu.classList.remove('is-open');
            mobileMenu.setAttribute('aria-hidden', 'true');
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
        loadHTML('header-placeholder', 'includes/header.html', 'header');
        loadHTML('footer-placeholder', 'includes/footer.html', 'footer');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
