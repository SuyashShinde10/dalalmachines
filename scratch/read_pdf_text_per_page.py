# scratch/read_pdf_text_per_page.py
import pypdf # or let's use a simple pdf parser or python-pdf
try:
    from pypdf import PdfReader
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "pypdf"])
    from pypdf import PdfReader

reader = PdfReader("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf")
print("Total pages in PDF:", len(reader.pages))

for idx, page in enumerate(reader.pages):
    text = page.extract_text()
    first_line = text.split('\n')[0] if text else "EMPTY"
    last_line = text.split('\n')[-1] if text else "EMPTY"
    has_m4 = "Module 04" in text or "Fast-Quote" in text or "ERP-MOD-04" in text
    has_m3 = "ERP-MOD-03" in text
    print(f"PDF Page {idx+1}: {len(text)} chars | First: {first_line[:40]} | Last: {last_line[-30:]} | M3={has_m3}, M4={has_m4}")

