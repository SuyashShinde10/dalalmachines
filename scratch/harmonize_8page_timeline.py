# scratch/harmonize_8page_timeline.py
with open('scratch/build_clean_8page_specification.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Harmonize Validity and Timeline on Page 1
text = text.replace('Valid for 30 days', 'Valid Through 14 November 2026')

old_table = """            <tr>
              <td><strong>Phase 1: Dalal Platform</strong></td>
              <td>All 24 units of System 1, the shared quotation engine, WhatsApp enquiry buttons, basic search-engine setup and Google Analytics, go-live</td>
              <td class="col-center">4 to 6 weeks</td>
              <td class="col-center">Months 1 to 2</td>
            </tr>
            <tr>
              <td><strong>Phase 2: OMPI Core ERP</strong></td>
              <td>15 modules: customers, catalogue, pricing, quotes, deal board, stock, purchase orders, landed costing, staff access, backups</td>
              <td class="col-center">8 to 10 weeks</td>
              <td class="col-center">Months 2 to 4</td>
            </tr>
            <tr>
              <td><strong>Phase 3: OMPI Operations and Control</strong></td>
              <td>18 modules: workshop, port tracking, GST billing, payments, accounts reports, service desk, Managing Director desk</td>
              <td class="col-center">8 to 10 weeks</td>
              <td class="col-center">Months 4 to 6</td>
            </tr>"""

new_table = """            <tr>
              <td><strong>Phase 1: Dalal Platform</strong></td>
              <td>All 24 units of System 1, the shared quotation engine, WhatsApp enquiry buttons, basic search-engine setup and Google Analytics, go-live</td>
              <td class="col-center">Weeks 1 to 8</td>
              <td class="col-center">Months 1 to 2</td>
            </tr>
            <tr>
              <td><strong>Phase 2: OMPI Core ERP</strong></td>
              <td>15 modules: customers, catalogue, pricing, quotes, deal board, stock, purchase orders, landed costing, staff access, backups</td>
              <td class="col-center">Weeks 9 to 20</td>
              <td class="col-center">Months 3 to 5</td>
            </tr>
            <tr>
              <td><strong>Phase 3: OMPI Operations and Control</strong></td>
              <td>18 modules: workshop, port tracking, GST billing, payments, accounts reports, service desk, Managing Director desk</td>
              <td class="col-center">Weeks 21 to 32</td>
              <td class="col-center">Months 6 to 8</td>
            </tr>"""

text = text.replace(old_table, new_table)
text = text.replace('Total: about 5 to 6 months. Phases are built one after another.', 'Total: 8 Months (32 Calendar Weeks). Phases are built one after another.')

with open('scratch/build_clean_8page_specification.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Harmonized timeline and validity successfully!')
