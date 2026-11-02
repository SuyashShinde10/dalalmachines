import subprocess, os, shutil

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
html_path = os.path.abspath('CLIENT_DISCOVERY_MEETING_PLAYBOOK_AND_QUESTIONS.html').replace('\\', '/')
pdf_path = os.path.abspath('CLIENT_DISCOVERY_MEETING_PLAYBOOK_AND_QUESTIONS.pdf')
url = f'file:///{html_path}'

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--print-to-pdf={pdf_path}',
    '--no-pdf-header-footer',
    url
]
print(f"Rendering {url} -> {pdf_path}...")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    sz = os.path.getsize(pdf_path)
    print(f"Generated PDF: {pdf_path} ({sz / 1024:.1f} KB)")
    artifact_dst = os.path.join(r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62', os.path.basename(pdf_path))
    shutil.copyfile(pdf_path, artifact_dst)
    print(f"Copied to artifact dir: {artifact_dst} (Verified: {os.path.exists(artifact_dst)})")
else:
    print("PDF generation failed.")
    print("Stderr:", res.stderr)

