// Scripts for knowledge/guides/getting-started.html

// Mobile navigation
        const navToggle = document.querySelector('.nav-toggle');
        const navLinks = document.querySelector('.nav-links');
        const nav = document.querySelector('nav');
        
        if (navToggle) {
            navToggle.addEventListener('click', () => {
                navToggle.classList.toggle('active');
                navLinks.classList.toggle('active');
            });
        }
        
        // Scroll effect for nav
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 60) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });