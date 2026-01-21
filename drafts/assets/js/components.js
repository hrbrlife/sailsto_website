/**
 * Sails.to Component Loader
 * Loads header and footer templates from a single source of truth
 * 
 * Usage: Add this script to your page and include placeholder elements:
 *   <div id="site-header"></div>
 *   <div id="site-footer"></div>
 * 
 * Or use data attributes on existing elements:
 *   <header data-component="header"></header>
 *   <footer data-component="footer"></footer>
 */

(function() {
    'use strict';

    // Calculate the path to root based on current page location
    function getBasePath() {
        const path = window.location.pathname;
        const depth = (path.match(/\//g) || []).length - 1;
        
        // Handle different folder depths
        // Root: /index.html -> ""
        // /company/about.html -> "../"
        // /knowledge/blog/post.html -> "../../"
        
        if (depth <= 1) return '';
        return '../'.repeat(depth - 1);
    }

    // Get assets path (for loading templates)
    function getAssetsPath() {
        return getBasePath() + 'assets/';
    }

    // Replace {{ROOT}} placeholders with actual path
    function processTemplate(html, basePath) {
        return html.replace(/\{\{ROOT\}\}/g, basePath);
    }

    // Load a component template
    async function loadComponent(name) {
        const assetsPath = getAssetsPath();
        const templatePath = `${assetsPath}templates/${name}.html`;
        
        try {
            const response = await fetch(templatePath);
            if (!response.ok) {
                throw new Error(`Failed to load ${name} template: ${response.status}`);
            }
            const html = await response.text();
            return processTemplate(html, getBasePath());
        } catch (error) {
            console.error(`Error loading component "${name}":`, error);
            return null;
        }
    }

    // Initialize mobile navigation after header loads
    function initNavigation() {
        const nav = document.querySelector('nav');
        const navToggle = document.querySelector('.nav-toggle');
        const navLinks = document.querySelector('.nav-links');
        const navDropdowns = document.querySelectorAll('.nav-dropdown');
        const isMobile = window.innerWidth <= 768;

        if (navToggle && navLinks) {
            navToggle.addEventListener('click', () => {
                navToggle.classList.toggle('active');
                navLinks.classList.toggle('active');
            });
        }

        // Mobile dropdown toggle
        navDropdowns.forEach(dropdown => {
            const trigger = dropdown.querySelector('.nav-dropdown-trigger');
            if (trigger) {
                trigger.addEventListener('click', (e) => {
                    if (isMobile) {
                        e.preventDefault();
                        dropdown.classList.toggle('active');
                    }
                });
            }
        });

        // Mark current page as active
        const currentPath = window.location.pathname;
        const navLinksAll = document.querySelectorAll('nav a');
        navLinksAll.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.endsWith(href.replace(/^\.\.\//, '').replace(/^\.\//, ''))) {
                link.classList.add('active');
            }
        });
    }

    // Check if nav should be in dark mode (for pages with dark hero sections)
    function checkNavDarkMode() {
        const nav = document.querySelector('nav');
        if (!nav) return;

        // Check if page has data-nav-dark attribute on body or html
        if (document.body.dataset.navDark === 'true' || 
            document.documentElement.dataset.navDark === 'true') {
            nav.classList.add('nav-dark');
        }

        // Or check for dark hero section
        const hero = document.querySelector('.hero, .hero-dark, [data-hero-dark]');
        if (hero) {
            // Scroll-based nav color change
            const handleScroll = () => {
                const heroBottom = hero.offsetTop + hero.offsetHeight;
                if (window.scrollY < heroBottom - 100) {
                    nav.classList.add('nav-dark');
                } else {
                    nav.classList.remove('nav-dark');
                }
            };
            
            window.addEventListener('scroll', handleScroll, { passive: true });
            handleScroll(); // Initial check
        }
    }

    // Main initialization
    async function init() {
        const basePath = getBasePath();
        
        // Find header placeholder
        const headerEl = document.getElementById('site-header') || 
                         document.querySelector('[data-component="header"]');
        
        // Find footer placeholder  
        const footerEl = document.getElementById('site-footer') || 
                         document.querySelector('[data-component="footer"]');

        // Load components in parallel
        const [headerHtml, footerHtml] = await Promise.all([
            headerEl ? loadComponent('header') : null,
            footerEl ? loadComponent('footer') : null
        ]);

        // Insert header
        if (headerEl && headerHtml) {
            headerEl.outerHTML = headerHtml;
            initNavigation();
            checkNavDarkMode();
        }

        // Insert footer
        if (footerEl && footerHtml) {
            footerEl.outerHTML = footerHtml;
        }

        // Dispatch event when components are loaded
        document.dispatchEvent(new CustomEvent('componentsLoaded', {
            detail: { header: !!headerHtml, footer: !!footerHtml }
        }));
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for manual use
    window.SailsComponents = {
        loadComponent,
        getBasePath,
        getAssetsPath,
        init
    };

})();
