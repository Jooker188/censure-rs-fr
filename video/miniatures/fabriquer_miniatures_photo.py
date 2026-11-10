import sys
import os
D=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(D,"..","mascotte","apercus"); T=os.path.join(D,"..","tweets"); P=D+"/polices"; PH=D+"/photos"
css=f"""@font-face{{font-family:Anton;src:url('file://{P}/anton.woff2')}}
*{{box-sizing:border-box}} html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#0b0d0c;color:#fff;font-family:Inter,sans-serif}}
.tw{{position:absolute;border-radius:16px;border:3px solid #3a3f44;box-shadow:0 18px 50px rgba(0,0,0,.85);background:#000}}
.photo{{position:absolute;right:0;top:0;width:760px;height:720px;object-fit:cover;object-position:50% 10%;-webkit-mask:linear-gradient(to right,transparent 0%,#000 38%);filter:saturate(.85) contrast(1.05) brightness(.9)}}
.titre{{position:absolute;font-family:Anton;line-height:1;color:#FFD60A;-webkit-text-stroke:10px #000;paint-order:stroke fill;text-shadow:0 0 40px rgba(255,214,10,.5),0 10px 0 #000}}"""
def page(c): return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{c}</body></html>"
def compo(photo, pose="apercu-lunettes-relevees"):
    return f"""<img class='photo' src='file://{PH}/{photo}'>
 <div style='position:absolute;inset:0;background:linear-gradient(to top,rgba(11,13,12,.85) 0%,transparent 35%)'></div>
 <div class='titre' style='left:40px;top:14px;font-size:200px'>CENSURÉ ?</div>
 <img class='tw' src='file://{T}/M_fait_flipper.png' style='left:560px;top:440px;width:600px;transform:rotate(-3deg)'>
 <img class='tw' src='file://{T}/M_dictature.png' style='left:600px;top:575px;width:640px;transform:rotate(2deg)'>
 <img src='file://{A}/{pose}.svg' style='position:absolute;left:-10px;bottom:-10px;height:520px;filter:drop-shadow(0 0 26px rgba(0,0,0,.85))'>"""
V={"E1_macron": compo("macron_2024.jpg"), "E2_lecornu": compo("lecornu_2025.jpg")}
for n,c in V.items(): open(f"{D}/{n}.html","w",encoding="utf-8").write(page(c))


def rendre(noms):
    """Rend les pages HTML en PNG 1280×720 avec Chromium (Playwright pour Node)."""
    import json, os, subprocess
    js = os.path.join(D, ".rendu.js")
    open(js, "w").write("""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
for(const n of %s){await p.goto('file://%s/'+n+'.html');await p.evaluate(()=>document.fonts.ready);
await p.waitForTimeout(600);await p.screenshot({path:'%s/'+n+'.png'});}await b.close();})();""" % (json.dumps(noms), D, D))
    subprocess.run(["node", js], check=True)
    os.remove(js)
    for n in noms:
        os.remove(os.path.join(D, n + ".html"))
    print("Écrits :", ", ".join(n + ".png" for n in noms))


rendre(list(V))
