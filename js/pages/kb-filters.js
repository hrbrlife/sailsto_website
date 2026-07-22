/**
 * kb-filters.js — Shared Knowledge Base filtering, search, and UI utilities
 * Replaces duplicated logic across knowledge-*.js files
 * 
 * Usage: Include this script, then call KBFilters.init({ ... }) with your config.
 */
const KBFilters = (() => {

  /* ─── Nav scroll ─── */
  function initNavScroll() {
    const nav = document.querySelector('nav');
    if (!nav) return;
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  /* ─── Category / Tab filtering ─── */
  function initCategoryFilter({
    filterSelector,         // e.g. '.kb-tab', '.glossary-filter', '.blog-filter'
    cardSelector,           // e.g. '.kb-card', '.glossary-card', '.blog-card'
    categoryAttr = 'category', // data-* attribute name on cards
    sectionSelector = null, // optional parent section selector to hide when empty
    featuredSelector = null,// optional featured section to show/hide
    noResultsSelector = null,
    onFilter = null,        // optional callback after filtering
  } = {}) {
    const filters = document.querySelectorAll(filterSelector);
    const cards = document.querySelectorAll(cardSelector);
    const sections = sectionSelector ? document.querySelectorAll(sectionSelector) : [];
    const featured = featuredSelector ? document.querySelector(featuredSelector) : null;
    const noResults = noResultsSelector ? document.querySelector(noResultsSelector) : null;

    if (!filters.length || !cards.length) return null;

    function applyFilter(category) {
      let visibleCount = 0;

      // Update active state
      filters.forEach(f => f.classList.remove('active'));
      const activeFilter = [...filters].find(f => f.dataset[categoryAttr] === category);
      if (activeFilter) activeFilter.classList.add('active');

      // Filter cards
      cards.forEach(card => {
        const show = category === 'all' || card.dataset[categoryAttr] === category;
        card.style.display = show ? '' : 'none';
        if (show) visibleCount++;
      });

      // Featured section
      if (featured) {
        if (category === 'all') {
          featured.style.display = 'block';
        } else {
          // Check if featured card matches
          const featuredCard = featured.querySelector(`[data-${categoryAttr}]`);
          featured.style.display = 
            (featuredCard && featuredCard.dataset[categoryAttr] === category) ? 'block' : 'none';
        }
      }

      // Hide empty sections
      if (sections.length) {
        sections.forEach(section => {
          const visible = section.querySelectorAll(`${cardSelector}:not([style*="display: none"])`);
          section.style.display = visible.length > 0 ? 'block' : 'none';
        });
      }

      // No results
      if (noResults) {
        noResults.style.display = visibleCount === 0 ? 'block' : 'none';
      }

      if (onFilter) onFilter(category, visibleCount);
    }

    // Bind click handlers
    filters.forEach(filter => {
      filter.addEventListener('click', () => {
        applyFilter(filter.dataset[categoryAttr]);
      });
    });

    return { applyFilter, filters, cards };
  }

  /* ─── Temporal (status) filtering ─── */
  function initTemporalFilter({
    tagSelector = '.kb-temporal-tag',
    cardSelector = '.kb-card-roadmap',
    temporalAttr = 'temporal',
  } = {}) {
    const tags = document.querySelectorAll(tagSelector);
    const cards = document.querySelectorAll(cardSelector);

    if (!tags.length) return null;

    function applyFilter(temporal) {
      tags.forEach(t => t.classList.remove('active'));
      const active = [...tags].find(t => t.dataset[temporalAttr] === temporal);
      if (active) active.classList.add('active');

      cards.forEach(card => {
        card.style.display = (temporal === 'all' || card.dataset[temporalAttr] === temporal) ? '' : 'none';
      });
    }

    function reset() {
      applyFilter('all');
    }

    tags.forEach(tag => {
      tag.addEventListener('click', () => {
        applyFilter(tag.dataset[temporalAttr]);
      });
    });

    return { applyFilter, reset };
  }

  /* ─── Search ─── */
  function initSearch({
    inputSelector,
    cardSelector,
    sectionSelector = null,
    featuredSelector = null,
    noResultsSelector = null,
    minChars = 2,
    searchFields = ['textContent'],  // 'textContent', 'tags', 'temporal', 'category'
    onSearch = null,
    onReset = null,
  } = {}) {
    const input = document.querySelector(inputSelector);
    const cards = document.querySelectorAll(cardSelector);
    const sections = sectionSelector ? document.querySelectorAll(sectionSelector) : [];
    const featured = featuredSelector ? document.querySelector(featuredSelector) : null;
    const noResults = noResultsSelector ? document.querySelector(noResultsSelector) : null;

    if (!input || !cards.length) return null;

    function doSearch(query) {
      if (query.length < minChars) {
        cards.forEach(card => card.style.display = '');
        if (sections.length) sections.forEach(s => s.style.display = 'block');
        if (featured) featured.style.display = 'block';
        if (noResults) noResults.style.display = 'none';
        if (onReset) onReset();
        return;
      }

      let visibleCount = 0;
      const q = query.toLowerCase();

      cards.forEach(card => {
        let match = false;
        for (const field of searchFields) {
          if (field === 'textContent') {
            match = card.textContent.toLowerCase().includes(q);
          } else {
            const val = card.dataset[field];
            if (val && val.toLowerCase().includes(q)) match = true;
          }
          if (match) break;
        }
        card.style.display = match ? '' : 'none';
        if (match) visibleCount++;
      });

      // Hide empty sections
      if (sections.length) {
        sections.forEach(section => {
          const visible = section.querySelectorAll(`${cardSelector}:not([style*="display: none"])`);
          section.style.display = visible.length > 0 ? 'block' : 'none';
        });
      }

      if (featured) featured.style.display = 'none';
      if (noResults) noResults.style.display = visibleCount === 0 ? 'block' : 'none';
      if (onSearch) onSearch(q, visibleCount);
    }

    input.addEventListener('input', (e) => doSearch(e.target.value));

    return { doSearch, clear: () => { input.value = ''; doSearch(''); } };
  }

  /* ─── Smooth scroll ─── */
  function initSmoothScroll(linkSelector) {
    document.querySelectorAll(linkSelector).forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target && target.style.display !== 'none') {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ─── FAQ accordion ─── */
  function initAccordion({
    questionSelector = '.faq-question',
    itemSelector = '.faq-item',
    featuredClass = 'featured',
    openClass = 'open',
  } = {}) {
    document.querySelectorAll(questionSelector).forEach(button => {
      button.addEventListener('click', () => {
        button.closest(itemSelector).classList.toggle(openClass);
      });
    });

    // Pre-expand featured items
    document.querySelectorAll(`${itemSelector}.${featuredClass}`).forEach(item => {
      item.classList.add(openClass);
    });
  }

  /* ─── FAQ section nav with scroll spy ─── */
  function initScrollSpy({
    sectionSelector,
    navLinkSelector,
    offset = 200,
  } = {}) {
    const faqSections = document.querySelectorAll(sectionSelector);
    const navLinks = document.querySelectorAll(navLinkSelector);

    if (!faqSections.length || !navLinks.length) return;

    function update() {
      const scrollPos = window.scrollY + offset;
      faqSections.forEach(section => {
        const top = section.offsetTop;
        const bottom = top + section.offsetHeight;
        const id = section.getAttribute('id');
        if (scrollPos >= top && scrollPos < bottom) {
          navLinks.forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === '#' + id);
          });
        }
      });
    }

    window.addEventListener('scroll', update);

    // Handle hash on load
    if (window.location.hash) {
      const target = document.querySelector(window.location.hash);
      if (target) {
        setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
      }
    }
  }

  /* ─── Public API ─── */
  return {
    initNavScroll,
    initCategoryFilter,
    initTemporalFilter,
    initSearch,
    initSmoothScroll,
    initAccordion,
    initScrollSpy,
  };
})();
