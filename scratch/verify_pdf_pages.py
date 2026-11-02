# scratch/verify_pdf_pages.py
import re

with open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html", "r", encoding="utf-8") as f:
    html = f.read()

pages_count = html.count('class="page"')
print("Total HTML A4 Page Containers:", pages_count)

# Check if any technical jargon remained
jargon_list = ["REST API", "JSON Schema", "CSP Level", "JWT", "cryptographic HMAC", "SHA-256", "regex", "DOM Tree", "Isotope layout", "Socket.IO"]
found_jargon = []
for j in jargon_list:
    if j.lower() in html.lower():
        found_jargon.append(j)

print("Technical Jargon Found in HTML:", found_jargon if found_jargon else "NONE (0% JARGON!)")

# Check confidentiality notices
confidential_mentions = html.count("CONFIDENTIAL")
do_not_share_mentions = html.count("NOT FOR SHARING") + html.count("DO NOT SHARE")
print(f"Confidentiality Notices Count: {confidential_mentions} times | Anti-Sharing Warnings: {do_not_share_mentions} times")

