import fitz

doc = fitz.open("DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.pdf")

# Render Page 7 and Page 8 to PNG
doc[6].get_pixmap(dpi=150).save("scratch/spec_page_07.png")
doc[7].get_pixmap(dpi=150).save("scratch/spec_page_08.png")
print("Saved spec_page_07.png and spec_page_08.png")

# Now verify the 5 items in the text
full_text = ""
for i, page in enumerate(doc):
    t = page.get_text()
    full_text += f"\n--- PAGE {i+1} ---\n" + t

# 1. Valid Through in Scope doc
print("\n1. Valid Through in Scope doc:")
print("   'Valid Through' in full text?:", "Valid Through" in full_text)

# 2. Power-trial video links in 'What we need from you'
print("\n2. 'What we need from you' check:")
print("   'power-trial video links' in full text?:", "power-trial video links" in full_text)
print("   'Machine details and photos for Pune stock' present?:", "Machine details and photos for Pune stock" in full_text)

# 3. Running videos in Unit 1
print("\n3. Unit 1 Homepage check:")
print("   'running videos' in full text?:", "running videos" in full_text)

# 4. Video links in Unit 23
print("\n4. Unit 23 Staff Desk check:")
print("   'add video links' in full text?:", "add video links" in full_text)

# 5. Approval section check
print("\n5. Approval section check:")
print("   '11. Approval' in full text?:", "11. Approval" in full_text)
print("   'Signature' in full text?:", "Signature" in full_text)
print("   'Authorised Signatory' in full text?:", "Authorised Signatory" in full_text)

print("\n6. Glossary and Governance check:")
print("   '10. Glossary of Industrial & Software Terms' in full text?:", "Glossary of Industrial & Software Terms" in full_text)
print("   'Scope Governance & Contractual Notice' in full text?:", "Scope Governance & Contractual Notice" in full_text)
