// Scripts for knowledge/faq.html

// FAQ accordion — independent toggle, featured items pre-expanded
        document.querySelectorAll('.faq-question').forEach(button => {
            button.addEventListener('click', () => {
                const item = button.parentElement;
                item.classList.toggle('open');
            });
        });

        // Pre-expand featured FAQ items on page load
        document.querySelectorAll('.faq-item.featured').forEach(item => {
            item.classList.add('open');
        });
        
        // FAQ nav active state on scroll
        const faqSections = document.querySelectorAll('.faq-section[id]');
        const faqNavLinks = document.querySelectorAll('.faq-nav-link');
        
        function updateActiveFaqNav() {
            const scrollPos = window.scrollY + 200;
            
            faqSections.forEach(section => {
                const top = section.offsetTop;
                const bottom = top + section.offsetHeight;
                const id = section.getAttribute('id');
                
                if (scrollPos >= top && scrollPos < bottom) {
                    faqNavLinks.forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href') === '#' + id) {
                            link.classList.add('active');
                        }
                    });
                }
            });
        }
        
        window.addEventListener('scroll', updateActiveFaqNav);
        
        // Smooth scroll for FAQ nav
        faqNavLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
        
        // Open FAQ from URL hash
        if (window.location.hash) {
            const target = document.querySelector(window.location.hash);
            if (target) {
                setTimeout(() => {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        }
        
        // Nav scroll behavior
        window.addEventListener('scroll', () => {
            const nav = document.querySelector('nav');
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });