/**
 * Dalal Machine Tools Agency Pvt. Ltd. (DMTA)
 * Enterprise B2B Analytics & Conversion Telemetry Layer
 * Connects UI interactions to Google Tag Manager (GTM) dataLayer & GA4
 */

(function () {
    'use strict';

    // Ensure dataLayer exists
    window.dataLayer = window.dataLayer || [];

    function pushEvent(eventName, params) {
        try {
            const payload = Object.assign({
                event: eventName,
                page_path: window.location.pathname,
                page_title: document.title,
                timestamp: new Date().toISOString()
            }, params || {});

            window.dataLayer.push(payload);
            // Dev logging in development mode
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                console.log('[DMTA Analytics Event]:', eventName, payload);
            }
        } catch (e) {
            console.warn('[DMTA Analytics Warning]:', e);
        }
    }

    // Expose global telemetry API
    window.DalalTelemetry = {
        trackWhatsAppClick: function (details) {
            pushEvent('whatsapp_rfq_click', {
                category: 'B2B Lead Generation',
                action: 'Click WhatsApp',
                machine_id: details?.machineId || 'GENERAL',
                machine_name: details?.machineName || 'General Inquiry',
                destination: details?.destination || '+91 98212 32131'
            });
        },
        trackPdfDownload: function (machineId, machineName) {
            pushEvent('pdf_spec_download', {
                category: 'Engagement',
                action: 'Download Spec Sheet',
                machine_id: machineId || 'UNKNOWN',
                machine_name: machineName || 'Datasheet'
            });
        },
        trackYardVisitRequest: function (details) {
            pushEvent('pune_yard_visit_click', {
                category: 'High Intent Lead',
                action: 'Schedule Yard Demonstration',
                machine_id: details?.machineId || 'ANY',
                machine_name: details?.machineName || 'Pune Stockyard Trial',
                preferred_date: details?.preferredDate || 'Earliest'
            });
        },
        trackRfqSubmission: function (details) {
            pushEvent('rfq_form_submit', {
                category: 'Conversion',
                action: 'Submit RFQ Form',
                machine_id: details?.machineId || 'GENERAL',
                machine_name: details?.machineName || 'General Machinery Inquiry',
                company: details?.company || 'Not Specified',
                lead_type: details?.leadType || 'Direct Inquiry'
            });
        },
        trackSearch: function (query, resultCount) {
            if (!query || query.length < 2) return;
            pushEvent('search_query', {
                search_term: query,
                results_count: resultCount || 0
            });
        }
    };

    // Auto-bind click handlers for WhatsApp links and PDF buttons across all pages
    document.addEventListener('DOMContentLoaded', function () {
        // 1. WhatsApp Links
        document.addEventListener('click', function (e) {
            const waTarget = e.target.closest('a[href*="wa.me"], a[href*="whatsapp.com"], .wa-btn, [data-track="whatsapp"]');
            if (waTarget) {
                const machineTitle = document.getElementById('pdp-title')?.textContent?.trim() || 
                                     waTarget.getAttribute('data-machine-name') || 'Machinery Inventory';
                const machineId = document.getElementById('pdp-id-tag')?.textContent?.trim() || 
                                  waTarget.getAttribute('data-machine-id') || 'GENERAL';
                window.DalalTelemetry.trackWhatsAppClick({
                    machineId: machineId,
                    machineName: machineTitle
                });
            }

            // 2. PDF Spec Sheet Download Clicks
            const pdfTarget = e.target.closest('a[href*="/spec-sheet"], button[onclick*="printMachineSpecSheet"], .pdf-download-btn, [data-track="pdf"]');
            if (pdfTarget) {
                const machineTitle = document.getElementById('pdp-title')?.textContent?.trim() || 'Machinery Datasheet';
                const machineId = document.getElementById('pdp-id-tag')?.textContent?.trim() || 
                                  new URLSearchParams(window.location.search).get('id') || 'GENERAL';
                window.DalalTelemetry.trackPdfDownload(machineId, machineTitle);
            }

            // 3. Yard Trial / Inspection Modal Triggers
            const yardTarget = e.target.closest('[data-target="#inspectionModal"], [data-track="yard-trial"]');
            if (yardTarget) {
                const machineTitle = document.getElementById('pdp-title')?.textContent?.trim() || 'Pune Yard Machinery';
                const machineId = document.getElementById('pdp-id-tag')?.textContent?.trim() || 'INVENTORY';
                window.DalalTelemetry.trackYardVisitRequest({
                    machineId: machineId,
                    machineName: machineTitle
                });
            }
        });
    });
})();
