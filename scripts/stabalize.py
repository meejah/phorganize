#!/usr/bine/env python

##
## using "transcode" this will stabalize a shaky video
## see http://public.hronopik.de/vid.stab/features.php?lang=en
##
## options: input-file and output-file
##

import sys
import os

if len(sys.argv) != 3:
    print "usage: %s input output" % sys.argv
    sys.exit(-1)

infname = sys.argv[1]
outfname = sys.argv[2]

print "stabalizing video %s writing to %s" % (infname, outfname)

cmd = 'transcode -J stabilize -i %s -y null,null -o dummy' % infname
## for extra shaky videos, apparently try something like the following for this step:
## cmd = 'transcode -J stabilize=shakiness=32 -i %s -y null,null -o dummy' % infname
print cmd
os.system(cmd)

cmd = 'transcode -J transform -i %s -o %s -y ffmpeg -F mpeg4' % (infname, outfname)
print cmd
os.system(cmd)
