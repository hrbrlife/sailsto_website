// Scripts for knowledge/index.html — uses kb-filters.js

KBFilters.initNavScroll();

const temporal = KBFilters.initTemporalFilter({
  tagSelector: '.kb-temporal-tag',
  cardSelector: '.kb-card-roadmap',
});

KBFilters.initCategoryFilter({
  filterSelector: '.kb-tab',
  cardSelector: '.kb-resource-section',
  sectionSelector: null,
  featuredSelector: '.kb-featured',
  onFilter: (category) => {
    const sections = document.querySelectorAll('.kb-resource-section');
    if (category === 'all') {
      sections.forEach(s => s.style.display = 'block');
      if (temporal) temporal.reset();
    } else {
      sections.forEach(s => {
        s.style.display = s.dataset.category === category ? 'block' : 'none';
      });
    }
  },
});

KBFilters.initSearch({
  inputSelector: '#kb-search-input',
  cardSelector: '.kb-card',
  sectionSelector: '.kb-resource-section',
  featuredSelector: '.kb-featured',
  searchFields: ['textContent', 'tags', 'temporal'],
  onReset: () => {
    if (temporal) temporal.reset();
    document.querySelectorAll('.kb-tab').forEach((t, i) => {
      t.classList.toggle('active', i === 0);
    });
  },
  onSearch: () => {
    if (temporal) temporal.reset();
    document.querySelectorAll('.kb-tab').forEach((t, i) => {
      t.classList.toggle('active', i === 0);
    });
  },
});