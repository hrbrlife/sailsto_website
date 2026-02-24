/* Melusina OS Navigation JavaScript */
(function() {
    'use strict';

    // Mobile navbar toggle
    const toggler = document.querySelector('.navbar-toggler');
    const collapse = document.querySelector('#main-navbar');
    
    if (toggler && collapse) {
        toggler.addEventListener('click', function() {
            collapse.classList.toggle('show');
            toggler.classList.toggle('collapsed');
            toggler.setAttribute('aria-expanded', collapse.classList.contains('show'));
        });
    }

    // Dropdown menus
    document.querySelectorAll('.dropdown-toggle').forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const parent = this.closest('.dropdown, .nav-item.dropdown');
            if (!parent) return;
            
            // Close other dropdowns
            document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
                if (menu.parentElement !== parent) {
                    menu.classList.remove('show');
                    menu.parentElement.classList.remove('show');
                    const t = menu.parentElement.querySelector('.dropdown-toggle');
                    if (t) t.setAttribute('aria-expanded', 'false');
                }
            });
            
            const menu = parent.querySelector('.dropdown-menu');
            if (menu) {
                menu.classList.toggle('show');
                parent.classList.toggle('show');
                this.setAttribute('aria-expanded', menu.classList.contains('show'));
            }
        });
    });

    // Close dropdowns on click outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown, .nav-item.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
                menu.classList.remove('show');
                menu.parentElement.classList.remove('show');
                const t = menu.parentElement.querySelector('.dropdown-toggle');
                if (t) t.setAttribute('aria-expanded', 'false');
            });
        }
    });

    // Close mobile nav on link click
    document.querySelectorAll('#main-navbar .nav-link:not(.dropdown-toggle)').forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992 && collapse) {
                collapse.classList.remove('show');
                toggler.classList.add('collapsed');
                toggler.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // Scroll behavior for navbar
    let lastScroll = 0;
    const navbar = document.querySelector('.neon-navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            lastScroll = currentScroll;
        }, { passive: true });
    }
})();
