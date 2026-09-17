import subprocess, urllib.request, textwrap
from pathlib import Path

ROOT = Path('public/shopify-videos')
ROOT.mkdir(parents=True, exist_ok=True)
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

products = [
('hair-roller','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/Hcbf7198ad68a482884387b6d035b7c07O.webp?v=1789318205','Pet hair everywhere?','Reusable cleanup for sofa, clothes and car seats','Car seats covered in fur?','Roll it up, rinse it, reuse it'),
('grooming-glove','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/Sdd1513d36261465ba99e6da9ad12e22dk.webp?v=1789321116','Groom while you pet','Collect loose fur with a soft grooming glove','Shedding season?','Easy deshedding for dogs and cats'),
('dog-harness','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/S48e8bce8284140fe8953850b9133d65dd.webp?v=1789296123','Make walks feel more secure','Adjustable fit, front clip and reflective detail','Daily walk upgrade','Handle, front clip and adjustable fit'),
('water-bottle','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/Scda8b99e37db429ca3f321204b161202J.webp?v=1789318206','Water on every walk','Built-in drinking trough for dogs on the go','No separate bowl needed','Portable dog water bottle for walks and travel'),
('lick-mat','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/S8761c3e126e740dbaf054248838fcf320.webp?v=1789318205','Bath time distraction','Suction lick mat for grooming and slow feeding','Keep them busy','Textured lick mat for dogs'),
('cat-disc','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/S387a44f17ba4438db78db2b1ca3850a5j.webp?v=1789318206','Give your cat something to chase','Interactive flying-disc launcher for indoor play','Playtime in one trigger','Launch light discs for chase play'),
('poop-bag-holder','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/Sa403c6b47be64752bc5db2041a5a4661k.webp?v=1789298334','Never forget the bags','Clip-on mesh waste-bag holder for dog walks','Walk-ready in seconds','Keep waste bags clipped to the lead'),
('travel-bowl','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/Sdfe687791a8f4b1b8d5d383c253f5fbaf.webp?v=1789296124','A bowl that folds flat','Collapsible silicone bowl with carabiner','Travel lighter with your dog','350ml fold-flat bowl for walks and trips'),
('treat-pouch','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/S0a0fa18d75564229b4aa6defe718989dm.webp?v=1789318206','Rewards right when you need them','Clip-on training pouch keeps treats close','Training walk essential','Quick-access treat pouch for dog training'),
('deshedding-rake','https://cdn.shopify.com/s/files/1/1095/9624/6341/files/S2d47b2cca0a24d418b2efd761c089d795.webp?v=1789321115','Thick coat? Start here','Two-sided rake for tangles and loose fur','Two sides, one grooming tool','Dematting and deshedding for dogs and cats'),
]

def download(url, dest):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r, open(dest, 'wb') as f:
        f.write(r.read())

def render(slug, image, variant, hook, benefit):
    hook_file = ROOT / f'{slug}_{variant}_hook.txt'
    benefit_file = ROOT / f'{slug}_{variant}_benefit.txt'
    cta_file = ROOT / f'{slug}_{variant}_cta.txt'
    hook_file.write_text(textwrap.fill(hook, 24), encoding='utf-8')
    benefit_file.write_text(textwrap.fill(benefit, 30), encoding='utf-8')
    cta_file.write_text('Shop now - link in bio', encoding='utf-8')
    out = ROOT / f'{slug}_{variant}.mp4'
    vf = (
        "scale=600:930:force_original_aspect_ratio=decrease,"
        "pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=0xf5f5f5,"
        "zoompan=z='min(zoom+0.0008,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=360:s=720x1280:fps=30,"
        "drawbox=x=0:y=0:w=iw:h=205:color=black@0.82:t=fill,"
        "drawbox=x=0:y=1045:w=iw:h=235:color=black@0.82:t=fill,"
        f"drawtext=fontfile='{FONT_BOLD}':textfile='{hook_file}':fontcolor=white:fontsize=42:line_spacing=8:x=(w-text_w)/2:y=48,"
        f"drawtext=fontfile='{FONT_REG}':textfile='{benefit_file}':fontcolor=white:fontsize=30:line_spacing=7:x=(w-text_w)/2:y=1082,"
        f"drawtext=fontfile='{FONT_BOLD}':textfile='{cta_file}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=1210"
    )
    cmd = ['ffmpeg','-y','-loop','1','-i',str(image),'-t','12','-vf',vf,'-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(out)]
    subprocess.run(cmd, check=True)
    hook_file.unlink(); benefit_file.unlink(); cta_file.unlink()

for slug, url, h1, b1, h2, b2 in products:
    image = ROOT / f'{slug}.webp'
    download(url, image)
    render(slug, image, 'a', h1, b1)
    render(slug, image, 'b', h2, b2)
    image.unlink()
print('CREATED 20')
