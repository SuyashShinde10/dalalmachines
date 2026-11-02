import subprocess, os
from PIL import Image

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
html_path = os.path.abspath('new/dalalmachine/contact.html').replace('\\', '/')
url = f'file:///{html_path}'
out_img = os.path.abspath('scratch/contact_verified.png')

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
    # Crop around the inquiry form header
    crop = im.crop((100, 220, 1180, 780))
    crop.save(r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62\contact_form_verified.png')
    print("Saved contact_form_verified.png!")
else:
    print("Failed")

