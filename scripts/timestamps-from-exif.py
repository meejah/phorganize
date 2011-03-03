#!/usr/bin/env python

##
## for all images on the command-line, use exiv2 to determine the date
## it was taken and change ctime and mtime on the file.
##

import pyexiv2
import sys
import os


## note: this looks a lot different than the docs (and tutorial, which
## is also different) from http://tilloy.net/dev/pyexiv2/tutorial.html
## using whatever version Debian gave me (doesn't have pyexiv2.version)

for fname in sys.argv[1:]:
    md = pyexiv2.Image(fname)
    md.readMetadata()
    dt = md['Exif.Photo.DateTimeOriginal']
    cmd = 'touch -t "%s" %s' % (dt.strftime('%Y%m%d%H%M'), fname)
    print cmd
    os.system(cmd)
    
        
