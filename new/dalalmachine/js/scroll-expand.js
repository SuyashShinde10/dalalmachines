/**
 * ScrollExpand.js - Ultra-Smooth, Lag-Free Vanilla JS Implementation
 * Optimized for 60/120fps hardware acceleration with zero layout thrashing
 */
(function(window, document) {
  'use strict';

  var clamp = function(v, a, b) {
    return v < a ? a : v > b ? b : v;
  };

  var smoothstep = function(edge0, edge1, x) {
    var t = clamp((x - edge0) / (edge1 - edge0 || 1e-6), 0, 1);
    return t * t * (3 - 2 * t);
  };

  function ScrollExpand(element, userOptions) {
    if (!element) return;

    var isMobile = window.innerWidth < 768;
    var defaults = {
      startWidth: isMobile ? 92 : 72,
      startHeight: isMobile ? 66 : 56,
      startRadius: isMobile ? 18 : 24,
      endRadius: 0,
      mediaZoom: 1.30,
      scrollDistance: 1.15,
      holdDistance: 0.30,
      lerpSpeed: 0.28, // Snappy 60fps tracking: zero lag feeling, instantly responsive
      overlayScrim: 0.82,
      useWindowScroll: true,
      enabled: true
    };

    var options = Object.assign({}, defaults, userOptions || {});

    var track = element.querySelector('.scroll-expand__track');
    var stage = element.querySelector('.scroll-expand__stage');
    var frame = element.querySelector('.scroll-expand__frame');
    var media = element.querySelector('.scroll-expand__media');
    var title = element.querySelector('.scroll-expand__title');
    var overlay = element.querySelector('.scroll-expand__overlay');
    var scrim = element.querySelector('.scroll-expand__scrim');
    var hint = element.querySelector('.scroll-expand__hint');

    if (!track || !stage || !frame || !media) return;

    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var rafId = 0;
    var current = 0;
    var target = 0;
    var stageH = 0;
    var trackTop = 0;
    var span = 0;
    var running = false;
    var lastP = -1;

    var applyProgress = function(p) {
      if (Math.abs(p - lastP) < 0.0001 && p !== 0 && p !== 1) return;
      lastP = p;

      var e = smoothstep(0, 1, p);

      var w = options.startWidth + (100 - options.startWidth) * e;
      var h = options.startHeight + (100 - options.startHeight) * e;
      var ix = Math.max(0, (100 - w) / 2);
      var iy = Math.max(0, (100 - h) / 2);
      var r = options.startRadius * (1 - e);

      // Fast hardware-accelerated clip path
      var clipStr = 'inset(' + iy.toFixed(2) + '% ' + ix.toFixed(2) + '% ' + iy.toFixed(2) + '% ' + ix.toFixed(2) + '% round ' + r.toFixed(1) + 'px)';
      frame.style.clipPath = clipStr;
      frame.style.webkitClipPath = clipStr;

      // GPU transform for zoom
      var currentZoom = options.mediaZoom + (1 - options.mediaZoom) * e;
      media.style.transform = 'translate3d(0, 0, 0) scale(' + currentZoom.toFixed(3) + ')';

      if (scrim) {
        scrim.style.opacity = (options.overlayScrim * e).toFixed(3);
      }

      if (title) {
        var out = smoothstep(0.20, 0.70, p);
        title.style.opacity = (1 - out).toFixed(3);
        title.style.transform = 'translate3d(0, ' + (-36 * out).toFixed(1) + 'px, 0)';
        title.style.pointerEvents = out > 0.4 ? 'none' : 'auto';
      }

      if (hint) {
        var gone = smoothstep(0, 0.12, p);
        hint.style.opacity = (1 - gone).toFixed(3);
        hint.style.transform = 'translate3d(0, ' + (12 * gone).toFixed(1) + 'px, 0)';
      }

      if (overlay) {
        var inn = smoothstep(0.55, 0.95, p);
        overlay.style.opacity = inn.toFixed(3);
        overlay.style.transform = 'translate3d(0, ' + (20 * (1 - inn)).toFixed(1) + 'px, 0)';
        overlay.style.pointerEvents = inn > 0.5 ? 'auto' : 'none';
      }
    };

    var measure = function() {
      var mobileNow = window.innerWidth < 768;
      options.startWidth = mobileNow ? 92 : 72;
      options.startHeight = mobileNow ? 66 : 56;
      options.startRadius = mobileNow ? 18 : 24;

      stageH = options.useWindowScroll ? window.innerHeight : element.clientHeight;
      if (stageH <= 0) return;

      stage.style.height = stageH + 'px';
      span = stageH * Math.max(0.01, options.scrollDistance);
      var totalH = stageH * (1 + Math.max(0, options.scrollDistance) + Math.max(0, options.holdDistance));
      track.style.height = totalH + 'px';

      // Accurately measure track absolute top position ONCE on resize/measure to avoid layout thrashing on scroll
      var rect = track.getBoundingClientRect();
      var scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
      trackTop = rect.top + scrollY;

      var w = element.clientWidth || stageH;
      stage.style.setProperty('--se-title-size', clamp(w * 0.065, 22, 64) + 'px');
    };

    var readProgress = function() {
      if (!options.enabled || span <= 0) return 1;
      if (options.useWindowScroll) {
        var rect = track.getBoundingClientRect();
        return clamp(-rect.top / span, 0, 1);
      }
      return clamp(element.scrollTop / span, 0, 1);
    };

    var tick = function() {
      var diff = target - current;
      if (Math.abs(diff) < 0.0004) {
        current = target;
        running = false;
      } else {
        // High-frequency snappy lerp: instant responsiveness, zero perceived lag
        current += diff * options.lerpSpeed;
      }

      applyProgress(current);

      if (running) {
        rafId = requestAnimationFrame(tick);
      } else {
        rafId = 0;
      }
    };

    var kick = function() {
      if (running) return;
      running = true;
      if (!rafId) rafId = requestAnimationFrame(tick);
    };

    var onScroll = function() {
      target = readProgress();
      if (reduceMotion) {
        current = target;
        applyProgress(current);
        return;
      }
      kick();
    };

    var onResize = function() {
      measure();
      target = readProgress();
      current = target;
      applyProgress(current);
    };

    measure();
    target = readProgress();
    current = target;
    applyProgress(current);

    var scroller = options.useWindowScroll ? window : element;
    scroller.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);

    // Re-check position after fonts and images finish layout
    window.addEventListener('load', function() {
      measure();
      target = readProgress();
      current = target;
      applyProgress(current);
    });

    if (window.ResizeObserver) {
      var ro = new ResizeObserver(onResize);
      ro.observe(element);
    }
  }

  // Auto-initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      var targets = document.querySelectorAll('.scroll-expand');
      for (var i = 0; i < targets.length; i++) {
        new ScrollExpand(targets[i]);
      }
    });
  } else {
    var targets = document.querySelectorAll('.scroll-expand');
    for (var i = 0; i < targets.length; i++) {
      new ScrollExpand(targets[i]);
    }
  }

  window.ScrollExpand = ScrollExpand;
})(window, document);
