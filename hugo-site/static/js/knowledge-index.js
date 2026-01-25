// Scripts for knowledge/index.html

// Category tab filtering
        const tabs = document.querySelectorAll('.kb-tab');
        const sections = document.querySelectorAll('.kb-resource-section');
        const featuredSection = document.querySelector('.kb-featured');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const category = tab.dataset.category;
                
                // Update active tab
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                // Filter sections
                if (category === 'all') {
                    featuredSection.style.display = 'block';
                    sections.forEach(s => s.style.display = 'block');
                    // Reset temporal filter when showing all
                    resetTemporalFilter();
                } else {
                    featuredSection.style.display = 'none';
                    sections.forEach(s => {
                        if (s.dataset.category === category) {
                            s.style.display = 'block';
                        } else {
                            s.style.display = 'none';
                        }
                    });
                }
            });
        });
        
        // Temporal filter for roadmap
        const temporalTags = document.querySelectorAll('.kb-temporal-tag');
        const roadmapCards = document.querySelectorAll('.kb-card-roadmap');
        
        function resetTemporalFilter() {
            temporalTags.forEach(t => t.classList.remove('active'));
            temporalTags[0].classList.add('active');
            roadmapCards.forEach(card => card.style.display = '');
        }
        
        temporalTags.forEach(tag => {
            tag.addEventListener('click', () => {
                const temporal = tag.dataset.temporal;
                
                // Update active temporal tag
                temporalTags.forEach(t => t.classList.remove('active'));
                tag.classList.add('active');
                
                // Filter roadmap cards
                if (temporal === 'all') {
                    roadmapCards.forEach(card => card.style.display = '');
                } else {
                    roadmapCards.forEach(card => {
                        if (card.dataset.temporal === temporal) {
                            card.style.display = '';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                }
            });
        });
        
        // Search functionality (includes roadmap items)
        const searchInput = document.getElementById('kb-search-input');
        const allCards = document.querySelectorAll('.kb-card');
        
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            
            if (query.length < 2) {
                allCards.forEach(card => card.style.display = '');
                sections.forEach(s => s.style.display = 'block');
                featuredSection.style.display = 'block';
                resetTemporalFilter();
                return;
            }
            
            // Reset to all
            tabs.forEach(t => t.classList.remove('active'));
            tabs[0].classList.add('active');
            featuredSection.style.display = 'none';
            sections.forEach(s => s.style.display = 'block');
            resetTemporalFilter();
            
            // Filter all cards (including roadmap)
            allCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                const tags = card.dataset.tags ? card.dataset.tags.toLowerCase() : '';
                const temporal = card.dataset.temporal ? card.dataset.temporal.toLowerCase() : '';
                
                if (text.includes(query) || tags.includes(query) || temporal.includes(query)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Hide empty sections
            sections.forEach(section => {
                const visibleCards = section.querySelectorAll('.kb-card:not([style*="display: none"])');
                if (visibleCards.length === 0) {
                    section.style.display = 'none';
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