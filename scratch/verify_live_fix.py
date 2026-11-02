import subprocess, os, shutil
from PIL import Image

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# 1. Test index.html
html_path = os.path.abspath('new/dalalmachine/index.html').replace('\\', '/')
url = f'file:///{html_path}'
out_img = os.path.abspath('scratch/live_home_verified.png')

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--screenshot={out_img}',
    '--window-size=1280,1200',
    url
]
subprocess.run(cmd)

if os.path.exists(out_img):
    im = Image.open(out_img)
    # Crop the cards section
    cards_crop = im.crop((120, 520, 1160, 1080))
    artifact_dst = r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62\cards_final_verified.png'
    cards_crop.save(artifact_dst)
    print("Saved cards_final_verified.png!")
else:
    print("Failed to capture index.html")

