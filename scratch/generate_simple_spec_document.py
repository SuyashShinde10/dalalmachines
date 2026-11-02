# scratch/generate_simple_spec_document.py
import os, subprocess, shutil

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dalal Machine Tools & OMPI India - Executive Business Guide (57 Systems & Modules)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 8mm 10mm 8mm 10mm;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #0f172a;
      background: #ffffff;
      font-size: 9.2pt;
      line-height: 1.4;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .page {
      height: 281mm;
      max-height: 281mm;
      overflow: hidden;
      box-sizing: border-box;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      break-after: page;
      padding: 1px 0;
    }
    .page:last-child {
      page-break-after: avoid;
      break-after: avoid;
    }
    .page-content {
      flex: 1;
    }

    /* Corporate Header */
    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #0f172a;
      border-top: 3.5px solid #d97706;
      padding-top: 4px;
      padding-bottom: 5px;
      margin-bottom: 7px;
    }
    .brand-title {
      font-size: 11pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.2px;
    }
    .brand-subtitle {
      font-size: 7.6pt;
      font-weight: 600;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .doc-meta {
      text-align: right;
      font-size: 7.2pt;
      color: #475569;
      line-height: 1.3;
    }

    /* Confidentiality Alert Bar */
    .confidential-bar {
      background: #fef2f2;
      border: 1.5px solid #dc2626;
      border-radius: 4px;
      padding: 4px 8px;
      margin-bottom: 7px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.4pt;
      font-weight: 700;
      color: #991b1b;
    }
    .confidential-tag {
      background: #b91c1c;
      color: #ffffff;
      padding: 1px 6px;
      border-radius: 3px;
      text-transform: uppercase;
      font-size: 6.8pt;
      letter-spacing: 0.5px;
    }

    /* Section Subheaders */
    .section-header {
      background: #0f172a;
      color: #ffffff;
      padding: 4.5px 8px;
      border-radius: 4px;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .section-title {
      font-size: 8.4pt;
      font-weight: 800;
      letter-spacing: 0.3px;
      text-transform: uppercase;
    }
    .section-tag {
      font-size: 7.2pt;
      font-weight: 600;
      background: #f59e0b;
      color: #0f172a;
      padding: 1px 6px;
      border-radius: 3px;
    }

    /* Standard Card Box (2 per page) */
    .card-box {
      border: 1.5px solid #cbd5e1;
      border-radius: 6px;
      background: #ffffff;
      margin-bottom: 8px;
      padding: 8px 10px;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 5px;
      margin-bottom: 6px;
    }
    .badge-id {
      background: #0f172a;
      color: #ffffff;
      padding: 2px 7px;
      border-radius: 3px;
      font-size: 7.6pt;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-right: 6px;
    }
    .card-title {
      font-size: 9.8pt;
      font-weight: 800;
      color: #0f172a;
    }
    .card-path {
      font-family: 'JetBrains Mono', monospace;
      font-size: 7.4pt;
      color: #b45309;
      font-weight: 700;
      background: #fffbeb;
      padding: 2px 6px;
      border: 1px solid #fef3c7;
      border-radius: 3px;
    }
    .card-status {
      font-size: 7.2pt;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      margin-left: 5px;
    }
    .status-live {
      background: #dcfce7;
      color: #15803d;
      border: 1px solid #bbf7d0;
    }
    .status-phase2 {
      background: #fef3c7;
      color: #b45309;
      border: 1px solid #fde68a;
    }

    /* Simple 2-Column Content Grid */
    .simple-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 6px;
    }
    .grid-label {
      font-size: 7.4pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      color: #475569;
      margin-bottom: 2px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 2px;
    }
    .grid-text {
      font-size: 8.6pt;
      line-height: 1.36;
      color: #334155;
    }

    /* Highlight Feature Box */
    .feature-strip {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 5px 8px;
      font-size: 8.2pt;
      line-height: 1.38;
      color: #1e293b;
    }
    .feature-strip strong {
      color: #0f172a;
    }

    /* Corporate Footer */
    .footer-bar {
      border-top: 1px solid #cbd5e1;
      padding-top: 4px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 6.9pt;
      color: #64748b;
      margin-top: auto;
    }
    .confidential-watermark {
      font-weight: 800;
      color: #dc2626;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
  </style>
</head>
<body>
"""

print("Writing generator script...")

