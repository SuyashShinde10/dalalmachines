import fitz
import sys

def run_audit():
    pdf_path = "DALAL_AND_OMPI_COMMERCIAL_QUOTATION_BREAKDOWN.pdf"
    doc = fitz.open(pdf_path)
    
    print(f"Total Pages in PDF: {len(doc)}")
    assert len(doc) == 2, f"Expected 2 pages, got {len(doc)}"
    
    p1 = doc[0].get_text()
    p2 = doc[1].get_text()
    full_text = p1 + "\n--- PAGE BREAK ---\n" + p2
    
    errors = []
    
    print("\n--- 1. GROUP & MODULE NUMBERING ALIGNMENT WITH SCOPE DOC v2.5 ---")
    expected_groups = [
        ("GROUP 1", "SALES AND CUSTOMERS", "MOD 01"),
        ("GROUP 2", "INVENTORY AND GODOWN", "MOD 07"),
        ("GROUP 3", "PROCUREMENT AND COSTING", "MOD 13"),
        ("GROUP 4", "WORKSHOP AND OVERHAULS", "MOD 17"),
        ("GROUP 5", "ACCOUNTS AND GST", "MOD 21"),
        ("GROUP 6", "SALES OPERATIONS AND SERVICE", "MOD 26"),
        ("GROUP 7", "CONTROL AND SECURITY", "MOD 31"),
    ]
    
    for grp_tag, grp_name, mod_prefix in expected_groups:
        has_grp = grp_tag in p1.upper() and grp_name in p1.upper()
        has_mods = mod_prefix in p1
        if not has_grp:
            errors.append(f"Missing or mismatch in group: {grp_tag}: {grp_name}")
            print(f"  [FAIL] {grp_tag}: {grp_name}")
        else:
            print(f"  [PASS] {grp_tag}: {grp_name}")
            
        if not has_mods:
            errors.append(f"Missing or mismatch in module range: {mod_prefix}")
            print(f"  [FAIL] Range starting with {mod_prefix}")
        else:
            print(f"  [PASS] Range starting with {mod_prefix}")

    print("\n--- 2. TIMELINE & VALIDITY ALIGNMENT ---")
    if "Weeks 1 to 8 (Months 1 to 2)" in p1:
        print("  [PASS] System 1 delivery: Weeks 1 to 8 (Months 1 to 2)")
    else:
        errors.append("System 1 delivery timeline missing or incorrect")
        print("  [FAIL] System 1 delivery timeline")
        
    if "Weeks 9 to 32 | 7 Monthly Sprints" in p1:
        print("  [PASS] System 2 delivery: Weeks 9 to 32 | 7 Monthly Sprints")
    else:
        errors.append("System 2 delivery timeline missing or incorrect")
        print("  [FAIL] System 2 delivery timeline")
        
    if "14 November 2026" in p1 and "17 November" not in full_text and "17 Nov" not in full_text:
        print("  [PASS] Validity synchronized to 14 November 2026 (17 Nov eliminated)")
    else:
        errors.append("Validity mismatch (14 November 2026 expected)")
        print("  [FAIL] Validity date")

    print("\n--- 3. SECTION 4 INCLUDED BADGE & FONT CORRUPTION CHECK ---")
    free_count = full_text.count("INCLUDED (FREE)")
    print(f"  'INCLUDED (FREE)' occurrences found: {free_count} (Expected: 6)")
    if free_count == 6:
        print("  [PASS] All 6 Section 4 items use 'INCLUDED (FREE)'")
    else:
        errors.append(f"Expected 6 'INCLUDED (FREE)' badges, found {free_count}")
        print("  [FAIL] 'INCLUDED (FREE)' count")
        
    if "२०" in full_text or "१०" in full_text or "(20)" in full_text or "(10)" in full_text:
        errors.append("Font corruption detected (Hindi numerals or (20)/(10) found)")
        print("  [FAIL] Font corruption found in text")
    else:
        print("  [PASS] Zero font/Devanagari corruption detected")

    print("\n--- 4. TYPOGRAPHICAL CHECKS ---")
    typos_to_check = [
        ("15-digit GSTIN", True, "15-digit GSTIN is present"),
        ("15digit", False, "15digit typo is eliminated"),
        ("clutch-brakes", True, "clutch-brakes hyphenated properly"),
        ("Clutchbrakes-", False, "Clutchbrakes- trailing hyphen eliminated"),
        ("327 Monthly Sprints", False, "327 Monthly Sprints glue error eliminated"),
        ("(Est.)", True, "(Est.) properly formatted"),
        ("(Est).", False, "(Est). trailing period outside bracket eliminated"),
        ("AI-crawler", True, "AI-crawler with capital I present"),
        ("Al-crawler", False, "Al-crawler with lowercase l eliminated"),
        ("settlement", True, "settlement properly spelled"),
        ("settlemerit", False, "settlemerit typo eliminated"),
    ]
    
    for text_snippet, should_exist, desc in typos_to_check:
        exists = text_snippet in full_text or text_snippet.lower() in full_text.lower()
        if exists == should_exist:
            print(f"  [PASS] {desc}")
        else:
            errors.append(f"Typo check failed for '{text_snippet}' (should_exist={should_exist})")
            print(f"  [FAIL] {desc}")

    print("\n--- 5. RETENTION & SPRINT MAPPING IN SECTION 5 ---")
    sprint_check = [
        ("OMPI Sprint 1", "MOD 01"),
        ("OMPI Sprint 2", "MOD 07"),
        ("OMPI Sprint 3", "MOD 13"),
        ("OMPI Sprint 4", "MOD 17"),
        ("OMPI Sprint 5", "MOD 21"),
        ("OMPI Sprint 6", "MOD 26"),
        ("OMPI Sprint 7", "MOD 31"),
    ]
    for sp_name, mod_pfx in sprint_check:
        if (sp_name in p2) and (mod_pfx in p2):
            print(f"  [PASS] {sp_name} mapped with {mod_pfx}")
        else:
            errors.append(f"Section 5 Sprint mismatch: {sp_name}")
            print(f"  [FAIL] {sp_name}")

    print("\n================ AUDIT SUMMARY ================")
    if not errors:
        print(">>> ALL CHECKS PASSED PERFECTLY! 100% PRODUCTION READY! <<<")
        return True
    else:
        print(f">>> {len(errors)} ERRORS ENCOUNTERED: <<<")
        for err in errors:
            print(f"  - {err}")
        return False

if __name__ == "__main__":
    success = run_audit()
    if not success:
        sys.exit(1)
