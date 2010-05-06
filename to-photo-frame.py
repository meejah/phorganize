#!/usr/bin/env python


out_size = (480,234)

## simple script to copy to frame; just take any picture which is the
## right "way" around and resize to 480 pixels wide -- this won't be
## the right aspect ratio (the frame as 16:9) but oh well...

width = 480

import sys
import os
from PIL import Image

num = 0
for f in sys.argv[1:]:
    if not os.path.isfile(f):
        continue

    try:
        a = Image.open(f)
    except:
        print "failed:",f
        continue
    if a.size[0] < a.size[1]:
        print "wrong aspect:",f
        continue

    ext = os.path.splitext(f)[-1]
    cmd = "convert -resize %dx%d %s %s" % (width, width, f, "/mnt/foo/%05d%s"%(num,ext))
    os.system(cmd)
    print cmd

    num += 1
        
