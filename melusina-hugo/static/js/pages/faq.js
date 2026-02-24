/**
 * FAQ page — category filter & accordion behaviour
 */
(function () {
  'use strict';

  const filterBar = document.querySelector('.faq-filter-bar');
  if (!filterBar) return;

  const buttons = filterBar.querySelectorAll('[data-category]');
  const items = document.querySelectorAll('.accordion-item[data-categories]');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.category;

      // Update active pill
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Filter items
      items.forEach(item => {
        if (cat === 'all') {
          item.style.display = '';
        } else {
          const cats = (item.dataset.categories || '').split(',').map(c => c.trim().toLowerCase());
          item.style.display = cats.includes(cat.toLowerCase()) ? '' : 'none';
        }
      });
    });
  });
})();
