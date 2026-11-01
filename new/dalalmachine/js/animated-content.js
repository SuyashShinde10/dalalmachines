/**
 * AnimatedContent - React Bits Component Adapter for Dalal Machine Tools
 * Variant: JavaScript + CSS (GSAP + ScrollTrigger)
 * 
 * Mirrors the exact props, wipes, and physics of React Bits <AnimatedContent />:
 * - distance, direction, reverse, duration, ease, initialOpacity, animateOpacity
 * - scale, blur, rotate, tilt, wipe ('up'|'down'|'left'|'right'|'center')
 * - threshold, delay, stagger, staggerFrom, trigger ('scroll'|'mount'), once, scrub
 * - prefers-reduced-motion compliance and automatic cleanup
 */

(function (window, document) {
  'use strict';

  var WIPES = {
    up: 'linear-gradient(to top, #000 calc(var(--ac-wipe) * 140% - 40%), transparent calc(var(--ac-wipe) * 140%))',
    down: 'linear-gradient(to bottom, #000 calc(var(--ac-wipe) * 140% - 40%), transparent calc(var(--ac-wipe) * 140%))',
    left: 'linear-gradient(to left, #000 calc(var(--ac-wipe) * 140% - 40%), transparent calc(var(--ac-wipe) * 140%))',
    right: 'linear-gradient(to right, #000 calc(var(--ac-wipe) * 140% - 40%), transparent calc(var(--ac-wipe) * 140%))',
    center: 'radial-gradient(farthest-corner at 50% 50%, #000 calc(var(--ac-wipe) * 140% - 40%), transparent calc(var(--ac-wipe) * 140%))'
  };

  function parseBool(val, defaultVal) {
    if (val === undefined || val === null) return defaultVal;
    if (val === 'true' || val === true || val === '') return true;
    if (val === 'false' || val === false) return false;
    return defaultVal;
  }

  function parseNum(val, defaultVal) {
    if (val === undefined || val === null) return defaultVal;
    var n = parseFloat(val);
    return isNaN(n) ? defaultVal : n;
  }

  function ensureGsapAndScrollTrigger(callback) {
    if (window.gsap && window.ScrollTrigger) {
      window.gsap.registerPlugin(window.ScrollTrigger);
      callback();
      return;
    }

    // Dynamic loader for GSAP CDN if not already included on the page
    var gsapLoaded = !!window.gsap;
    var stLoaded = !!window.ScrollTrigger;

    function checkReady() {
      if (window.gsap && window.ScrollTrigger) {
        window.gsap.registerPlugin(window.ScrollTrigger);
        callback();
      }
    }

    if (!gsapLoaded) {
      var script1 = document.createElement('script');
      script1.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js';
      script1.onload = function () {
        if (!stLoaded) {
          var script2 = document.createElement('script');
          script2.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js';
          script2.onload = checkReady;
          document.head.appendChild(script2);
        } else {
          checkReady();
        }
      };
      document.head.appendChild(script1);
    } else if (!stLoaded) {
      var script2 = document.createElement('script');
      script2.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js';
      script2.onload = checkReady;
      document.head.appendChild(script2);
    }
  }

  function initAnimatedElement(el) {
    if (!el || el.dataset.animatedContentInitialized === 'true') return;
    el.dataset.animatedContentInitialized = 'true';

    var ds = el.dataset;

    var distance = parseNum(ds.distance, 100);
    var direction = ds.direction === 'horizontal' ? 'horizontal' : 'vertical';
    var reverse = parseBool(ds.reverse, false);
    var duration = parseNum(ds.duration, 0.8);
    var ease = ds.ease || 'power3.out';
    var initialOpacity = parseNum(ds.initialOpacity, 0);
    var animateOpacity = parseBool(ds.animateOpacity, true);
    var scale = parseNum(ds.scale, 1);
    var blur = parseNum(ds.blur, 0);
    var rotate = parseNum(ds.rotate, 0);
    var tilt = parseNum(ds.tilt, 0);
    var wipe = ds.wipe || 'none';
    var threshold = parseNum(ds.threshold, 0.1);
    var delay = parseNum(ds.delay, 0);
    var stagger = parseNum(ds.stagger, 0);
    var staggerFrom = ds.staggerFrom || 'start';
    var trigger = ds.trigger || 'scroll';
    var once = parseBool(ds.once, true);
    var scrub = ds.scrub ? (ds.scrub === 'true' ? true : parseNum(ds.scrub, true)) : false;
    var disappearAfter = parseNum(ds.disappearAfter, 0);
    var disappearDuration = parseNum(ds.disappearDuration, 0.5);
    var disappearEase = ds.disappearEase || 'power3.in';

    var container = ds.container ? document.querySelector(ds.container) : (document.getElementById('snap-main-container') || null);
    var reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)').matches : false;

    var targets = stagger > 0 && el.children.length ? Array.from(el.children) : [el];
    var horizontal = direction === 'horizontal';
    var axis = horizontal ? 'x' : 'y';
    var sign = reverse ? -1 : 1;
    var mask = WIPES[wipe] || null;

    gsap.set(el, { visibility: 'visible' });

    if (reduce) {
      gsap.set(targets, { opacity: 1, x: 0, y: 0, scale: 1 });
      return;
    }

    var from = {
      scale: scale,
      opacity: animateOpacity ? initialOpacity : 1
    };
    from[axis] = distance * sign;

    var to = {
      scale: 1,
      opacity: 1,
      duration: duration,
      ease: ease
    };
    to[axis] = 0;

    if (blur > 0) {
      from.filter = 'blur(' + blur + 'px)';
      to.filter = 'blur(0px)';
    }
    if (rotate) {
      from.rotation = rotate * sign;
      to.rotation = 0;
    }
    if (tilt) {
      var tiltAxis = horizontal ? 'rotationY' : 'rotationX';
      from[tiltAxis] = horizontal ? -tilt * sign : tilt * sign;
      to[tiltAxis] = 0;
      from.transformPerspective = 900;
      to.transformPerspective = 900;
    }
    if (mask) {
      gsap.set(targets, { maskImage: mask, webkitMaskImage: mask });
      from['--ac-wipe'] = 0;
      to['--ac-wipe'] = 1;
    }
    if (stagger > 0) {
      to.stagger = { each: stagger, from: staggerFrom };
    }

    var settle = function () {
      if (scrub) return;
      gsap.set(targets, { clearProps: mask ? 'filter,transform,maskImage,webkitMaskImage' : 'filter,transform' });
    };

    var disappear = function () {
      if (disappearAfter <= 0) return;
      var out = {
        scale: 0.8,
        opacity: animateOpacity ? initialOpacity : 0,
        delay: disappearAfter,
        duration: disappearDuration,
        ease: disappearEase
      };
      out[axis] = -distance * sign;
      if (blur > 0) out.filter = 'blur(' + blur + 'px)';
      if (stagger > 0) out.stagger = { each: stagger, from: staggerFrom };
      gsap.to(targets, out);
    };

    var tl = gsap.timeline({
      paused: true,
      onComplete: function () {
        settle();
        if (once && !scrub) disappear();
      }
    });

    tl.fromTo(targets, from, to, scrub ? 0 : Math.max(delay, 0));

    if (trigger === 'mount') {
      tl.play();
      return;
    }

    var start = 'top ' + ((1 - threshold) * 100) + '%';

    if (scrub) {
      ScrollTrigger.create({
        trigger: el,
        scroller: container,
        start: start,
        end: 'top ' + Math.max((1 - threshold) * 100 - 45, 5) + '%',
        scrub: scrub === true ? true : Math.max(Number(scrub) || 0, 0.01),
        animation: tl
      });
      return;
    }

    ScrollTrigger.create({
      trigger: el,
      scroller: container,
      start: start,
      once: once,
      onEnter: function () {
        tl.play();
      },
      onLeaveBack: once
        ? undefined
        : function () {
            if (mask) gsap.set(targets, { maskImage: mask, webkitMaskImage: mask });
            tl.reverse();
          }
    });
  }

  function initAll() {
    ensureGsapAndScrollTrigger(function () {
      var elements = document.querySelectorAll('[data-animated-content="true"], .animated-content');
      for (var i = 0; i < elements.length; i++) {
        initAnimatedElement(elements[i]);
      }
    });
  }

  // Auto-init on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  // Export to window
  window.AnimatedContent = {
    init: initAll,
    animate: initAnimatedElement
  };

})(window, document);

