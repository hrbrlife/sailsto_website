// Scripts for knowledge/glossary/index.html

// Search functionality
        const searchInput = document.getElementById('glossary-search-input');
        const cards = document.querySelectorAll('.glossary-card');
        const letterSections = document.querySelectorAll('.glossary-letter-section');
        const noResults = document.querySelector('.glossary-no-results');
        
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            let visibleCount = 0;
            
            if (query.length < 1) {
                cards.forEach(card => card.style.display = '');
                letterSections.forEach(s => s.style.display = 'block');
                noResults.style.display = 'none';
                return;
            }
            
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = '';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Hide empty letter sections
            letterSections.forEach(section => {
                const visibleCards = section.querySelectorAll('.glossary-card:not([style*="display: none"])');
                section.style.display = visibleCards.length > 0 ? 'block' : 'none';
            });
            
            // Show/hide no results
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        });
        
        // Category filter functionality
        const filters = document.querySelectorAll('.glossary-filter');
        
        filters.forEach(filter => {
            filter.addEventListener('click', () => {
                const category = filter.dataset.category;
                
                // Update active state
                filters.forEach(f => f.classList.remove('active'));
                filter.classList.add('active');
                
                // Clear search
                searchInput.value = '';
                
                // Filter cards
                let visibleCount = 0;
                
                cards.forEach(card => {
                    if (category === 'all' || card.dataset.category === category) {
                        card.style.display = '';
                        visibleCount++;
                    } else {
                        card.style.display = 'none';
                    }
                });
                
                // Hide empty letter sections
                letterSections.forEach(section => {
                    const visibleCards = section.querySelectorAll('.glossary-card:not([style*="display: none"])');
                    section.style.display = visibleCards.length > 0 ? 'block' : 'none';
                });
                
                noResults.style.display = visibleCount === 0 ? 'block' : 'none';
            });
        });
        
        // Smooth scroll for alphabet links
        document.querySelectorAll('.alpha-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target && target.style.display !== 'none') {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
        
        // Nav scroll behavior
        window.addEventListener('scroll', () => {
            const nav = document.querySelector('nav');
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });