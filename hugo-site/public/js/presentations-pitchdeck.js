// Scripts for presentations/pitchdeck.html

// Slide navigation
        let currentSlide = 1;
        const totalSlides = 13;
        
        function updateSlide(slideNumber) {
            currentSlide = slideNumber;
            document.querySelector('.slide-counter .current').textContent = currentSlide;
            document.getElementById('prevSlide').disabled = currentSlide === 1;
            document.getElementById('nextSlide').disabled = currentSlide === totalSlides;
            
            const targetSlide = document.querySelector(`[data-slide="${currentSlide}"]`);
            if (targetSlide) {
                targetSlide.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
        
        document.getElementById('prevSlide').addEventListener('click', () => {
            if (currentSlide > 1) updateSlide(currentSlide - 1);
        });
        
        document.getElementById('nextSlide').addEventListener('click', () => {
            if (currentSlide < totalSlides) updateSlide(currentSlide + 1);
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                e.preventDefault();
                if (currentSlide < totalSlides) updateSlide(currentSlide + 1);
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                if (currentSlide > 1) updateSlide(currentSlide - 1);
            }
        });
        
        // Track scroll position to update slide counter
        const slides = document.querySelectorAll('.slide');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const slideNum = parseInt(entry.target.getAttribute('data-slide'));
                    currentSlide = slideNum;
                    document.querySelector('.slide-counter .current').textContent = currentSlide;
                    document.getElementById('prevSlide').disabled = currentSlide === 1;
                    document.getElementById('nextSlide').disabled = currentSlide === totalSlides;
                }
            });
        }, { threshold: 0.5 });
        
        slides.forEach(slide => observer.observe(slide));
        
        // Initialize Mermaid
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'base',
            themeVariables: {
                primaryColor: '#C9A227',
                primaryTextColor: '#0A0A0A',
                primaryBorderColor: '#8A8A8A',
                lineColor: '#4A4A4A',
                secondaryColor: '#EDE8DC',
                tertiaryColor: '#F7F5ED'
            }
        });