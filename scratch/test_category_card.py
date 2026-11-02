import subprocess, os, shutil
from PIL import Image

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
html_path = os.path.abspath('new/dalalmachine/category.html').replace('\\', '/')
url = f'file:///{html_path}'
out_img = os.path.abspath('scratch/category_card_fixed.png')

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--screenshot={out_img}',
    '--window-size=1280,1000',
    url
]
subprocess.run(cmd)

if os.path.exists(out_img):
    im = Image.open(out_img)
    # On category page, cards are in the middle-right area
    im.save(r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62\category_card_fixed.png')
    print("Category screenshot saved successfully!")
else:
    print("Failed")

