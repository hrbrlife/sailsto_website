// Issuers Directory Filter functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterPills = document.querySelectorAll('.filter-pill');
    const cards = document.querySelectorAll('.issuer-card');
    const countEl = document.getElementById('count');

    let activeFilters = {
        structure: 'all',
        trust: []
    };

    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const filterType = pill.dataset.filter;
            const filterValue = pill.dataset.value;

            if (filterType === 'trust') {
                // Toggle trust filters
                pill.classList.toggle('active');
                if (pill.classList.contains('active')) {
                    activeFilters.trust.push(filterValue);
                } else {
                    activeFilters.trust = activeFilters.trust.filter(v => v !== filterValue);
                }
            } else {
                // Radio-style for structure
                document.querySelectorAll(`.filter-pill[data-filter="${filterType}"]`).forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                activeFilters[filterType] = filterValue;
            }

            applyFilters();
        });
    });

    function applyFilters() {
        let visibleCount = 0;

        cards.forEach(card => {
            let show = true;

            // Structure filter
            if (activeFilters.structure !== 'all') {
                if (card.dataset.structure !== activeFilters.structure) {
                    show = false;
                }
            }

            // Trust filters (AND logic)
            if (activeFilters.trust.includes('audited') && card.dataset.audited !== 'true') {
                show = false;
            }
            if (activeFilters.trust.includes('regulated') && card.dataset.regulated !== 'true') {
                show = false;
            }

            card.style.display = show ? 'block' : 'none';
            if (show) visibleCount++;
        });

        countEl.textContent = visibleCount;
    }
});
