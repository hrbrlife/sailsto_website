/* ═══════════════════════════════════════════════════════════════
   SAILS.TO - NAVIGATION JAVASCRIPT
   Mobile toggle, dropdown handling, scroll behavior, accessibility
═══════════════════════════════════════════════════════════════ */

(function() {
    'use strict';
    
    // DOM Elements
    const nav = document.querySelector('nav');
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    const dropdowns = document.querySelectorAll('.nav-dropdown');
    const dropdownTriggers = document.querySelectorAll('.nav-dropdown-trigger');
    
    // Scroll behavior - add scrolled class for transparent nav
    let lastScroll = 0;
    const handleScroll = () => {
        const currentScroll = window.scrollY;
        
        if (currentScroll > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    };
    
    // Mobile nav toggle
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
            navToggle.setAttribute('aria-expanded', 
                navToggle.classList.contains('active') ? 'true' : 'false'
            );
        });
    }
    
    // Mobile dropdown toggle (on click)
    const handleMobileDropdown = (e) => {
        if (window.innerWidth <= 768) {
            const dropdown = e.target.closest('.nav-dropdown');
            if (dropdown) {
                e.preventDefault();
                dropdown.classList.toggle('active');
                
                // Update ARIA
                const trigger = dropdown.querySelector('.nav-dropdown-trigger');
                if (trigger) {
                    trigger.setAttribute('aria-expanded', 
                        dropdown.classList.contains('active') ? 'true' : 'false'
                    );
                }
            }
        }
    };
    
    // Keyboard support for dropdown triggers
    dropdownTriggers.forEach(trigger => {
        trigger.addEventListener('click', handleMobileDropdown);
        
        trigger.addEventListener('keydown', (e) => {
            // Enter or Space to toggle
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleMobileDropdown(e);
            }
            // Escape to close
            if (e.key === 'Escape') {
                const dropdown = trigger.closest('.nav-dropdown');
                if (dropdown) {
                    dropdown.classList.remove('active');
                    trigger.setAttribute('aria-expanded', 'false');
                }
            }
        });
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!e.target.closest('.nav-links') && !e.target.closest('.nav-toggle')) {
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        }
    });
    
    // Close mobile menu on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            navLinks.classList.remove('active');
            navToggle.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
            
            dropdowns.forEach(dropdown => {
                dropdown.classList.remove('active');
                const trigger = dropdown.querySelector('.nav-dropdown-trigger');
                if (trigger) {
                    trigger.setAttribute('aria-expanded', 'false');
                }
            });
        }
    });
    
    // Initialize
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // Run once on load
    
    // Set initial ARIA states
    if (navToggle) {
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-controls', 'nav-links');
    }
    
    dropdownTriggers.forEach(trigger => {
        trigger.setAttribute('aria-expanded', 'false');
    });
    
})();
