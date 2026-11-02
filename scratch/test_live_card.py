import subprocess, os, shutil

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
html_path = os.path.abspath('new/dalalmachine/index.html').replace('\\', '/')
url = f'file:///{html_path}'
out_img = os.path.abspath('scratch/live_card_fixed.png')

cmd = [
    edge,
    '--headless',
    '--disable-gpu',
    f'--screenshot={out_img}',
    '--window-size=1280,1100',
    url
]
subprocess.run(cmd)

if os.path.exists(out_img):
    print("Screenshot exists! Size:", os.path.getsize(out_img))
    artifact_dst = r'C:\Users\91940\.gemini\antigravity\brain\75a30f5c-ccbc-43b7-9b59-6c8c1ab99b62\live_card_fixed.png'
    shutil.copyfile(out_img, artifact_dst)
    print("Copied to artifact dir:", os.path.exists(artifact_dst))
else:
    print("Failed to capture screenshot")

