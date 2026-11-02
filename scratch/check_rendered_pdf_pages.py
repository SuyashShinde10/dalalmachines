# scratch/check_rendered_pdf_pages.py
import re

with open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html", "r", encoding="utf-8") as f:
    html = f.read()

pages_count = html.count('class="page"')
print("Total HTML Pages:", pages_count)

# Let's inspect Page 1, Page 2, Page 14, Page 32 texts to verify pre-commencement wording
print("\n--- Page 1 Pre-commencement snippet ---")
idx1 = html.find("IMPORTANT PRE-PROJECT STATEMENT")
print(html[idx1:idx1+400])

print("\n--- Page 2 Route status snippet ---")
idx2 = html.find("TO BE BUILT: SYSTEM 1")
print(html[idx2-50:idx2+150])

print("\n--- Page 32 Sign-off snippet ---")
idx32 = html.find("Accepted &amp; Approved to Commence Work")
print(html[idx32-50:idx32+200])

