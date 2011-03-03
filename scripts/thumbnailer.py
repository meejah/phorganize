#!/usr/bin/env python

## makes 400x400 "thumbnails" of everything in photos-canon (into
## photos-canon/thumbs)

import os
import subprocess

IMAGES = '/home/mike/photos-canon'
THUMBS = '/home/mike/photos-canon/thumbnails'

for f in os.listdir(IMAGES):
    if f[:4] != 'IMG_' or f[-3:].lower() != 'jpg':
        print "skipping",f
        continue

    if os.path.exists(os.path.join(THUMBS,'small_'+f)):
        if os.stat(os.path.join(THUMBS,'small_'+f)).st_ctime >= os.stat(os.path.join(IMAGES,f)).st_ctime:
            print "already done",f
            continue
    
    cmd = ['convert','-resize','400x400',os.path.join(IMAGES,f),os.path.join(THUMBS,'small_'+f)]
    print ' '.join(cmd)
    subprocess.call(cmd)
    
