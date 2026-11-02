# scratch/calibrate_p18.py
with open('scratch/build_enterprise_specification_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Calibrate ERP-MOD-03
old_m03 = '''        "id": "ERP-MOD-03",
        "title": "Manual Exchange Rate & Landed Cost Calculator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Commercial Manager, Managing Director",
        "focus": "Daily Manual Euro/INR Entry & Duty Surcharge Matrix (Optional Live API)",
        "does": "Enables commercial staff to input daily official Euro/INR rates manually (or via optional live Forex API subscription if provided by Client) to calculate landed selling prices including sea freight, basic customs duty, and target margins.",
        "benefit": "Helps protect profit margins against currency shifts between the Euro and Rupee during international shipping, supporting consistent and sustainable commercial pricing.",
        "deliverables": ["Daily Manual Euro Exchange Rate Entry Interface", "Customs Duty & Port Handling Surcharge Matrix", "Target Margin Calculation Guidelines"],
        "feature": "Manual daily exchange rate entry with automated duty surcharge calculation (live feed optional add-on)."'''

new_m03 = '''        "id": "ERP-MOD-03",
        "title": "Manual Exchange Rate & Landed Cost Calculator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Commercial Manager, Managing Director",
        "focus": "Daily Manual Euro/INR Entry & Duty Surcharges (Optional Live API)",
        "does": "Allows staff to input daily official Euro/INR rates manually (or connect optional live Forex API) to calculate landed selling prices including sea freight, basic customs duty, and target margins.",
        "benefit": "Helps protect profit margins against currency shifts between Euro and Rupee during international shipping, supporting consistent commercial pricing.",
        "deliverables": ["Daily Manual Euro Exchange Rate Entry Interface", "Customs Duty & Port Handling Surcharge Matrix", "Target Margin Calculation Guidelines"],
        "feature": "Manual daily exchange rate entry with automated duty surcharge calculation (live feed optional add-on)."'''

text = text.replace(old_m03, new_m03)

# Calibrate ERP-MOD-04
old_m04 = '''        "id": "ERP-MOD-04",
        "title": "OMPI Fast-Quote & Commercial Proposal Generator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Sales Representatives, Commercial Staff",
        "focus": "Shared Quoting Architecture with Isolated OMPI Letterhead & Banking",
        "does": "Extends the Phase 1 Centralized Quoting Engine to OMPI India LLP products. Generates formal PDF proposals for Italian clutch models and sizing data, strictly maintaining OMPI India LLP's distinct letterhead, sequential quote numbering, and independent bank details.",
        "benefit": "Enables sales staff to generate and send official quotation letters while discussing requirements with prospective buyers, helping accelerate response times and customer decisions.",
        "deliverables": ["Dedicated OMPI India LLP Branded Quotation Format", "Separate Quote Numbering Sequence & Bank Details", "WhatsApp & Email Proposal Dispatch Link"],
        "feature": "Shared quoting engine generating OMPI proposals with distinct entity letterhead and banking."'''

new_m04 = '''        "id": "ERP-MOD-04",
        "title": "OMPI Fast-Quote & Commercial Proposal Generator",
        "engine": "Engine 1: Sales & Customer Management",
        "role": "Sales Representatives, Commercial Staff",
        "focus": "Shared Quoting Engine with Isolated OMPI Letterhead & Banking",
        "does": "Extends Phase 1 Core Quoting Engine to OMPI products. Generates formal PDF proposals for Italian clutch models, strictly maintaining OMPI's separate letterhead, quote numbering, and bank details.",
        "benefit": "Enables sales staff to generate official quotation letters quickly, helping accelerate response times while keeping entity records strictly segregated.",
        "deliverables": ["Dedicated OMPI India LLP Branded Quotation Format", "Separate Quote Numbering Sequence & Bank Details", "WhatsApp & Email Proposal Dispatch Link"],
        "feature": "Shared quoting engine generating OMPI proposals with distinct entity letterhead and banking."'''

text = text.replace(old_m04, new_m04)

with open('scratch/build_enterprise_specification_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated build_enterprise_specification_v2.py for Page 18 calibration!')

