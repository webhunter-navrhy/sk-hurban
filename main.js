/* HURBAN – náhľad webu. Bez knižníc: natívny scroll, IntersectionObserver. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* navigácia */
  const nav = $('#nav'), burger = $('#burger');
  const onScroll = () => nav.classList.toggle('is-s', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const closeMenu = () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; };
  burger.addEventListener('click', () => {
    const open = !nav.classList.contains('is-open');
    nav.classList.toggle('is-open', open); burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  $$('#menu a').forEach(a => a.addEventListener('click', closeMenu));

  /* nadpis po slovách */
  $$('[data-words]').forEach(h => {
    let i = 0;
    const walk = el => [...el.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(t => {
          if (!t) return;
          if (/^\s+$/.test(t)) { frag.append(' '); return; }
          const w = document.createElement('span'); w.className = 'w';
          const s = document.createElement('span'); s.textContent = t; s.style.setProperty('--i', i++);
          w.append(s); frag.append(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    walk(h);
  });

  /* odhalenie pri skrolovaní */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  $$('.rv').forEach(el => io.observe(el));

  /* služby: fotka pri kurzore */
  const pv = $('#svcPv'), pvImg = pv && $('img', pv);
  if (fine && pv) {
    let x = 0, y = 0, tx = 0, ty = 0, raf = 0;
    const loop = () => {
      x += (tx - x) * .18; y += (ty - y) * .18;
      pv.style.transform = `translate(${x + 28}px, ${y - 110}px)`;
      raf = Math.abs(tx - x) + Math.abs(ty - y) > .3 ? requestAnimationFrame(loop) : 0;
    };
    $$('.svc').forEach(li => {
      li.addEventListener('mouseenter', e => {
        pvImg.src = li.dataset.img; pv.classList.add('is-on');
        if (!pv.dataset.ok) { x = tx = e.clientX; y = ty = e.clientY; pv.dataset.ok = 1; }
      });
      li.addEventListener('mouseleave', () => pv.classList.remove('is-on'));
      li.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; if (!raf) raf = requestAnimationFrame(loop); });
    });
  }

  /* zateplenie: vrstvy podľa aktívneho kroku */
  const rez = $('.rez'), steps = $$('.step');
  const setK = k => {
    steps.forEach(s => s.classList.toggle('is-on', +s.dataset.k === k));
    $$('.ly', rez).forEach(g => g.classList.toggle('on', +g.dataset.k <= k));
    $$('.lb', rez).forEach(g => { g.classList.toggle('on', +g.dataset.k <= k); g.classList.toggle('cur', +g.dataset.k === k); });
  };
  if (rez) {
    setK(0);
    const mid = matchMedia('(max-width: 900px)').matches ? '-62% 0px -30% 0px' : '-48% 0px -48% 0px';
    const so = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) setK(+e.target.dataset.k); }), { rootMargin: mid });
    steps.forEach(s => so.observe(s));
  }

  /* počítadlá */
  const fmt = n => n.toLocaleString('sk-SK').replace(/ /g, ' ');
  const co = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    co.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, t0 = performance.now(), d = 1600;
    const tick = t => {
      const p = Math.min(1, (t - t0) / d), v = Math.round(to * (1 - Math.pow(1 - p, 3)));
      el.textContent = fmt(v);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }), { threshold: .6 });
  $$('[data-count]').forEach(el => { el.textContent = '0'; co.observe(el); });

  /* lightbox */
  const lb = $('#lb'), lbImg = $('#lbImg'), lbCap = $('#lbCap'), lbFig = $('.lb__fig');
  let list = [], idx = 0, last = null;
  const show = () => {
    const n = list[idx];
    lbImg.src = `img/${n}.jpg`; lbImg.alt = FOTO[n] || ''; lbCap.textContent = FOTO[n] || '';
    // fotky sú malé skeny – zväčšiť najviac 1,3×
    const w = Math.min(343 * 1.3, innerWidth - 32);
    lbFig.style.width = `${w + 24}px`;
    $('#lbPrev').hidden = $('#lbNext').hidden = list.length < 2;
  };
  const open = (fotos, el) => {
    list = fotos.split(','); idx = 0; last = el; show();
    lb.hidden = false; document.body.style.overflow = 'hidden'; $('#lbX').focus();
  };
  const close = () => { lb.hidden = true; document.body.style.overflow = ''; last && last.focus(); };
  const step = d => { idx = (idx + d + list.length) % list.length; show(); };
  $('#lbX').addEventListener('click', close);
  $('#lbPrev').addEventListener('click', () => step(-1));
  $('#lbNext').addEventListener('click', () => step(1));
  lb.addEventListener('click', e => { if (e.target === lb) close(); });
  addEventListener('keydown', e => {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });
  // album: listovanie všetkými fotkami
  const all = $$('.ph').map(p => p.dataset.fotos);
  $$('.ph').forEach((p, i) => {
    const go = () => { open(all.join(','), p); idx = i; show(); };
    p.addEventListener('click', go);
    p.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });
  $$('.ref--f').forEach(r => {
    const go = () => open(r.dataset.fotos, r);
    r.addEventListener('click', go);
    r.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });

  /* mapa ↔ zoznam referencií */
  const rl = $('#reflist'), all2 = $('#refsAll'), pins = $$('.pin');
  let cur = null;
  const pick = o => {
    cur = cur === o ? null : o;
    rl.classList.toggle('is-f', !!cur); all2.hidden = !cur;
    $$('.ref', rl).forEach(r => r.classList.toggle('is-on', r.dataset.obec === cur));
    pins.forEach(p => p.classList.toggle('is-on', p.dataset.obec === cur));
    if (cur && matchMedia('(max-width: 1080px)').matches) {
      const first = $(`.ref[data-obec="${cur}"]`, rl);
      first && first.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };
  pins.forEach(p => {
    p.addEventListener('click', () => pick(p.dataset.obec));
    p.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(p.dataset.obec); } });
  });
  all2.addEventListener('click', () => pick(cur));
  $$('.ref', rl).forEach(r => {
    r.addEventListener('mouseenter', () => pins.forEach(p => p.classList.toggle('is-on', p.dataset.obec === r.dataset.obec || p.dataset.obec === cur)));
    r.addEventListener('mouseleave', () => pins.forEach(p => p.classList.toggle('is-on', p.dataset.obec === cur)));
  });

  /* formulár – v náhľade neodosiela */
  const form = $('#form');
  form.addEventListener('submit', e => { e.preventDefault(); $('#formNote').hidden = false; });
})();
