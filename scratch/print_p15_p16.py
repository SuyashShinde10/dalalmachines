# scratch/print_p15_p16.py
from pypdf import PdfReader
reader = PdfReader('DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf')

with open('scratch/p15.txt', 'w', encoding='utf-8') as f:
    f.write(reader.pages[14].extract_text())

with open('scratch/p16.txt', 'w', encoding='utf-8') as f:
    f.write(reader.pages[15].extract_text())

print("P15 length:", len(reader.pages[14].extract_text()))
print("P16 length:", len(reader.pages[15].extract_text()))

