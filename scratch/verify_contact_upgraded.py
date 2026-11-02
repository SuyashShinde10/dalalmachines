import subprocess, os
from PIL import Image

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
html_path = os.path.abspath('new/dalalmachine/contact.html').replace('\\', '/')
url = f'file:///{html_path}'
out_img = os.path.abspath('scratch/contact_upgraded.png')

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--screenshot={out_img}',
    '--window-size=1280,1050',
    url
]
subprocess.run(cmd)

if os.path.exists(out_img):
    im = Image.open(out_img)
    # Crop around the two cards
    crop = im.crop((100, 220, 1180, 850))
    artifact_dst = r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62\contact_upgraded_verified.png'
    crop.save(artifact_dst)
    print("Saved contact_upgraded_verified.png successfully! Size:", os.path.getsize(artifact_dst))
else:
    print("Failed")

