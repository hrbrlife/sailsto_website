/* ═══════════════════════════════════════════════════════════════
   SAILS.TO - HOME PAGE JAVASCRIPT
   Hero parallax effect, editorial columns reveal animation
═══════════════════════════════════════════════════════════════ */

(function() {
    'use strict';
    
    // Respect reduced motion preferences
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    
    const heroEditorial = document.getElementById('heroEditorial');
    const editorialParagraphs = heroEditorial ? heroEditorial.querySelectorAll('p, .editorial-header .line1, .editorial-header .line2') : [];
    const editorialSection = document.querySelector('.editorial-section');
    const windowHeight = window.innerHeight;
    const isMobile = window.innerWidth <= 768;
    
    // Get the height of the editorial columns
    const columnsHeight = heroEditorial ? heroEditorial.offsetHeight : 300;
    
    // Scroll handler for parallax effect
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        // Skip parallax on mobile - CSS handles it
        if (isMobile) return;
        
        // Editorial columns parallax (desktop only)
        if (heroEditorial && editorialSection) {
            // Calculate where columns should "land" - top of editorial section
            const sectionTop = editorialSection.offsetTop;
            const landingScroll = sectionTop - windowHeight + columnsHeight + 40;
            
            if (scrolled < landingScroll) {
                // Phase 1: Fixed, revealing
                heroEditorial.style.position = 'fixed';
                heroEditorial.style.bottom = '0';
                heroEditorial.style.top = 'auto';
                
                // Reveal: 50% -> 0%
                const revealProgress = Math.min(1, scrolled / (windowHeight * 0.5));
                const translateY = Math.max(0, 50 - (revealProgress * 50));
                heroEditorial.style.transform = `translateY(${translateY}%)`;
            } else {
                // Phase 2: Absolute, locked in place at top of white section
                heroEditorial.style.position = 'absolute';
                heroEditorial.style.bottom = 'auto';
                heroEditorial.style.top = `${sectionTop + 40}px`;
                heroEditorial.style.transform = 'none';
            }
            
            // Color: turn black quickly
            const colorProgress = Math.min(1, scrolled / (windowHeight * 0.3));
            const colorValue = Math.round(255 - (255 - 35) * colorProgress);
            const color = `rgb(${colorValue}, ${colorValue}, ${colorValue})`;
            
            // Shadow: fade out as we scroll
            const shadowOpacity = Math.max(0, 0.5 - (colorProgress * 0.5));
            const shadowBlur = Math.max(0, 4 - (colorProgress * 4));
            const shadow = shadowOpacity > 0 ? `0 2px ${shadowBlur}px rgba(0,0,0,${shadowOpacity})` : 'none';
            
            editorialParagraphs.forEach(p => {
                p.style.color = color;
                p.style.textShadow = shadow;
            });
        }
    });
})();
