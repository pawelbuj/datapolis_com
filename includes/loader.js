// Loader for header and footer
(function() {
    'use strict';
    
    var loadedComponents = {
        header: false,
        footer: false
    };
    
    // Function to load HTML content
    function loadHTML(elementId, filePath, componentName) {
        fetch(filePath)
            .then(response => {
                if (!response.ok) {
                    throw new Error('HTTP error! status: ' + response.status);
                }
                return response.text();
            })
            .then(data => {
                const element = document.getElementById(elementId);
                if (element) {
                    element.innerHTML = data;
                    loadedComponents[componentName] = true;
                    
                    // Check if both components are loaded
                    if (loadedComponents.header && loadedComponents.footer) {
                        // Trigger custom event when all content is loaded
                        const event = new CustomEvent('includesLoaded');
                        document.dispatchEvent(event);
                        
                        // Reinitialize scripts after content is loaded
                        reinitializeScripts();
                    }
                }
            })
            .catch(error => {
                console.error('Error loading ' + filePath + ':', error);
            });
    }
    
    // Reinitialize JavaScript functions after loading header/footer
    function reinitializeScripts() {
        // Wait a bit for DOM to settle
        setTimeout(function() {
            // Reinitialize menu dropdowns
            if (typeof window.initMenu === 'function') {
                window.initMenu();
            }
            
            // Dispatch a custom event that main.js can listen to
            var event = new Event('headerLoaded');
            document.dispatchEvent(event);
            
            // Try to manually initialize common components
            initializeComponents();
        }, 100);
    }
    
    // Manual initialization of common components
    function initializeComponents() {
        // Initialize dropdown menus
        var dropdowns = document.querySelectorAll('.js-dropdown');
        dropdowns.forEach(function(dropdown) {
            var trigger = dropdown.querySelector('.js-dropdown-trigger');
            if (trigger && !trigger.hasAttribute('data-initialized')) {
                trigger.setAttribute('data-initialized', 'true');
                trigger.addEventListener('click', function(e) {
                    e.preventDefault();
                    dropdown.classList.toggle('is-active');
                });
            }
        });
        
        // Initialize language switcher buttons
        var langButtons = document.querySelectorAll('.dropdown-links__item button');
        langButtons.forEach(function(btn) {
            if (!btn.hasAttribute('data-lang-initialized')) {
                btn.setAttribute('data-lang-initialized', 'true');
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    e.preventDefault();
                    var btnText = btn.textContent.trim();
                    if (btnText === 'PL') {
                        window.location.href = '/PL/index.html';
                    } else if (btnText === 'EN') {
                        window.location.href = '/index.html';
                    }
                });
            }
        });
        
        // Initialize menu items with submenus
        var menuItems = document.querySelectorAll('.js-menu-item');
        menuItems.forEach(function(item) {
            var link = item.querySelector('a');
            var submenu = item.querySelector('.js-menu-sub');
            
            if (link && submenu && !item.hasAttribute('data-initialized')) {
                item.setAttribute('data-initialized', 'true');
                
                link.addEventListener('click', function(e) {
                    // On mobile/tablet, toggle submenu
                    if (window.innerWidth <= 1024) {
                        e.preventDefault();
                        item.classList.toggle('is-active');
                        
                        // Close other open menus
                        menuItems.forEach(function(otherItem) {
                            if (otherItem !== item) {
                                otherItem.classList.remove('is-active');
                            }
                        });
                    }
                });
            }
        });
        
        // Initialize mobile menu
        var mobileMenuBtn = document.querySelector('.js-mobile-menu');
        var body = document.body;
        
        if (mobileMenuBtn && !mobileMenuBtn.hasAttribute('data-initialized')) {
            mobileMenuBtn.setAttribute('data-initialized', 'true');
            mobileMenuBtn.addEventListener('click', function() {
                body.classList.toggle('mobile-menu-open');
            });
        }
    }
    
    // Load header and footer when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            loadHTML('header-placeholder', 'includes/header.html', 'header');
            loadHTML('footer-placeholder', 'includes/footer.html', 'footer');
        });
    } else {
        loadHTML('header-placeholder', 'includes/header.html', 'header');
        loadHTML('footer-placeholder', 'includes/footer.html', 'footer');
    }
})();
