/* ==========================================================
   BOOKIFY · Book reader
   - Reads the pages from <template id="pages">
   - Double mode (PC and landscape tablet) or single (phone and portrait tablet)
   - 3D page turn, keyboard, click, swipe, link to a page (#12)
   No libraries needed.
   ========================================================== */
{
  const PW = 440, PH = 660, BAR = 64, MARGIN = 14;
  const src = [...document.getElementById('pages').content.children];
  const book = document.getElementById('book');
  const scaler = document.getElementById('scaler');
  const $ = id => document.getElementById(id);
  let mode = null, sheets = [], step = 0, busy = false, pages = [];

  // Page index for each id (for internal links)
  const byId = {};
  src.forEach((p, i) => { if (p.id) byId[p.id] = i; });

  const isDouble = () => {
    const w = innerWidth, h = innerHeight;
    return w > h && w >= 900 && h >= 500;
  };

  const face = (page, cls) => {
    const f = document.createElement('div');
    f.className = 'face ' + cls;
    if (page) f.appendChild(page.cloneNode(true)); else f.classList.add('empty');
    return f;
  };

  // Current step -> first visible page
  const pageOfStep = s => mode === 'double' ? Math.max(0, 2 * s - 1) : s;
  const stepOfPage = i => mode === 'double' ? Math.ceil(i / 2) : i;
  const total = () => mode === 'double' ? sheets.length : pages.length - 1;

  function mount(goTo) {
    mode = isDouble() ? 'double' : 'single';
    book.className = mode;
    book.querySelectorAll('.sheet').forEach(s => s.remove());
    sheets = [];
    // Single mode does not show filler blank pages
    pages = mode === 'double' ? src : src.filter(p => !p.classList.contains('blank'));
    if (mode === 'double') {
      for (let i = 0; i < pages.length; i += 2) {
        const s = document.createElement('div');
        s.className = 'sheet';
        s.append(face(pages[i], 'front r'), face(pages[i + 1], 'rear l'));
        sheets.push(s);
      }
    } else {
      pages.forEach(p => {
        const s = document.createElement('div');
        s.className = 'sheet';
        s.append(face(p, 'front r'), face(null, 'rear l'));
        sheets.push(s);
      });
    }
    sheets.forEach(s => book.appendChild(s));
    const idx = Math.max(0, pages.indexOf(src[goTo] ?? src[0]));
    step = Math.min(stepOfPage(idx), total());
    paint(false);
    fit();
  }

  function paint(animate, dir) {
    const n = sheets.length;
    sheets.forEach((s, i) => {
      const turned = i < step;
      s.classList.toggle('no-anim', !animate);
      s.classList.toggle('turned', turned);
      s.style.zIndex = turned ? i + 1 : n - i;
      const near = Math.abs(i - step) <= 2 || (animate && Math.abs(i - step) <= 3);
      s.classList.toggle('far', !near);
    });
    if (animate) {
      const i = dir > 0 ? step - 1 : step;
      const s = sheets[i];
      if (s) {
        s.style.zIndex = 999;
        s.classList.add('turning');
        busy = true;
        setTimeout(() => {
          s.classList.remove('turning');
          s.style.zIndex = s.classList.contains('turned') ? i + 1 : n - i;
          busy = false;
        }, parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--turn')) || 700);
      }
    }
    if (document.body.classList.contains('short')) $('desk').scrollTop = 0;
    // Closed book: center the cover or the back cover
    let dx = 0;
    if (mode === 'double') {
      if (step === 0) dx = -PW / 2;
      else if (step === n && pages.length % 2 === 0) dx = PW / 2;
    }
    book.style.transform = `translateX(${dx}px)`;
    // Bases and page edges
    const remaining = mode === 'double' ? n - step : n - step - 1;
    const read = step;
    const bl = book.querySelector('.base.left'), br = book.querySelector('.base.right');
    br.classList.toggle('shown', remaining > 0 || mode === 'single');
    bl.classList.toggle('shown', mode === 'double' && read > 0);
    const edge = (k, s) => {
      const c = Math.min(6, Math.ceil(k / 6));
      const out = [];
      for (let j = 1; j <= c; j++) out.push(`${s * j * 1.5}px ${j * 0.6}px 0 ${j % 2 ? '#d9d9d9' : '#fbfbfb'}`);
      return out.join(',') || '0 0 0 transparent';
    };
    br.style.setProperty('--edge-r', edge(remaining, 1));
    bl.style.setProperty('--edge-l', edge(read, -1));
    // Bar
    const p0 = pageOfStep(step);
    const num = el => el?.dataset.n || '';
    let txt;
    if (mode === 'double' && step > 0 && step < n) {
      const a = num(pages[p0]), b = num(pages[p0 + 1]);
      txt = [a, b].filter(Boolean).join('–') || '·';
    } else txt = num(pages[mode === 'double' && step === n ? pages.length - 1 : p0]) || (step === 0 ? UI.cover : step >= total() ? UI.end : '·');
    $('pos').textContent = txt;
    $('prev').disabled = step === 0;
    $('next').disabled = step >= total();
    $('progress').style.width = (100 * step / Math.max(1, total())) + '%';
    const real = src.indexOf(pages[p0]);
    history.replaceState(null, '', real > 0 ? '#' + (pages[p0].dataset.n || real) : location.pathname + location.search);
  }

  function go(s, animate = true) {
    s = Math.max(0, Math.min(total(), s));
    if (s === step || busy) return;
    const dir = s > step ? 1 : -1;
    const jump = Math.abs(s - step) > 1;
    step = s;
    paint(animate && !jump, dir);
  }
  const next = () => go(step + 1), prev = () => go(step - 1);
  const goPage = i => go(stepOfPage(Math.max(0, pages.indexOf(src[i]))), true);

  function fit() {
    const w = mode === 'double' ? PW * 2 : PW;
    const aw = innerWidth - MARGIN * 2, ah = innerHeight - BAR - MARGIN * 2;
    // Phone in landscape: the page fills the width and is read by scrolling down
    const short = mode === 'single' && innerHeight < 500;
    document.body.classList.toggle('short', short);
    const s = short ? Math.min((innerWidth * 0.64) / PW, 1.3) : Math.min(aw / w, ah / PH, 1.7);
    scaler.style.transform = `scale(${s})`;
    scaler.style.width = w + 'px';
    scaler.style.height = PH + 'px';
    const frame = $('frame');
    frame.style.width = w * s + 'px';
    frame.style.height = PH * s + 'px';
  }

  // Events
  $('next').onclick = next; $('prev').onclick = prev;
  $('toc-btn').onclick = () => { const i = byId['contents']; if (i != null) goPage(i); };
  addEventListener('keydown', e => {
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') go(0, false);
    else if (e.key === 'End') go(total(), false);
  });
  // Internal links (contents) and clicks on the page edges
  book.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (a) {
      const h = a.getAttribute('href') || '';
      if (h.startsWith('#') && byId[h.slice(1)] != null) { e.preventDefault(); goPage(byId[h.slice(1)]); }
      return;
    }
    if (swiped) return;
    const r = book.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    if (mode === 'double') { x > .5 ? next() : prev(); } else { x > .35 ? next() : prev(); }
  });
  // Swipe
  let x0 = null, y0 = 0, swiped = false;
  addEventListener('pointerdown', e => { x0 = e.clientX; y0 = e.clientY; swiped = false; });
  addEventListener('pointerup', e => {
    if (x0 == null) return;
    const dx = e.clientX - x0, dy = e.clientY - y0;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3) { swiped = true; dx < 0 ? next() : prev(); setTimeout(() => swiped = false, 50); }
    x0 = null;
  });
  let resizeTimer;
  addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      const current = src.indexOf(pages[pageOfStep(step)]);
      if ((isDouble() ? 'double' : 'single') !== mode) mount(current); else fit();
    }, 120);
  });
  addEventListener('hashchange', () => {
    const n = location.hash.slice(1);
    const i = src.findIndex(p => p.dataset.n === n);
    if (i >= 0 && i !== src.indexOf(pages[pageOfStep(step)])) goPage(i);
  });

  // Start: honor the #page number in the link
  const h = location.hash.slice(1);
  const start = Math.max(0, src.findIndex(p => p.dataset.n === h));
  mount(start);
  document.fonts?.ready?.then(fit);

  // Check mode: open the book with ?check to see which pages overflow (exact measurement)
  if (/[?&]check\b/.test(location.search)) {
    (document.fonts?.ready || Promise.resolve()).then(() => {
      const box = document.createElement('div');
      box.style.cssText = 'position:absolute;left:-99999px;top:0';
      document.body.appendChild(box);
      const bad = [];
      src.forEach(p => {
        if (p.classList.contains('cover')) return;
        const c = p.cloneNode(true); box.appendChild(c);
        const extra = c.scrollHeight - c.clientHeight, wide = c.scrollWidth - c.clientWidth;
        if (extra > 1 || wide > 1) { p.classList.add('overflow'); bad.push({ n: p.dataset.n || '·', extra, wide, i: src.indexOf(p) }); }
      });
      box.remove();
      const panel = document.createElement('div');
      panel.id = 'check-panel';
      panel.innerHTML = bad.length
        ? '<b>' + (bad.length === 1 ? UI.one_overflows : UI.n_overflow.replace('{n}', bad.length)) + '</b> ' + bad.map(m => `<button data-i="${m.i}">${UI.page_abbr} ${m.n} (+${m.extra}px)</button>`).join(' ')
        : '<b>' + UI.check + '</b> ' + UI.all_fit;
      document.body.appendChild(panel);
      panel.addEventListener('click', e => { const b = e.target.closest('button'); if (b) goPage(+b.dataset.i); });
      console.log('[check]', bad.length ? bad : 'every page fits');
      mount(src.indexOf(pages[pageOfStep(step)]));
    });
  }
}
