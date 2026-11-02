# scratch/inspect_page_sample.py
with open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html", "r", encoding="utf-8") as f:
    c = f.read()

pages = c.split('<div class="page"')
print("=== Route Card sample from Page 2 ===")
print(pages[2][1100:2600])

print("\n=== Module Card sample from Page 15 ===")
print(pages[15][1100:2600])
