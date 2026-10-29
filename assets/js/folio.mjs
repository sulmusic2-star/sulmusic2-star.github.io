const views = {search: {src: '/assets/product/lasting-ground-search.png', alt: 'Actual Lasting Ground public search interface, captured October 28, 2026.', caption: 'Actual public interface · 28 October 2026'}, preview: {src: '/assets/product/lasting-ground-preview.png', alt: 'Actual public preview for 78 Main Street, Hudson, Massachusetts. Questions are listed; answers and supporting records require access.', caption: 'Public preview · access required; the mobile capture also shows an unfinished elevation check'}};
for (const gallery of document.querySelectorAll('[data-product-gallery]')) {
  const img = gallery.querySelector('[data-product-image]');
  const caption = gallery.querySelector('[data-capture-caption]');
  const full = gallery.querySelector('[data-full-image]');
  for (const button of gallery.querySelectorAll('[data-capture]')) { button.disabled = false; button.addEventListener('click', () => {
    const view = views[button.dataset.capture]; if (!view) return;
    img.src = view.src; img.alt = view.alt; full.href = view.src;
    gallery.querySelector('[data-mobile-capture]').srcset = view.src.replace('.png', '-mobile.png');
    full.setAttribute('aria-label', 'Open full-size ' + (button.dataset.capture === 'search' ? 'Lasting Ground search capture' : 'Lasting Ground address preview'));
    caption.textContent = view.caption;
    for (const item of gallery.querySelectorAll('[data-capture]')) item.setAttribute('aria-pressed', String(item === button));
  }); }
}

for (const example of document.querySelectorAll('[data-source-example]')) {
  try {
    const response = await fetch('/assets/product/source-example.json');
    if (!response.ok) throw new Error('Sample unavailable');
    const data = await response.json();
    for (const button of example.querySelectorAll('[data-scenario]')) {
      button.disabled = false;
      button.addEventListener('click', () => {
        const sample = data.cases[button.dataset.scenario]; if (!sample) return;
        example.querySelector('[data-permit-state]').textContent = button.dataset.scenario === 'original' ? 'Missing' : 'Validated';
        example.querySelector('[data-warning-output]').textContent = sample.sections.find(x => x.title === 'What stays uncertain').body;
        const list = example.querySelector('[data-warning-list]'); list.replaceChildren();
        for (const lane of sample.validation.lane_checks.filter(x => x.warning)) { const li = document.createElement('li'); li.textContent = lane.label + ': ' + lane.warning; list.append(li); }
        for (const item of example.querySelectorAll('[data-scenario]')) item.setAttribute('aria-pressed', String(item === button));
      });
    }
  } catch { example.querySelector('[data-example-error]').hidden = false; }
}
