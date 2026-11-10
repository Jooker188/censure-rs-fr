from PIL import Image, ImageDraw, ImageFilter
I="captures/"   # captures d'origine (non publiées), à placer dans video/tweets/captures/
O="./"
# (fichier, nom, boîte de découpe, zones à masquer en coordonnées de l'image source)
T=[("17.png","T_dictature",(48,1300,1244,1500),[(70,1318,170,1408),(170,1322,425,1368)]),
   ("17.png","T_zero_tweets",(48,1082,1244,1298),[(70,1086,170,1176),(170,1088,600,1132)]),
   ("16.png","T_fait_flipper",(24,560,1220,745),[(45,566,145,656),(148,572,612,618)]),
   ("16.png","T_magace",(24,1240,1220,1418),[(45,1242,145,1332),(148,1246,470,1292)]),
   ("15.png","T_date_censure",(36,40,1232,262),[(62,40,160,135),(160,44,520,90)]),
   ("18.webp","T_radiolondres",(18,30,1212,250),[(40,38,140,130),(140,40,440,88)]),
   ("14.png","T_tiktok_avertissement",(36,30,1232,1380),[(56,36,160,130),(160,40,560,90)])]
for f,n,box,masques in T:
    im=Image.open(I+f).convert("RGB"); d=ImageDraw.Draw(im)
    for (x0,y0,x1,y1) in masques[1:]:   # le premier masque est l'avatar : on le garde visible
        zone=im.crop((x0,y0,x1,y1))
        petit=zone.resize((max(1,(x1-x0)//12),max(1,(y1-y0)//12)))
        zone=petit.resize(zone.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(6))
        im.paste(zone,(x0,y0))
    im.crop(box).save(O+n+".png")
    print(n, im.crop(box).size)
# découpes serrées pour la miniature (sans la barre d'actions)
SERRES=[("16.png","M_fait_flipper",(40,560,730,665),[(45,566,145,656),(148,572,612,618)]),
        ("17.png","M_dictature",(66,1312,835,1415),[(70,1318,170,1408),(170,1322,425,1368)]),
        ("17.png","M_zero_tweets",(66,1080,1185,1215),[(70,1086,170,1176),(170,1088,600,1132)]),
        ("16.png","M_magace",(40,1236,1125,1338),[(45,1242,145,1332),(148,1246,470,1292)])]
for f,n,box,masques in SERRES:
    im=Image.open(I+f).convert("RGB"); d=ImageDraw.Draw(im)
    for (x0,y0,x1,y1) in masques[1:]:   # le premier masque est l'avatar : on le garde visible
        zone=im.crop((x0,y0,x1,y1))
        petit=zone.resize((max(1,(x1-x0)//12),max(1,(y1-y0)//12)))
        zone=petit.resize(zone.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(6))
        im.paste(zone,(x0,y0))
    im.crop(box).save(O+n+".png")
