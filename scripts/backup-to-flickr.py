#!/usr/bin/env python

import sys
import os
sys.path.insert(0,'/home/mike/python')

from flickrapi import FlickrAPI
from flickr import MikeFlickr

flickrAPIKey = open('/home/mike/flickr.key', 'r').read()
flickrSecret = open('/home/mike/flickr.secret', 'r').read()

fapi = None
fapi = FlickrAPI(flickrAPIKey, flickrSecret)

if len(sys.argv) < 2:
    print "usage: %s JPEG [JPEG]" % sys.argv[0]
    sys.exit(-1)

token = fapi.getToken(browser="lynx")
mikeapi = MikeFlickr(fapi,flickrAPIKey,token)

##
## first get info from Flickr on what I've already backed up, by the
## "mikebackup" tag
##

existing = mikeapi.imagesByTag("mikebackup", privateOnly=True)
print "got",len(existing),"existing photos."

names = map(lambda x: x[1].lower(), existing)
#print names[:10]

##
## now, upload everything on the command line (unless we have already
## backed it up)
##

toupload = []
for jpeg in sys.argv[1:]:
    if os.stat(jpeg).st_size == 0:
        print "zero-size:",jpeg,"...skipping"
        continue

    if os.path.split(jpeg)[-1].split('.')[-1].lower() in ['avi','mov']:
        print "movie, skipping:",jpeg
        continue        

    if os.path.split(jpeg)[-1].split('.')[0].lower() in names:
        print "already on flickr, skipping:",jpeg
        continue

    toupload.append(jpeg)

print "found",len(toupload),"images to upload."
#print toupload

for jpeg in toupload:
    print "uploading",jpeg,
    sys.stdout.flush()
    title = os.path.split(jpeg)[-1]
    title = title.split('.')[0]

    try:
        photoid = mikeapi.upload(jpeg,
                                 title=title,
                                 description='backup of "%s"' % jpeg,
                                 tags='mikebackup',
                                 isPublic=False,
                                 isFriend=False,
                                 isFamily=False)
        print "done; id=",photoid
    except:
        print "ERROR"
