// Scripts for knowledge/blog/index.html

// Category filter functionality
        const filters = document.querySelectorAll('.blog-filter');
        const cards = document.querySelectorAll('.blog-card');
        const featuredCard = document.querySelector('.blog-featured-card');
        const noResults = document.querySelector('.blog-no-results');
        const blogFeatured = document.querySelector('.blog-featured');
        
        filters.forEach(filter => {
            filter.addEventListener('click', () => {
                const category = filter.dataset.category;
                
                // Update active state
                filters.forEach(f => f.classList.remove('active'));
                filter.classList.add('active');
                
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
                
                // Handle featured card
                if (category === 'all' || featuredCard.dataset.category === category) {
                    blogFeatured.style.display = 'block';
                    visibleCount++;
                } else {
                    blogFeatured.style.display = 'none';
                }
                
                noResults.style.display = visibleCount === 0 ? 'block' : 'none';
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