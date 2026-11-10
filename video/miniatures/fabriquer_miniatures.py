import os
D=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(D,"..","mascotte","apercus"); T=os.path.join(D,"..","tweets"); P=D+"/polices"
css=f"""@font-face{{font-family:Anton;src:url('file://{P}/anton.woff2')}} @font-face{{font-family:ArchivoBlack;src:url('file://{P}/archivo-black.woff2')}}
*{{box-sizing:border-box}} html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#0b0d0c;color:#fff;font-family:Inter,sans-serif}}
.tw{{position:absolute;border-radius:16px;border:3px solid #3a3f44;box-shadow:0 18px 50px rgba(0,0,0,.8);background:#000}}
.fond{{position:absolute;opacity:.28;filter:blur(1.5px) grayscale(.2)}}"""
def page(c): return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{c}</body></html>"
fond = "".join(f"<img class='fond' src='file://{T}/{n}.png' style='left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg)'>"
   for n,x,y,w,r in [("T_zero_tweets",-60,10,760,-4),("T_magace",560,-20,760,3),("T_date_censure",-40,250,720,2),
                     ("T_radiolondres",620,300,760,-3),("T_dictature",-80,520,700,-2),("T_fait_flipper",600,560,720,4)])
V={
"D1_detective": f"""{fond}
 <div style='position:absolute;inset:0;background:radial-gradient(circle at 72% 60%,rgba(255,214,10,.18) 0%,rgba(11,13,12,.2) 35%,rgba(11,13,12,.85) 75%)'></div>
 <div style='position:absolute;left:44px;top:18px;font-family:Anton;font-size:215px;line-height:1;color:#FFD60A;-webkit-text-stroke:10px #000;paint-order:stroke fill;text-shadow:0 0 40px rgba(255,214,10,.55),0 10px 0 #000'>CENSURÉ ?</div>
 <img class='tw' src='file://{T}/M_fait_flipper.png' style='left:46px;top:330px;width:640px;transform:rotate(-4deg)'>
 <img class='tw' src='file://{T}/M_dictature.png' style='left:70px;top:480px;width:660px;transform:rotate(2deg)'>
 <img src='file://{A}/apercu-lunettes-relevees.svg' style='position:absolute;right:-40px;bottom:-10px;height:660px;filter:drop-shadow(0 0 30px rgba(0,0,0,.8))'>""",
"D2_minimal": f"""
 <div style='position:absolute;left:640px;top:520px;width:1500px;height:1500px;transform:translate(-50%,-50%);border-radius:50%;background:repeating-conic-gradient(from 0deg,#d9480f 0deg 9deg,#1a0f0b 9deg 18deg);opacity:.9;-webkit-mask:radial-gradient(circle,#000 18%,transparent 62%)'></div>
 <div style='position:absolute;left:0;right:0;top:20px;text-align:center;font-family:ArchivoBlack;font-size:150px;line-height:1;letter-spacing:-3px;color:#fff;text-shadow:0 8px 0 #000,0 0 30px rgba(0,0,0,.6)'>Censuré ?</div>
 <img class='tw' src='file://{T}/M_fait_flipper.png' style='left:30px;top:250px;width:500px;transform:rotate(-6deg)'>
 <img class='tw' src='file://{T}/M_dictature.png' style='left:760px;top:300px;width:500px;transform:rotate(5deg)'>
 <img src='file://{A}/apercu-sceptique.svg' style='position:absolute;left:50%;bottom:-12px;height:540px;transform:translateX(-50%);filter:drop-shadow(0 0 24px rgba(0,0,0,.7))'>""",
}
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
