/**
 * Polaroid Line Carousel — Dalal Machine Tools Agency Pvt. Ltd.
 * Instant photos pegged to a sagging string with spring-damper physics,
 * pendulum swing dynamics, momentum drag, and procedural landscape fallbacks.
 */

(function(global) {
  'use strict';

  // Logic helpers
  function clamp(v, a, b) {
    return Math.min(b, Math.max(a, v));
  }

  function stringY(x, w, y0, sag) {
    var t = clamp(x / w, 0, 1);
    return y0 + 4 * sag * t * (1 - t);
  }

  function springStep(x, v, target, dt, k) {
    k = k || 70;
    var c = 2 * Math.sqrt(k);
    var nv = v + (k * (target - x) - c * v) * dt;
    return [x + nv * dt, nv];
  }

  function swingStep(a, w, lineVel, dt, gain) {
    var nw = w + (-38 * a - 4.2 * w + lineVel * 0.0034 * gain) * dt;
    return [clamp(a + nw * dt, -0.6, 0.6), nw];
  }

  function nearestAt(off, spacing, n) {
    return clamp(Math.round(off / spacing), 0, Math.max(0, n - 1));
  }

  function pad2(n) {
    return n < 10 ? '0' + n : String(n);
  }

  var PALETTES = {
    dawn: { top: "#e7b7a5", bottom: "#f8e8d6", sun: "#fff4df", far: "#d2b2bb", near: "#3a2a3b", mist: "255,240,232" },
    alpine: { top: "#7ea5c8", bottom: "#e3ecf2", sun: "#ffffff", far: "#a9bfd0", near: "#1c3044", mist: "236,244,250" },
    dusk: { top: "#2a2450", bottom: "#ef8d60", sun: "#ffd9a6", far: "#93607c", near: "#18121f", mist: "255,196,160" },
    mist: { top: "#c4d0cb", bottom: "#eef1ec", sun: "#ffffff", far: "#aebcb5", near: "#2c3a33", mist: "246,248,245" }
  };

  function mulberry32(seed) {
    var a = seed >>> 0;
    return function() {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function hexRgb(h) {
    var v = parseInt(h.replace("#", ""), 16);
    return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
  }

  function mixRgb(a, b, t) {
    var A = hexRgb(a);
    var B = hexRgb(b);
    return "rgb(" + A.map(function(v, i) { return Math.round(v + (B[i] - v) * t); }).join(",") + ")";
  }

  function paintLandscape(seed, palette, w, h) {
    w = w || 800;
    h = h || 800;
    var c = document.createElement("canvas");
    c.width = w;
    c.height = h;
    var g = c.getContext("2d");
    if (!g) return "";
    var P = PALETTES[palette] || PALETTES.dawn;
    var r = mulberry32(seed * 104729 + 7);

    var sky = g.createLinearGradient(0, 0, 0, h * 0.72);
    sky.addColorStop(0, P.top);
    sky.addColorStop(1, P.bottom);
    g.fillStyle = sky;
    g.fillRect(0, 0, w, h);

    var sx = w * (0.22 + r() * 0.56);
    var sy = h * (0.26 + r() * 0.16);
    var halo = g.createRadialGradient(sx, sy, 0, sx, sy, w * 0.45);
    halo.addColorStop(0, "rgba(" + hexRgb(P.sun).join(",") + ",.85)");
    halo.addColorStop(0.08, "rgba(" + hexRgb(P.sun).join(",") + ",.55)");
    halo.addColorStop(1, "rgba(" + hexRgb(P.sun).join(",") + ",0)");
    g.fillStyle = halo;
    g.fillRect(0, 0, w, h);
    g.fillStyle = P.sun;
    g.beginPath();
    g.arc(sx, sy, h * 0.045, 0, Math.PI * 2);
    g.fill();

    var layers = 5;
    for (var L = 0; L < layers; L++) {
      var k = L / (layers - 1);
      var base = h * (0.42 + k * 0.4);
      var amp = h * (0.07 + k * 0.1);
      var ph = [r(), r(), r(), r()].map(function(v) { return v * Math.PI * 2; });
      var fr = [1.3 + r(), 3.1 + r() * 2, 7 + r() * 4, 17 + r() * 8];
      var makeRidge = function(baseVal, ampVal, phArr, frArr) {
        return function(x) {
          var u = x / w;
          return (
            baseVal -
            ampVal *
              (0.55 * Math.sin(u * frArr[0] + phArr[0]) +
                0.28 * Math.sin(u * frArr[1] + phArr[1]) +
                0.12 * Math.abs(Math.sin(u * frArr[2] + phArr[2])) +
                0.05 * Math.sin(u * frArr[3] + phArr[3]))
          );
        };
      };
      var ridge = makeRidge(base, amp, ph, fr);
      var mist = g.createLinearGradient(0, base - amp * 1.4, 0, base + amp * 0.4);
      mist.addColorStop(0, "rgba(" + P.mist + ",0)");
      mist.addColorStop(1, "rgba(" + P.mist + "," + (0.55 - k * 0.35).toFixed(2) + ")");
      g.fillStyle = mist;
      g.fillRect(0, base - amp * 1.4, w, amp * 1.8);

      var body = g.createLinearGradient(0, base - amp, 0, h);
      body.addColorStop(0, mixRgb(P.far, P.near, Math.pow(k, 1.3)));
      body.addColorStop(1, mixRgb(P.far, P.near, Math.min(1, Math.pow(k, 1.3) + 0.18)));
      g.fillStyle = body;
      g.beginPath();
      g.moveTo(0, h);
      for (var x = 0; x <= w; x += 6) g.lineTo(x, ridge(x));
      g.lineTo(w, h);
      g.closePath();
      g.fill();

      if (L >= layers - 2) {
        g.fillStyle = mixRgb(P.far, P.near, Math.min(1, Math.pow(k, 1.3) + 0.08));
        for (var tx = 0; tx < w; tx += 7 + r() * 9) {
          if (r() < 0.35) continue;
          var ty = ridge(tx) + 2;
          var th = h * (0.025 + r() * 0.035) * (0.6 + k);
          var tw = th * 0.32;
          g.beginPath();
          g.moveTo(tx, ty - th);
          g.lineTo(tx + tw, ty);
          g.lineTo(tx - tw, ty);
          g.closePath();
          g.fill();
        }
      }
    }

    var vig = g.createRadialGradient(w / 2, h * 0.45, h * 0.3, w / 2, h / 2, w * 0.78);
    vig.addColorStop(0, "rgba(0,0,0,0)");
    vig.addColorStop(1, "rgba(0,0,0,.32)");
    g.fillStyle = vig;
    g.fillRect(0, 0, w, h);

    try {
      var grain = g.getImageData(0, 0, w, h);
      var d = grain.data;
      for (var i = 0; i < d.length; i += 4) {
        var v = (r() - 0.5) * 14;
        d[i] += v;
        d[i + 1] += v;
        d[i + 2] += v;
      }
      g.putImageData(grain, 0, 0);
    } catch (e) {}

    return c.toDataURL("image/jpeg", 0.88);
  }

  // Ensure CSS is injected
  var CSS_INJECTED = false;
  function injectStyles() {
    if (CSS_INJECTED) return;
    CSS_INJECTED = true;
    var style = document.createElement('style');
    style.id = 'polaroid-line-carousel-style';
    style.textContent = [
      ".pl-root{position:relative;width:100%;height:100%;overflow:hidden;background:var(--pl-bg,#101622);color:var(--pl-ink,#f8fafc);user-select:none;-webkit-user-select:none;touch-action:pan-y;outline:none;cursor:grab;border-radius:18px;border:1px solid rgba(255,255,255,0.08);box-shadow:inset 0 1px 0 rgba(255,255,255,0.06),0 28px 60px -15px rgba(0,0,0,0.65)}",
      ".pl-root[data-drag='1']{cursor:grabbing}",
      ".pl-root:focus-visible{box-shadow:inset 0 0 0 2px var(--pl-accent,#f89d13)}",
      ".pl-string{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;overflow:visible;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.4))}",
      ".pl-card{position:absolute;left:0;top:0;width:var(--pl-cw,280px);transform-origin:50% 0;will-change:transform;cursor:inherit}",
      ".pl-print{margin-top:10px;background:#fbfaf7;padding:12px 12px 0;border-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,.15),0 20px 35px -12px rgba(0,0,0,.5);transition:transform .45s cubic-bezier(.2,.7,.2,1),filter .45s ease,box-shadow .45s ease}",
      ".pl-card[data-on='0'] .pl-print{transform:scale(.88);filter:saturate(.7) brightness(.88);opacity:0.85}",
      ".pl-card[data-on='1'] .pl-print{box-shadow:0 2px 8px rgba(0,0,0,.25),0 25px 45px -10px rgba(0,0,0,.65);opacity:1}",
      ".pl-shot{position:relative;aspect-ratio:1;overflow:hidden;background:#2a3447;border-radius:2px}",
      ".pl-shot img{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:cover;display:block;pointer-events:none}",
      ".pl-zoom-badge{position:absolute;top:8px;right:8px;background:rgba(15,23,42,0.75);color:#f89d13;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;opacity:0;transition:opacity 0.25s ease;backdrop-filter:blur(4px);pointer-events:none}",
      ".pl-card:hover .pl-zoom-badge{opacity:1}",
      ".pl-note{min-height:52px;height:auto;display:flex;align-items:center;justify-content:center;text-align:center;padding:8px 10px 10px;font:italic 600 13.5px/1.35 ui-serif,Georgia,'Times New Roman',serif;color:#1e293b;white-space:normal;overflow:visible;word-break:normal;overflow-wrap:break-word}",
      ".pl-peg{position:absolute;left:50%;top:0;width:12px;height:28px;margin-left:-6px;border-radius:2px;background:linear-gradient(90deg,#b38958,#dfc399 45%,#9c7241);box-shadow:0 3px 6px rgba(0,0,0,.35);z-index:2}",
      ".pl-peg::after{content:'';position:absolute;left:5px;top:9px;width:2px;height:8px;background:rgba(60,40,20,.6);border-radius:1px}",
      ".pl-bar{position:absolute;left:clamp(16px,4vw,48px);right:clamp(16px,4vw,48px);bottom:24px;display:flex;align-items:center;gap:clamp(12px,2vw,24px);cursor:default;background:rgba(15,23,42,0.88);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,0.12);padding:14px 22px;border-radius:50px;box-shadow:0 14px 32px rgba(0,0,0,0.45);z-index:100}",
      ".pl-cap{flex:1;min-width:0;overflow:visible}",
      ".pl-title{display:block;font:700 clamp(16px,1.6vw,20px)/1.3 'Barlow',ui-serif,Georgia,serif;color:#f8fafc;white-space:normal;overflow:visible}",
      ".pl-title span{color:var(--pl-accent,#f89d13);margin-right:8px}",
      ".pl-sub{display:block;margin-top:4px;font:400 13px/1.45 system-ui,sans-serif;color:#94a3b8;white-space:normal;overflow:visible}",
      ".pl-count{font:600 13px/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;color:#94a3b8;padding:0 6px}",
      ".pl-count b{color:#f89d13;font-weight:700}",
      ".pl-controls{display:flex;align-items:center;gap:8px}",
      ".pl-btn{appearance:none;width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.06);color:#f8fafc;display:grid;place-items:center;cursor:pointer;transition:all .2s ease}",
      ".pl-btn:hover{background:#f89d13;color:#111;border-color:#f89d13;transform:scale(1.05)}",
      ".pl-btn:focus-visible{outline:2px solid #f89d13;outline-offset:2px}",
      ".pl-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}",
      "@keyframes pl-in{from{transform:translateY(8px);opacity:0}to{transform:none;opacity:1}}",
      ".pl-cap.pl-animated > *{animation:pl-in .4s cubic-bezier(.2,.8,.2,1) both}",
      "@media (max-width:767px){.pl-bar{border-radius:16px;padding:10px 14px;bottom:12px;gap:8px}.pl-sub{display:none}.pl-btn{width:32px;height:32px}}",
      "@media (prefers-reduced-motion:reduce){.pl-cap > *{animation:none}.pl-print{transition:none}}"
    ].join('\n');
    document.head.appendChild(style);
  }

  /**
   * Main Carousel Controller
   */
  function createPolaroidLineCarousel(rootElement, userOptions) {
    injectStyles();

    var options = Object.assign({
      slides: [],
      height: 680,
      cardWidth: 300,
      sag: 36,
      swing: 1.1,
      autoplay: 4500,
      string: "#c9a67a",
      background: "#0c111c",
      ink: "#f8fafc",
      accent: "#f89d13",
      onCardClick: null,
      onChange: null,
      ariaLabel: "Machinery Shipment Polaroid Carousel"
    }, userOptions || {});

    var slides = options.slides.slice();
    var n = slides.length;
    var active = 0;
    var dragging = false;
    var size = { w: 1200, h: typeof options.height === 'number' ? options.height : 680, cw: options.cardWidth };

    // Set CSS properties on root
    rootElement.classList.add('pl-root');
    rootElement.setAttribute('tabindex', '0');
    rootElement.setAttribute('role', 'region');
    rootElement.setAttribute('aria-roledescription', 'carousel');
    rootElement.setAttribute('aria-label', options.ariaLabel);
    rootElement.style.setProperty('--pl-bg', options.background);
    rootElement.style.setProperty('--pl-ink', options.ink);
    rootElement.style.setProperty('--pl-accent', options.accent);
    rootElement.style.setProperty('--pl-cw', size.cw + 'px');
    rootElement.style.height = typeof options.height === 'number' ? (options.height + 'px') : options.height;

    // Cache generated canvas images for slides missing explicit image
    var slideImgs = slides.map(function(s, idx) {
      if (s.image) return s.image;
      return paintLandscape(s.seed || (idx + 1), s.palette || 'dawn', 600, 600);
    });

    // Create SVG String
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute('class', 'pl-string');
    svg.setAttribute('aria-hidden', 'true');
    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', options.string);
    path.setAttribute('stroke-width', '2');
    path.setAttribute('stroke-linecap', 'round');
    svg.appendChild(path);
    rootElement.appendChild(svg);

    // Create Cards
    var cards = [];
    var sim = { off: 0, vel: 0, target: 0, a: [], w: [] };
    for (var k = 0; k < n; k++) {
      sim.a.push(0);
      sim.w.push(0);
    }

    var cardsWrapper = document.createDocumentFragment();
    slides.forEach(function(sl, i) {
      var card = document.createElement('div');
      card.className = 'pl-card';
      card.setAttribute('data-i', String(i));
      card.setAttribute('data-on', i === 0 ? '1' : '0');
      if (i !== 0) card.setAttribute('aria-hidden', 'true');

      var print = document.createElement('div');
      print.className = 'pl-print';

      var shot = document.createElement('div');
      shot.className = 'pl-shot';
      var img = document.createElement('img');
      img.src = slideImgs[i];
      img.alt = sl.alt || sl.title || '';
      img.draggable = false;
      img.loading = i < 5 ? 'eager' : 'lazy';
      img.onerror = function() {
        this.onerror = null;
        this.src = paintLandscape(sl.seed || (i + 1), sl.palette || 'dawn', 600, 600);
      };
      shot.appendChild(img);

      var zoomBadge = document.createElement('div');
      zoomBadge.className = 'pl-zoom-badge';
      zoomBadge.innerHTML = '<i class="fa fa-search-plus"></i>';
      shot.appendChild(zoomBadge);

      var note = document.createElement('div');
      note.className = 'pl-note';
      note.textContent = sl.title || '';

      print.appendChild(shot);
      print.appendChild(note);

      var peg = document.createElement('div');
      peg.className = 'pl-peg';

      card.appendChild(print);
      card.appendChild(peg);

      cards.push(card);
      cardsWrapper.appendChild(card);
    });
    rootElement.appendChild(cardsWrapper);

    // Create Bottom Control Bar
    var bar = document.createElement('div');
    bar.className = 'pl-bar';

    var cap = document.createElement('div');
    cap.className = 'pl-cap pl-animated';
    var titleEl = document.createElement('div');
    titleEl.className = 'pl-title';
    var subEl = document.createElement('div');
    subEl.className = 'pl-sub';
    cap.appendChild(titleEl);
    cap.appendChild(subEl);

    var countEl = document.createElement('span');
    countEl.className = 'pl-count';
    countEl.setAttribute('aria-hidden', 'true');

    var controls = document.createElement('div');
    controls.className = 'pl-controls';

    var prevBtn = document.createElement('button');
    prevBtn.type = 'button';
    prevBtn.className = 'pl-btn';
    prevBtn.setAttribute('aria-label', 'Previous Shipment');
    prevBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3 5 8l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    var nextBtn = document.createElement('button');
    nextBtn.type = 'button';
    nextBtn.className = 'pl-btn';
    nextBtn.setAttribute('aria-label', 'Next Shipment');
    nextBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    controls.appendChild(prevBtn);
    controls.appendChild(nextBtn);

    bar.appendChild(cap);
    bar.appendChild(countEl);
    bar.appendChild(controls);
    rootElement.appendChild(bar);

    var srEl = document.createElement('div');
    srEl.className = 'pl-sr';
    srEl.setAttribute('aria-live', 'polite');
    rootElement.appendChild(srEl);

    // Update bottom UI
    function updateBar(idx) {
      var s = slides[idx] || {};
      var dateBadge = s.date ? '<span style="color:#f89d13; margin-right:6px;">[' + s.date + ']</span>' : '';
      titleEl.innerHTML = dateBadge + (s.title || '');
      subEl.textContent = s.caption || s.desc || '';
      countEl.innerHTML = '<b>' + pad2(idx + 1) + '</b> / ' + pad2(n);
      srEl.textContent = 'Print ' + (idx + 1) + ' of ' + n + (s.title ? ': ' + s.title : '');

      cap.classList.remove('pl-animated');
      void cap.offsetWidth; // re-trigger animation
      cap.classList.add('pl-animated');

      cards.forEach(function(c, i) {
        c.setAttribute('data-on', i === idx ? '1' : '0');
        if (i === idx) c.removeAttribute('aria-hidden');
        else c.setAttribute('aria-hidden', 'true');
      });

      if (typeof options.onChange === 'function') {
        options.onChange(idx, s);
      }
    }

    var spacing = size.cw * 1.08;

    function updateSize() {
      var r = rootElement.getBoundingClientRect();
      var cw = Math.round(Math.max(180, Math.min(options.cardWidth, r.width * 0.38, (r.height - 240) * 0.95)));
      size = { w: r.width, h: r.height, cw: cw };
      spacing = size.cw * 1.08;
      rootElement.style.setProperty('--pl-cw', cw + 'px');
      sim.target = active * spacing;
      sim.off = active * spacing;
    }

    updateSize();
    updateBar(0);

    var ro = new ResizeObserver(updateSize);
    ro.observe(rootElement);

    var drag = null;
    var lastTouch = performance.now();

    function goTo(i) {
      var targetIdx = clamp(i, 0, n - 1);
      sim.target = targetIdx * spacing;
    }

    function step(dir) {
      lastTouch = performance.now();
      goTo(active + dir);
    }

    prevBtn.addEventListener('click', function(e) { e.stopPropagation(); step(-1); });
    nextBtn.addEventListener('click', function(e) { e.stopPropagation(); step(1); });

    rootElement.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowRight') { step(1); e.preventDefault(); }
      else if (e.key === 'ArrowLeft') { step(-1); e.preventDefault(); }
    });

    // Pointer events for drag & flick
    rootElement.addEventListener('pointerdown', function(e) {
      if (e.target.closest('.pl-bar')) return;
      lastTouch = performance.now();
      drag = {
        x: e.clientX,
        off: sim.off,
        lx: e.clientX,
        lt: e.timeStamp,
        v: 0,
        moved: false,
        pointerId: e.pointerId
      };
    });

    rootElement.addEventListener('pointermove', function(e) {
      if (!drag) return;
      var dx = e.clientX - drag.x;
      if (!drag.moved && Math.abs(dx) > 5) {
        drag.moved = true;
        dragging = true;
        rootElement.setAttribute('data-drag', '1');
        try { rootElement.setPointerCapture(e.pointerId); } catch (err) {}
      }
      if (!drag.moved) return;

      var dt = Math.max(1, e.timeStamp - drag.lt);
      drag.v = 0.7 * ((e.clientX - drag.lx) / dt) + 0.3 * drag.v;
      drag.lx = e.clientX;
      drag.lt = e.timeStamp;

      var max = (n - 1) * spacing;
      var off = drag.off - dx;
      if (off < 0) off *= 0.35;
      if (off > max) off = max + (off - max) * 0.35;
      sim.off = off;
    });

    function onPointerEnd(e) {
      if (!drag) return;
      var d = drag;
      drag = null;
      lastTouch = performance.now();

      if (d.moved) {
        dragging = false;
        rootElement.setAttribute('data-drag', '0');
        sim.vel = -d.v * 1000;
        goTo(nearestAt(sim.off - d.v * 180, spacing, n));
        return;
      }

      var cardEl = e.target.closest('[data-i]');
      if (cardEl) {
        var clickedIdx = Number(cardEl.getAttribute('data-i'));
        if (clickedIdx === active) {
          // Centered active card clicked -> trigger Zoom Lightbox!
          if (typeof options.onCardClick === 'function') {
            options.onCardClick(slides[active], active);
          } else if (typeof window.openGalleryLightbox === 'function') {
            var curr = slides[active];
            window.openGalleryLightbox(curr.image, curr.title, curr.caption || curr.desc);
          }
        } else {
          goTo(clickedIdx);
        }
      }
    }

    rootElement.addEventListener('pointerup', onPointerEnd);
    rootElement.addEventListener('pointercancel', onPointerEnd);

    // Physics Simulation loop
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var visible = true;
    var rafId = 0;
    var prevTime = performance.now();

    function frame(now) {
      rafId = 0;
      if (!visible) return;
      var dt = Math.min(0.033, (now - prevTime) / 1000);
      prevTime = now;

      var w = size.w;
      var h = size.h;
      var cw = size.cw;
      var y0 = Math.max(35, Math.min(75, Math.round(h * 0.11)));

      var lineVel = 0;
      if (drag && drag.moved) {
        lineVel = drag.v * 1000;
      } else {
        var before = sim.off;
        var sStep = springStep(sim.off, sim.vel, sim.target, dt, 70);
        sim.off = sStep[0];
        sim.vel = sStep[1];
        lineVel = -(sim.off - before) / Math.max(dt, 1e-3);
      }

      var g = reduceMotion ? 0 : options.swing;
      var near = nearestAt(sim.off, spacing, n);

      for (var i = 0; i < n; i++) {
        var el = cards[i];
        if (!el) continue;
        var x = w / 2 + i * spacing - sim.off;
        if (x < -cw * 1.5 || x > w + cw * 1.5) {
          el.style.visibility = 'hidden';
          continue;
        }
        el.style.visibility = 'visible';

        var a = sim.a[i] || 0;
        var av = sim.w[i] || 0;
        var swStep = swingStep(a, av, lineVel, dt, g);
        a = swStep[0];
        av = swStep[1];

        if (g) {
          a += Math.sin(now / 1300 + i * 1.7) * 0.0009 * g;
        }
        sim.a[i] = a;
        sim.w[i] = av;

        var y = stringY(x, w, y0, options.sag) - 6;
        el.style.transform = "translate(" + (x - cw / 2).toFixed(1) + "px," + y.toFixed(1) + "px) rotate(" + a.toFixed(4) + "rad)";
        el.style.zIndex = String(i === near ? n + 1 : n - Math.abs(i - near));
      }

      path.setAttribute("d", "M0 " + y0 + " Q" + (w / 2) + " " + (y0 + 2 * options.sag) + " " + w + " " + y0);

      if (near !== active) {
        active = near;
        updateBar(active);
      }

      rafId = requestAnimationFrame(frame);
    }

    var io = new IntersectionObserver(function(entries) {
      visible = entries[0].isIntersecting;
      if (visible && !rafId) {
        prevTime = performance.now();
        rafId = requestAnimationFrame(frame);
      }
    });
    io.observe(rootElement);
    rafId = requestAnimationFrame(frame);

    // Autoplay
    var autoTimer = null;
    if (options.autoplay && n > 1) {
      autoTimer = setInterval(function() {
        if (document.hidden || drag || (performance.now() - lastTouch < options.autoplay)) return;
        goTo(active >= n - 1 ? 0 : active + 1);
      }, options.autoplay);
    }

    // Return controller instance
    return {
      goTo: goTo,
      step: step,
      getActiveIndex: function() { return active; },
      setSlides: function(newSlides) {
        if (autoTimer) clearInterval(autoTimer);
        cancelAnimationFrame(rafId);
        ro.disconnect();
        io.disconnect();
        rootElement.innerHTML = '';
        options.slides = newSlides;
        return createPolaroidLineCarousel(rootElement, options);
      },
      destroy: function() {
        if (autoTimer) clearInterval(autoTimer);
        cancelAnimationFrame(rafId);
        ro.disconnect();
        io.disconnect();
      }
    };
  }

  global.createPolaroidLineCarousel = createPolaroidLineCarousel;
  global.paintLandscape = paintLandscape;

})(typeof window !== 'undefined' ? window : this);
