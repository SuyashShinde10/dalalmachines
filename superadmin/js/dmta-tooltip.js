/**
 * Dalal Machine Tools Agency Pvt. Ltd.
 * Enterprise Tooltip Engine - Scoped to Administrative & Developer Panels
 * (Admin, Superadmin, and Developer Console)
 */

(function(window, document) {
  'use strict';

  const DmtaTooltip = {
    tooltipEl: null,
    arrowEl: null,
    contentEl: null,
    activeTarget: null,
    hideTimeout: null,

    init: function() {
      if (this.tooltipEl || typeof document === 'undefined') return;

      const initOnDomReady = () => {
        if (!document.body) {
          setTimeout(initOnDomReady, 20);
          return;
        }

        const tip = document.createElement('div');
        tip.className = 'dmta-tooltip';
        tip.id = 'dmta-global-tooltip';
        tip.setAttribute('role', 'tooltip');
        tip.setAttribute('aria-hidden', 'true');

        const arrow = document.createElement('div');
        arrow.className = 'dmta-tooltip-arrow';
        tip.appendChild(arrow);

        const content = document.createElement('span');
        content.className = 'dmta-tooltip-text';
        tip.appendChild(content);

        document.body.appendChild(tip);
        this.tooltipEl = tip;
        this.arrowEl = arrow;
        this.contentEl = content;

        // Global Event Delegation for all dynamic & static elements
        document.addEventListener('pointerover', (e) => this.handlePointerOver(e), { passive: true });
        document.addEventListener('pointerout', (e) => this.handlePointerOut(e), { passive: true });
        document.addEventListener('focusin', (e) => this.handleFocusIn(e), { passive: true });
        document.addEventListener('focusout', (e) => this.handlePointerOut(e), { passive: true });
        window.addEventListener('scroll', () => this.hide(), { passive: true });
        window.addEventListener('resize', () => this.hide(), { passive: true });
      };

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initOnDomReady);
      } else {
        initOnDomReady();
      }
    },

    getTarget: function(el) {
      if (!el || el === document.body || el === document.documentElement) return null;
      return el.closest('[data-tooltip], [title]');
    },

    handlePointerOver: function(e) {
      const target = this.getTarget(e.target);
      if (!target) return;

      // Migrate native title to data-tooltip to suppress default browser tooltip
      if (target.hasAttribute('title')) {
        const titleVal = target.getAttribute('title').trim();
        if (titleVal) {
          target.setAttribute('data-tooltip', titleVal);
        }
        target.removeAttribute('title');
      }

      const text = target.getAttribute('data-tooltip');
      if (!text || !text.trim()) return;

      clearTimeout(this.hideTimeout);
      this.show(target, text.trim());
    },

    handlePointerOut: function(e) {
      if (!this.activeTarget) return;
      if (e.relatedTarget && this.activeTarget.contains(e.relatedTarget)) return;
      this.hide();
    },

    handleFocusIn: function(e) {
      const target = this.getTarget(e.target);
      if (!target) return;
      let text = target.getAttribute('data-tooltip');
      if (target.hasAttribute('title')) {
        text = target.getAttribute('title').trim();
        target.setAttribute('data-tooltip', text);
        target.removeAttribute('title');
      }
      if (text && text.trim()) {
        this.show(target, text.trim());
      }
    },

    show: function(target, text) {
      if (!this.tooltipEl) return;
      this.activeTarget = target;
      this.contentEl.textContent = text;
      this.tooltipEl.setAttribute('aria-hidden', 'false');

      const placement = target.getAttribute('data-tooltip-pos') || 'top';
      this.position(target, placement);
      this.tooltipEl.classList.add('is-visible');
    },

    position: function(target, requestedPlacement) {
      const tip = this.tooltipEl;
      const targetRect = target.getBoundingClientRect();

      tip.style.display = 'flex';
      tip.style.visibility = 'hidden';
      const tipRect = tip.getBoundingClientRect();

      let placement = requestedPlacement;
      const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
      const scrollY = window.pageYOffset || document.documentElement.scrollTop;

      const gap = 8;
      // Auto flip if overflowing top or bottom screen boundaries
      if (placement === 'top' && targetRect.top - tipRect.height - gap < 0) {
        placement = 'bottom';
      } else if (placement === 'bottom' && targetRect.bottom + tipRect.height + gap > window.innerHeight) {
        placement = 'top';
      }

      let top = 0;
      let left = 0;

      if (placement === 'top') {
        top = targetRect.top + scrollY - tipRect.height - gap;
        left = targetRect.left + scrollX + (targetRect.width / 2) - (tipRect.width / 2);
      } else if (placement === 'bottom') {
        top = targetRect.bottom + scrollY + gap;
        left = targetRect.left + scrollX + (targetRect.width / 2) - (tipRect.width / 2);
      } else if (placement === 'left') {
        top = targetRect.top + scrollY + (targetRect.height / 2) - (tipRect.height / 2);
        left = targetRect.left + scrollX - tipRect.width - gap;
      } else if (placement === 'right') {
        top = targetRect.top + scrollY + (targetRect.height / 2) - (tipRect.height / 2);
        left = targetRect.right + scrollX + gap;
      }

      // Boundary Clamping (prevent screen edge cut-off)
      const minLeft = scrollX + 8;
      const maxLeft = scrollX + window.innerWidth - tipRect.width - 8;
      left = Math.max(minLeft, Math.min(left, maxLeft));

      tip.setAttribute('data-placement', placement);
      tip.style.top = `${Math.round(top)}px`;
      tip.style.left = `${Math.round(left)}px`;
      tip.style.visibility = '';
    },

    hide: function() {
      if (!this.tooltipEl) return;
      this.tooltipEl.classList.remove('is-visible');
      this.tooltipEl.setAttribute('aria-hidden', 'true');
      this.activeTarget = null;
    }
  };

  window.DmtaTooltip = DmtaTooltip;

  // Auto-initialize when loaded
  DmtaTooltip.init();

})(window, document);
