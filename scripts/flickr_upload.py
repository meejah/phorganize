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

token = fapi.getToken(browser="lynx",perms="delete")
mikeapi = MikeFlickr(fapi,flickrAPIKey,token)

## methods

def userinput(prompt):
    rtn = ''
    while len(rtn) == 0:
        rtn = raw_input(prompt).strip()
    return rtn

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

    toupload.append(jpeg)

print "found",len(toupload),"images to upload."

for jpeg in toupload:
    print jpeg
    while True:
        name = userinput("Name:")
        desc = userinput("Description:")
        tags = userinput("Tags:")

        print name
        print
        print desc
        print "tags:",tags
        good = False
        while not good:
            yn = userinput("ok ?")
            yn = yn.strip().lower()
            if len(yn) > 0 and (yn[0] is 'y' or yn[0] is 'n'):
                good = True
        if yn[0] == 'y':
            print "...uploading",jpeg,
            sys.stdout.flush()

            try:
                photoid = mikeapi.upload(jpeg,
                                         title=name,
                                         description=desc,
                                         tags=tags,
                                         isPublic=True,
                                         isFriend=False,
                                         isFamily=False)
                print "done; id=",photoid
            except:
                print "ERROR"

            break

        else:
            print "trying again"
