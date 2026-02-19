// Scripts for knowledge/glossary/index.html — uses kb-filters.js

KBFilters.initNavScroll();

const glossarySearch = KBFilters.initSearch({
  inputSelector: '#glossary-search-input',
  cardSelector: '.glossary-card',
  sectionSelector: '.glossary-letter-section',
  noResultsSelector: '.glossary-no-results',
  minChars: 1,
});

KBFilters.initCategoryFilter({
  filterSelector: '.glossary-filter',
  cardSelector: '.glossary-card',
  sectionSelector: '.glossary-letter-section',
  noResultsSelector: '.glossary-no-results',
  onFilter: () => {
    // Clear search when category changes
    if (glossarySearch) glossarySearch.clear();
  },
});

KBFilters.initSmoothScroll('.alpha-link');