"""Sample the real pixels behind each text run, so a photograph or a gradient is measured
rather than skipped.

The computed-style check cannot answer "what colour is behind this text?" when the answer
is a photo. This renders the page, crops each element's box out of the screenshot, takes
the MEDIAN colour of that crop as the background (glyph pixels are a minority in a text
box, so the median is the paper, not the ink) and compares it with the element's own
colour.
"""
import json, os, re, socket, subprocess, sys, tempfile, time

COLLECT = r"""
<script>
(function(){
  var _cv=document.createElement('canvas').getContext('2d');
  function norm(c){try{_cv.fillStyle='#000';_cv.fillStyle=c;return _cv.fillStyle;}catch(e){return null;}}
  var out=[];
  document.querySelectorAll('button,a,h1,h2,h3,h4,p,span,label,li,td,th').forEach(function(el){
    var t=(el.textContent||'').trim(); if(!t||t.length<2) return;
    var r=el.getBoundingClientRect(); if(r.width<6||r.height<6) return;
    var cs=getComputedStyle(el);
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.9) return;
    // measure the element that actually paints the text: a <li> inherits one colour while
    // the <a> inside it carries another, and the list item is the wrong node to judge
    if(el.querySelector('a,span,strong,em') && el.querySelector('a,span,strong,em').textContent.trim()===t) return;
    if(r.top<0||r.top>window.innerHeight-4) return;      // only what is on this screenful
    out.push({x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),
              c:norm(cs.color)||cs.color,t:t.slice(0,32),tag:el.tagName,
              grad:cs.backgroundImage!=='none'});
  });
  var p=document.createElement('pre');p.id='__pixels__';
  p.textContent='PIXELS_JSON'+JSON.stringify(out.slice(0,400));
  document.body.appendChild(p);
})();
</script>
"""

def free_port():
    s=socket.socket(); s.bind(("127.0.0.1",0)); p=s.getsockname()[1]; s.close(); return p

def lum(rgb):
    def f(v):
        v/=255.0
        return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b = rgb[0],rgb[1],rgb[2]
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)

def ratio(a,b):
    la,lb = lum(a),lum(b)
    hi,lo = max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)

def check(repo, page):
    workdir = os.environ.get("CONTRAST_WORKDIR","/scratch/work")
    d = os.path.join(workdir, f"ct_{repo}")
    if not os.path.isdir(d):
        subprocess.run(["gh","repo","clone",f"drsamonline/{repo}",d,"--","--depth","1"], capture_output=True)
    full = os.path.join(d, page)
    if not os.path.exists(full): return None
    html = open(full, encoding="utf-8", errors="replace").read()
    probe = full + ".px.html"
    open(probe,"w",encoding="utf-8").write(html.replace("</body>", COLLECT+"</body>"))
    port = free_port()
    srv = subprocess.Popen([sys.executable,"-m","http.server",str(port)], cwd=os.path.dirname(full),
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    binp = os.environ.get("CHROMIUM_BIN","chromium")
    url = f"http://127.0.0.1:{port}/{os.path.basename(probe)}"
    shot = os.path.join(tempfile.mkdtemp(), "page.png")
    try:
        r = subprocess.run([binp,"--headless","--disable-gpu","--no-sandbox","--ignore-certificate-errors",
                            "--hide-scrollbars","--window-size=1280,900",
                            # a page that never settles will hold the browser open forever:
                            # virtual time makes it give up on its own
                            "--virtual-time-budget=5000",
                            f"--screenshot={shot}","--dump-dom",url],
                           capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        srv.terminate(); os.remove(probe)
        return {"timeout": True}
    srv.terminate(); os.remove(probe)
    m = re.search(r'<pre id="__pixels__">PIXELS_JSON(.*?)</pre>', r.stdout or "", re.S)
    if not m or not os.path.exists(shot): return None
    els = json.loads(m.group(1))
    from PIL import Image
    im = Image.open(shot).convert("RGB")
    bad = []
    skipped_grad = 0
    for e in els:
        box = (max(0,e["x"]), max(0,e["y"]), min(im.width,e["x"]+e["w"]), min(im.height,e["y"]+e["h"]))
        if box[2]-box[0] < 4 or box[3]-box[1] < 4: continue
        crop = im.crop(box)
        # SAMPLE THE EDGE, not the middle. In a small button the glyphs outnumber the paper,
        # and a glowing text-shadow puts its colour around every letter - both make the
        # middle of the box a poor answer to "what is behind this text". The ring a few
        # pixels inside the box edge is background in every layout worth measuring.
        from collections import Counter
        # SAMPLE THE RING JUST INSIDE THE BOX EDGE. The middle of a small button is glyphs,
        # and a text glow puts its colour around every letter; the ring is background in
        # every layout that is not deliberately glitch-styled.
        w, h = crop.size
        ring = []
        m = max(1, min(3, w // 8, h // 8))
        for x in range(w):
            for y in (m, h - 1 - m):
                ring.append(crop.getpixel((x, y)))
        for y in range(m, h - m):
            for x in (m, w - 1 - m):
                ring.append(crop.getpixel((x, y)))
        px = ring or list(crop.getdata())
        px = px or list(crop.getdata())
        bg = Counter(px).most_common(1)[0][0]
        c = e["c"]
        if c.startswith("#"):
            fg = [int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)]
        elif c.startswith("color("):
            # color(srgb 0.717 0.739 0.691): channels are 0..1, not 0..255
            fg = [int(round(float(v)*255)) for v in re.findall(r"[\d.]+", c)[:3]]
        else:
            fg = [int(float(v)) for v in re.findall(r"[\d.]+", c)[:3]]
        if len(fg) < 3: continue
        rr = ratio(fg, bg)
        if e.get("grad"):
            skipped_grad += 1
            continue
        if rr < 2.0:
            bad.append({"text": e["t"], "tag": e["tag"], "ratio": round(rr,2), "fg": e["c"], "bg": tuple(bg)})
    return {"checked": len(els), "bad": bad, "gradient": skipped_grad}

for spec in sys.argv[1:]:
    repo, page = spec.split(":",1)
    res = check(repo, page)
    if res is None:
        print(f"{repo:24} NO MEASUREMENT"); continue
    if res.get("timeout"):
        print(f"{repo:24} TIMEOUT - the page did not settle, so it was not measured"); continue
    print(f"{repo:24} checked={res['checked']:3} unreadable={len(res['bad']):2} gradient={res.get('gradient',0):2}  {[(b['tag'],b['text'][:16],b['ratio'],b['bg']) for b in res['bad'][:4]]}")
