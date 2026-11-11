"""Render each app page in light and dark and report text that cannot be read."""
import json, os, subprocess, sys, socket, time, glob, re

MEASURE = r"""
<script>
(function(){
  // normalise through a canvas: computed colours come back as hex, rgb(), rgba() and
  // color-mix() - and parsing numbers straight out of "#0b1f14" reads 0, 1, 31, 14
  var _cv=document.createElement('canvas').getContext('2d');
  function norm(c){try{_cv.fillStyle='#000';_cv.fillStyle=c;return _cv.fillStyle;}catch(e){return null;}}
  function lum(c){
    if(!c)return null;
    var r,g,b;
    // color(srgb 0.94 0.93 0.88 / 0.88): Chromium returns modern colours this way, and a
    // canvas refuses them, so they are parsed here rather than normalised
    var cs2=c.match(/color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)/);
    if(cs2){r=+cs2[1];g=+cs2[2];b=+cs2[3];}
    else {c=norm(c);if(!c)return null;
      var m=c.match(/\d+(\.\d+)?/g);if(!m)return null;
      if(c.charAt(0)==='#'){r=parseInt(c.substr(1,2),16)/255;g=parseInt(c.substr(3,2),16)/255;b=parseInt(c.substr(5,2),16)/255;}
      else {r=+m[0]/255;g=+m[1]/255;b=+m[2]/255;}}
    function f(v){return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);}
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b);}
  function opaque(c){
    if(!c||c==='transparent')return false;
    if(c.indexOf('color-mix')>=0)return false;            // a blend of the page colour: walk past it
    var ca=c.match(/color\(srgb[^)]*\/\s*([\d.]+)/);
    if(ca&&parseFloat(ca[1])<0.9)return false;            // translucent modern colour
    var m=c.match(/rgba?\(([^)]+)\)/);
    if(m){var p=m[1].split(',');if(p.length>3&&parseFloat(p[3])<0.9)return false;}
    return true;
  }
  function bgOf(el){var e=el;while(e){var cs=getComputedStyle(e);
    if(cs.backgroundImage&&cs.backgroundImage!=='none')return null;   // a photo or a gradient: not computable
    if(opaque(cs.backgroundColor))return cs.backgroundColor;e=e.parentElement;}
    return 'rgb(255,255,255)';}
  var bad=[],seen={},skip=0;
  document.querySelectorAll('button,a,h1,h2,h3,p,span,label,li,td,th').forEach(function(el){
    var t=(el.textContent||'').trim(); if(!t||t.length<2) return;
    var r=el.getBoundingClientRect(); if(r.width<4||r.height<4) return;
    var cs=getComputedStyle(el); // a reveal-on-scroll section is mid-animation at load: its real colour is not yet on screen
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.9) return;
    var bgc=bgOf(el); if(bgc===null){skip++;return;}
    var fg=lum(cs.color), bg=lum(bgc); if(fg===null||bg===null) return;
    var L1=Math.max(fg,bg), L2=Math.min(fg,bg); var ratio=(L1+0.05)/(L2+0.05);
    if(ratio<2.0){var k=el.tagName+'.'+(el.className||'').toString().slice(0,24)+'|'+t.slice(0,28);
      if(!seen[k]){seen[k]=1;bad.push({sel:el.tagName,cls:(el.className||'').toString().slice(0,40),text:t.slice(0,40),ratio:Math.round(ratio*100)/100,fg:cs.color,bg:bgOf(el)});}}
  });
  var out=document.createElement('pre'); out.id='__contrast__';
  out.textContent='CONTRAST_JSON'+JSON.stringify({theme:document.documentElement.getAttribute('data-theme')||'(none)',bad:bad.slice(0,12),total:bad.length,unmeasurable:skip});
  document.body.appendChild(out);
})();
</script>
"""

def free_port():
    s=socket.socket(); s.bind(("127.0.0.1",0)); p=s.getsockname()[1]; s.close(); return p

def probe(repo, page, theme):
    # a working copy under the current directory: /scratch does not exist on a CI runner
    d = os.path.join(os.environ.get("CONTRAST_WORKDIR", "/scratch/work"), f"ct_{repo}")
    if not os.path.isdir(d):
        subprocess.run(["gh","repo","clone",f"drsamonline/{repo}",d,"--","--depth","1"], capture_output=True)
    full = os.path.join(d, page)
    if not os.path.exists(full): return None
    html = open(full, encoding="utf-8", errors="replace").read()
    if theme == "dark":
        # set the attribute AND the stored preference before the page's own script runs,
        # so a toggle that reads localStorage at load starts in dark
        html = re.sub(r'data-theme="[^"]*"', 'data-theme="dark"', html, count=1)
        if 'data-theme=' not in html:
            html = html.replace('<html', '<html data-theme="dark"', 1)
        html = html.replace("<head>", "<head><script>try{['theme','chalk-theme','kre-landing-theme','colour-theme','color-theme','mode'].forEach(function(k){localStorage.setItem(k,'dark')});}catch(e){}</script>", 1)
    tmp = full + ".probe.html"
    open(tmp, "w", encoding="utf-8").write(html.replace("</body>", MEASURE + "</body>"))
    port = free_port()
    # serve from the page's own directory: the temp file sits beside it, so serving the
    # repo root made the URL a 404 and every page reported "no measurement"
    srv = subprocess.Popen([sys.executable,"-m","http.server",str(port)], cwd=os.path.dirname(full),
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    r = subprocess.run([os.environ.get("CHROMIUM_BIN","chromium"),"--headless","--disable-gpu","--no-sandbox","--ignore-certificate-errors",
                        "--virtual-time-budget=4000","--dump-dom",
                        f"http://127.0.0.1:{port}/{os.path.basename(tmp)}"], capture_output=True, text=True, timeout=90)
    srv.terminate(); os.remove(tmp)
    # the dumped DOM contains the <script> source too, which also says CONTRAST_JSON -
    # match the rendered <pre>, not the first mention in the page
    m = re.search(r'<pre id="__contrast__">CONTRAST_JSON(.*?)</pre>', r.stdout or "", re.S)
    return json.loads(m.group(1)) if m else None

missing = 0
for repo, page in [tuple(a.split(":")) for a in sys.argv[1:]]:
    for theme in ("light","dark"):
        res = probe(repo, page, theme)
        if res is None:
            print(f"{repo:22} {theme:5} NO MEASUREMENT - the page did not render or the browser is missing")
            missing += 1
            continue
        print(f"{repo:22} {theme:5} unreadable={res['total']:3} unmeasurable={res.get('unmeasurable',0):3}  {[ (b['sel'],b['text'][:18],b['ratio']) for b in res['bad'][:3] ]}")

# A RUN THAT MEASURED NOTHING MUST NOT PASS. The first CI run of this tool reported every
# page as "no measurement" - no browser on the runner - and the workflow went green,
# because nothing failed. Exit non-zero when a page could not be read at all.
if missing:
    print(f"\n{missing} measurement(s) could not be taken - treating that as a failure")
    sys.exit(1)
