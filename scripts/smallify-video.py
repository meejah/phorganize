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

print "rescaling video %s writing to %s" % (infname, outfname)

cmd = 'mencoder "%s" -oac copy -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -vf scale=640:360 -o "%s"' % (infname, outfname)
print cmd
os.system(cmd)
