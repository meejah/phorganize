#!/usr/bin/env python

import sys
import os
sys.path.insert(0,'/home/mike/python')

from flickrapi import FlickrAPI
from flickr import MikeFlickr

flickrAPIKey = "a0de8ce59dde838ba49666288023d23a"  # API key
flickrSecret = "2e738d4a1f82c483"                  # shared "secret"

fapi = None
fapi = FlickrAPI(flickrAPIKey, flickrSecret)

if len(sys.argv) < 2:
    print "usage: %s JPEG [JPEG]" % sys.argv[0]
    sys.exit(-1)

token = fapi.getToken(browser="lynx",perms="delete")
mikeapi = MikeFlickr(fapi,flickrAPIKey,token)


for jpeg in sys.argv[1:]:
    if os.stat(jpeg).st_size == 0:
        print "zero-size:",jpeg,"...skipping"
        continue
               
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
