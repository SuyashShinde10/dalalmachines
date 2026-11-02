# scratch/diagnose_pages.py
with open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html", "r", encoding="utf-8") as f:
    html = f.read()

pages = html.split('<div class="page"')
print("Total pages in HTML:", len(pages) - 1)

for i in range(1, len(pages)):
    p = pages[i]
    badges = p.count('class="badge-id"')
    print(f"Page {i}: {len(p)} chars, badges: {badges}")

