# scratch/inspect_p1_p32.py
with open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html", "r", encoding="utf-8") as f:
    c = f.read()

pages = c.split('<div class="page"')
print("=== PAGE 1 ===")
print(pages[1][:1200])

print("\n=== PAGE 32 ===")
print(pages[32][:1200])

