// Scripts for knowledge/faq.html

// FAQ accordion
        document.querySelectorAll('.faq-question').forEach(button => {
            button.addEventListener('click', () => {
                const item = button.parentElement;
                const isOpen = item.classList.contains('open');
                
                // Close all others in same section
                item.parentElement.querySelectorAll('.faq-item').forEach(i => {
                    i.classList.remove('open');
                });
                
                // Toggle current
                if (!isOpen) {
                    item.classList.add('open');
                }
            });
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