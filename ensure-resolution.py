

from PIL import Image
import os

for f in os.listdir('.'):
    try:
        img = Image.open(f)
    except:
        print "error on",f
        continue

    (w,h) = img.size
    print f,w,h

    if h > 768:
        ratio = float(h)/768.0
        newwidth = int(w / ratio)
        print "   scaling to",newwidth,768
        img = img.resize( (newwidth, 768), Image.ANTIALIAS )
        print "   saving..."
        img.save(f)
    
