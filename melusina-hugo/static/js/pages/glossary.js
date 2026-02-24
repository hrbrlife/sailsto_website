/**
 * Glossary page — category filter, search, and view toggle
 */
(function () {
  'use strict';

  /* ── Category filter ── */
  const filterBar = document.querySelector('.glossary-filter-bar');
  const cards = document.querySelectorAll('.glossary-card[data-category]');

  if (filterBar) {
    const buttons = filterBar.querySelectorAll('[data-category]');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const cat = btn.dataset.category;

        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        cards.forEach(card => {
          if (cat === 'all') {
            card.closest('.col') && (card.closest('.col').style.display = '');
            card.style.display = '';
          } else {
            const match = card.dataset.category === cat;
            if (card.closest('.col')) {
              card.closest('.col').style.display = match ? '' : 'none';
            } else {
              card.style.display = match ? '' : 'none';
            }
          }
        });

        updateCount();
      });
    });
  }

  /* ── Search ── */
  const searchInput = document.querySelector('.glossary-search');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase().trim();

      cards.forEach(card => {
        const title = (card.querySelector('.card-title') || card).textContent.toLowerCase();
        const def = (card.querySelector('.card-text') || card).textContent.toLowerCase();
        const match = !query || title.includes(query) || def.includes(query);

        if (card.closest('.col')) {
          card.closest('.col').style.display = match ? '' : 'none';
        } else {
          card.style.display = match ? '' : 'none';
        }
      });

      updateCount();
    });
  }

  /* ── Count update ── */
  function updateCount() {
    const visible = document.querySelectorAll('.glossary-card[data-category]');
    let count = 0;
    visible.forEach(c => {
      const el = c.closest('.col') || c;
      if (el.style.display !== 'none') count++;
    });
    const counter = document.querySelector('.glossary-count');
    if (counter) counter.textContent = count + ' term' + (count !== 1 ? 's' : '');
  }
})();
